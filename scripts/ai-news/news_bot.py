#!/usr/bin/env python3
"""FAI AI-company news bot.

Modes:
  setup    Verify that all company Discussion categories exist (GitHub has no API to create
           categories; manage them at /FAI-Union/FckAI/discussions/categories).
  run      Fetch latest news, dedupe, publish up to N items to the matching Discussion category.
  dry-run  Same as run but does not publish (no token required).

Token resolution (first match wins):
  env GH_PAT
  file <workspace>/.workbuddy/secrets/github_pat.txt

State: <workspace>/.workbuddy/ai-news/state.json
Log:   <workspace>/.workbuddy/ai-news/bot.log

Examples:
  python scripts/ai-news/news_bot.py setup
  python scripts/ai-news/news_bot.py dry-run
  python scripts/ai-news/news_bot.py run --per-run 3
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

REPO_OWNER = "FAI-Union"
REPO_NAME = "FckAI"
ROOT = Path(__file__).resolve().parents[2]
COMPANIES_FILE = Path(__file__).with_name("companies.json")
STATE_DIR = ROOT / ".workbuddy" / "ai-news"
STATE_FILE = STATE_DIR / "state.json"
LOG_FILE = STATE_DIR / "bot.log"
PAT_FILE = ROOT / ".workbuddy" / "secrets" / "github_pat.txt"
API_URL = "https://api.github.com/graphql"
UA = "FAI-News-Bot/1.0 (+https://github.com/FAI-Union/FckAI)"

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src", "spm", "from",
}


def log(msg: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    return {"posted_keys": [], "posted_urls": [], "rotation_index": 0}


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["posted_keys"] = state.get("posted_keys", [])[-5000:]
    state["posted_urls"] = state.get("posted_urls", [])[-5000:]
    state["last_run"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)


def get_token() -> str:
    token = os.environ.get("GH_PAT", "").strip()
    if not token and PAT_FILE.exists():
        token = PAT_FILE.read_text(encoding="utf-8").strip()
    return token


def graphql(query: str, variables: dict, token: str, retries: int = 3) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": UA,
        "Accept": "application/json",
    }
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            if result.get("errors"):
                messages = "; ".join(e.get("message", "unknown") for e in result["errors"])
                raise RuntimeError(f"GraphQL error: {messages}")
            return result.get("data", {})
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")[:300]
            if exc.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"GitHub HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"GitHub network error: {exc}") from exc
    raise RuntimeError("GitHub request failed after retries")


def repo_context(token: str) -> tuple[str, dict[str, dict]]:
    data = graphql(
        """query($owner:String!,$name:String!){
          repository(owner:$owner,name:$name){
            id
            discussionCategories(first:100){ nodes { id name slug } }
          }
        }""",
        {"owner": REPO_OWNER, "name": REPO_NAME},
        token,
    )
    repo = data.get("repository")
    if not repo:
        raise RuntimeError("repository not found or token cannot read it")
    categories = {node["name"]: node for node in repo["discussionCategories"]["nodes"]}
    return repo["id"], categories


def verify_categories(token: str) -> int:
    """GitHub does not expose a category-creation mutation; only verify them here."""
    companies = json.loads(COMPANIES_FILE.read_text(encoding="utf-8"))
    _, existing = repo_context(token)
    missing = []
    for company in companies:
        name = company["category"]
        if name in existing:
            log(f"category OK: {name} (slug={existing[name].get('slug')})")
        else:
            missing.append(name)
            log(f"category MISSING: {name}")
    if missing:
        log(
            "create missing categories at "
            "https://github.com/FAI-Union/FckAI/discussions/categories"
        )
    return len(missing)


def existing_discussion_titles(token: str) -> set[str]:
    data = graphql(
        """query($owner:String!,$name:String!){
          repository(owner:$owner,name:$name){
            discussions(first:100,orderBy:{field:CREATED_AT,direction:DESC}){
              nodes { title category { name } }
            }
          }
        }""",
        {"owner": REPO_OWNER, "name": REPO_NAME},
        token,
    )
    titles = set()
    for node in data["repository"]["discussions"]["nodes"]:
        titles.add(normalize_title(node["title"]))
    return titles


def normalize_title(title: str) -> str:
    text = html.unescape(title or "").lower()
    text = re.sub(r"^\[news\]\s*", "", text)
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text)


def normalize_url(url: str) -> str:
    try:
        parts = urllib.parse.urlsplit(url)
        query = [
            (k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS
        ]
        return urllib.parse.urlunsplit((
            parts.scheme, parts.netloc.lower().removeprefix("www."),
            parts.path.rstrip("/"), urllib.parse.urlencode(query), "",
        ))
    except Exception:
        return (url or "").strip()


def item_key(title: str, url: str) -> str:
    seed = normalize_title(title) + "|" + normalize_url(url)
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()


def fetch_rss(url: str, attempts: int = 3) -> ET.Element | None:
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as resp:
                return ET.fromstring(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < attempts - 1:
                time.sleep(1.5 * (attempt + 1))
                continue
            log(f"RSS HTTP {exc.code}: {url.split('?')[0]}")
            return None
        except Exception as exc:
            if attempt < attempts - 1:
                time.sleep(1.0)
                continue
            log(f"RSS error: {type(exc).__name__}: {exc}")
            return None
    return None


def original_url(link: str) -> str:
    """Bing wraps the real article URL in an apiclick redirect."""
    try:
        parts = urllib.parse.urlsplit(link)
        if "bing.com" in parts.netloc:
            params = urllib.parse.parse_qs(parts.query)
            if params.get("url"):
                return params["url"][0]
    except Exception:
        pass
    return link


def parse_rss(root: ET.Element, company: dict, cutoff: datetime) -> list[dict]:
    items: list[dict] = []
    for element in root.findall("./channel/item"):
        title = html.unescape((element.findtext("title") or "").strip())
        link = original_url((element.findtext("link") or "").strip())
        if not title or not link:
            continue
        pub_raw = element.findtext("pubDate") or ""
        try:
            published = parsedate_to_datetime(pub_raw)
            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)
            if published < cutoff:
                continue
            published_str = published.astimezone(timezone.utc).isoformat(timespec="seconds")
        except Exception:
            published_str = pub_raw
        source_node = element.find("source")
        source = (source_node.text or "").strip() if source_node is not None else ""
        if not source:
            for child in element:
                if child.tag.endswith("Source") and child.text:
                    source = child.text.strip()
                    break
        if source and title.endswith(" - " + source):
            title = title[: -(len(source) + 3)].strip()
        items.append({
            "company": company["category"],
            "company_key": company["key"],
            "title": title,
            "url": link,
            "source": source or "News RSS",
            "published": published_str,
            "key": item_key(title, link),
        })
    return items


def fetch_company(company: dict, max_age_days: int) -> list[dict]:
    locale = company.get("locale", "en-US")
    if locale.startswith("zh"):
        locale_params = "hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    else:
        locale_params = "hl=en-US&gl=US&ceid=US:en"
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    items: list[dict] = []
    seen: set[str] = set()
    for query in company.get("queries", [company["category"]]):
        feeds = [
            "https://www.bing.com/news/search?q=" + urllib.parse.quote(query) + "&format=rss",
            "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&" + locale_params,
        ]
        feed_items: list[dict] = []
        for feed in feeds:
            root = fetch_rss(feed)
            if root is None:
                continue
            feed_items = parse_rss(root, company, cutoff)
            if feed_items:
                break
        for item in feed_items:
            if item["key"] in seen:
                continue
            seen.add(item["key"])
            items.append(item)
    return items


def fetch_all(companies: list[dict], max_age_days: int) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(fetch_company, c, max_age_days): c for c in companies}
        for future in as_completed(futures):
            company = futures[future]
            try:
                result[company["key"]] = future.result()
            except Exception as exc:
                log(f"fetch failed for {company['category']}: {exc}")
                result[company["key"]] = []
    return result


def select_items(
    fetched: dict[str, list[dict]],
    companies: list[dict],
    state: dict,
    per_run: int,
    extra_seen: set[str],
) -> list[dict]:
    seen_keys = set(state.get("posted_keys", [])) | extra_seen
    seen_urls = set(state.get("posted_urls", []))
    picked: list[dict] = []
    picked_keys: set[str] = set()
    picked_urls: set[str] = set()
    total_companies = len(companies)

    def take(company: dict) -> bool:
        for item in fetched.get(company["key"], []):
            if item["key"] in seen_keys or item["key"] in picked_keys:
                continue
            url = normalize_url(item["url"])
            if url in seen_urls or url in picked_urls:
                continue
            picked.append(item)
            picked_keys.add(item["key"])
            picked_urls.add(url)
            return True
        return False

    start = int(state.get("rotation_index", 0)) % total_companies
    for offset in range(total_companies):
        if len(picked) >= per_run:
            break
        take(companies[(start + offset) % total_companies])
    if len(picked) < per_run:
        for company in companies:
            if len(picked) >= per_run:
                break
            for _ in range(per_run - len(picked)):
                if not take(company):
                    break
    state["rotation_index"] = (start + len(picked)) % total_companies
    return picked


def discussion_body(item: dict) -> str:
    return (
        f"**Automated news digest — {html.escape(item['company'])}**\n\n"
        f"- **Headline:** {item['title']}\n"
        f"- **Source:** {item['source']}\n"
        f"- **Published:** {item['published']}\n"
        f"- **Original link:** {item['url']}\n\n"
        "Posted by FAI's automated news feed. This is a pointer to a third-party "
        "report, not a verified claim by FAI. Check the original source before "
        "citing it; accountability evidence belongs in [RESEARCH/](https://github.com/FAI-Union/FckAI/tree/main/RESEARCH).\n"
    )


def publish(item: dict, category_id: str, repo_id: str, token: str) -> str:
    mutation = """mutation($repositoryId:ID!,$categoryId:ID!,$title:String!,$body:String!){
      createDiscussion(input:{repositoryId:$repositoryId,categoryId:$categoryId,title:$title,body:$body}){
        discussion { number url title }
      }
    }"""
    title = f"[News] {item['title']}"[:240]
    data = graphql(mutation, {
        "repositoryId": repo_id,
        "categoryId": category_id,
        "title": title,
        "body": discussion_body(item),
    }, token)
    return data["createDiscussion"]["discussion"]["url"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["setup", "run", "dry-run"])
    parser.add_argument("--per-run", type=int, default=3)
    parser.add_argument("--max-age-days", type=int, default=7)
    args = parser.parse_args()

    companies = json.loads(COMPANIES_FILE.read_text(encoding="utf-8"))
    token = get_token()

    if args.mode == "setup":
        if not token:
            log("WAITING_PAT: no GitHub token found; set GH_PAT or write .workbuddy/secrets/github_pat.txt")
            return 2
        return 0 if verify_categories(token) == 0 else 2

    state = load_state()
    fetched = fetch_all(companies, args.max_age_days)
    counts = ", ".join(f"{c['category']}={len(fetched.get(c['key'], []))}" for c in companies)
    log(f"fetched candidates: {counts}")

    extra_seen: set[str] = set()
    if token:
        try:
            extra_seen = existing_discussion_titles(token)
        except RuntimeError as exc:
            log(f"warning: could not read existing discussions: {exc}")
    picked = select_items(fetched, companies, state, args.per_run, extra_seen)
    if not picked:
        log("no new items to publish")
        return 0

    if args.mode == "dry-run":
        for item in picked:
            log(f"DRY-RUN -> {item['company']}: {item['title']} | {item['url']}")
        return 0

    if not token:
        log("WAITING_PAT: no GitHub token found; set GH_PAT or write .workbuddy/secrets/github_pat.txt")
        return 2

    repo_id, categories = repo_context(token)
    missing = [c["category"] for c in companies if c["category"] not in categories]
    if missing:
        log("missing categories: " + ", ".join(missing) + " (run: setup)")
        return 2

    published = 0
    for item in picked:
        try:
            url = publish(item, categories[item["company"]]["id"], repo_id, token)
            state.setdefault("posted_keys", []).append(item["key"])
            state.setdefault("posted_urls", []).append(normalize_url(item["url"]))
            published += 1
            log(f"published -> {item['company']}: {url}")
        except RuntimeError as exc:
            log(f"publish failed for {item['company']}: {exc}")
    save_state(state)
    log(f"done: {published}/{len(picked)} published")
    return 0 if published == len(picked) else 1


if __name__ == "__main__":
    sys.exit(main())
