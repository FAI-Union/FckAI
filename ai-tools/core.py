"""FAI repository AI toolkit.

Pure standard-library helpers shared by the CLI and the MCP server.
All paths are resolved relative to the repository root (FAI_REPO_ROOT override).
Nothing in this module reads .workbuddy/secrets or writes to tracked files.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
import sys
import urllib.parse
from collections import deque
from pathlib import Path
from typing import Any, Iterable

EV_ID_RE = re.compile(r"EV-\d{4}-\d{3}")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SECRET_RE = re.compile(
    r"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}"
    r"|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,})"
)
SENSITIVE_ENV = ("GH_PAT", "GITHUB_TOKEN", "FAI_GITHUB_PAT")
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
CORE_DOCS = ("README.md", "MANIFESTO.md", "GOVERNANCE.md", "CODE_OF_CONDUCT.md")
TEXT_SUFFIXES = {".md", ".html", ".json", ".yml", ".yaml", ".py", ".txt", ".xml"}
SKIP_DIRS = {".git", ".workbuddy", "__pycache__", "node_modules", "dist", ".venv"}


def root() -> Path:
    override = os.environ.get("FAI_REPO_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[1]


def _read(path: Path) -> str:
    return _ensure_readable(path).read_text(encoding="utf-8", errors="replace")


def redact(text: object) -> str:
    """Never echo token-like strings or live secret env values into output."""
    result = SECRET_RE.sub("[REDACTED]", str(text) if text is not None else "")
    for name in SENSITIVE_ENV:
        value = os.environ.get(name, "").strip()
        if len(value) >= 8:
            result = result.replace(value, "[REDACTED]")
    return result


def _is_symlink_path(path: Path) -> bool:
    """Detect symlinks in the path itself or any parent up to the repo root."""
    base = root()
    for candidate in (path, *path.parents):
        if candidate == base:
            break
        try:
            if candidate.is_symlink():
                return True
        except OSError:
            return True
    return False


def _ensure_readable(path: Path) -> Path:
    """Resolve a path only if it is a regular file inside the repository."""
    if _is_symlink_path(path):
        raise ValueError("symlink paths are not readable")
    try:
        resolved = path.resolve()
    except (OSError, RuntimeError) as exc:
        raise ValueError("path cannot be resolved") from exc
    if not resolved.is_relative_to(root()):
        raise ValueError("path escapes the repository root")
    if not resolved.is_file():
        raise FileNotFoundError(f"not a regular file: {path}")
    return resolved


def _run_git(args: list[str]) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(root()),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        if proc.returncode != 0:
            return ""
        return proc.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def tracked_files(suffixes: Iterable[str] | None = None) -> list[Path]:
    """List tracked files via git, with a filesystem fallback."""
    wanted = set(suffixes) if suffixes is not None else TEXT_SUFFIXES
    raw = _run_git(["ls-files", "-z"])
    if raw:
        candidates = [root() / p for p in raw.split("\0") if p]
    else:
        candidates = [
            p
            for p in root().rglob("*")
            if p.is_file() and not (set(p.relative_to(root()).parts) & SKIP_DIRS)
        ]
    files: list[Path] = []
    for path in candidates:
        if path.suffix.lower() not in wanted or not path.exists():
            continue
        try:
            if not path.resolve().is_relative_to(root()):
                continue
        except (OSError, RuntimeError):
            continue
        if _is_symlink_path(path):
            continue
        files.append(path)
    return sorted(files)


# --------------------------------------------------------------------------
# Markdown helpers
# --------------------------------------------------------------------------
def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    meta: dict[str, Any] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        else:
            value = value.strip("\"'")
        meta[key] = value
    return meta, "\n".join(lines[end + 1 :])


def sections(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            if current is not None:
                result[current] = "\n".join(buffer).strip()
            current = match.group(1)
            buffer = []
        elif current is not None:
            buffer.append(line)
    if current is not None:
        result[current] = "\n".join(buffer).strip()
    return result


def find_section(parts: dict[str, str], *keywords: str) -> str:
    for heading, body in parts.items():
        if any(k.lower() in heading.lower() for k in keywords):
            return body
    return ""


def parse_tables(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in _read(path).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


# --------------------------------------------------------------------------
# Evidence cards
# --------------------------------------------------------------------------
def evidence_files() -> list[Path]:
    return sorted((root() / "RESEARCH").glob("EV-*.md"))


def _card(path: Path) -> dict[str, Any]:
    text = _read(path)
    meta, body = parse_frontmatter(text)
    parts = sections(body)
    source = find_section(parts, "Source", "来源")
    urls = URL_RE.findall(source)
    h1 = next((l for l in body.splitlines() if l.startswith("# ")), "")
    return {
        "id": str(meta.get("id", path.stem)),
        "path": path.relative_to(root()).as_posix(),
        "title": h1.lstrip("# ").strip(),
        "status": meta.get("status", ""),
        "verified_by": meta.get("verified_by", ""),
        "last_reviewed": meta.get("last_reviewed", ""),
        "tags": meta.get("tags", []) if isinstance(meta.get("tags"), list) else [],
        "source_url": urls[0] if urls else "",
        "meta": meta,
        "parts": parts,
        "text": text,
    }


def list_evidence(tag: str | None = None, query: str | None = None) -> dict[str, Any]:
    cards = [_card(p) for p in evidence_files()]
    if tag:
        cards = [c for c in cards if tag.lower() in [str(t).lower() for t in c["tags"]]]
    if query:
        needle = query.lower()
        cards = [
            c
            for c in cards
            if needle in (c["title"] + " " + c["text"]).lower()
        ]
    return {
        "count": len(cards),
        "cards": [
            {k: c[k] for k in ("id", "title", "status", "tags", "source_url", "path")}
            for c in cards
        ],
    }


def get_evidence(evidence_id: str) -> dict[str, Any]:
    if not EV_ID_RE.fullmatch(evidence_id or ""):
        raise ValueError("evidence_id must look like EV-2026-001")
    path = root() / "RESEARCH" / f"{evidence_id}.md"
    if not path.is_file():
        raise FileNotFoundError(f"unknown evidence card: {evidence_id}")
    card = _card(path)
    return {
        "id": card["id"],
        "title": card["title"],
        "frontmatter": card["meta"],
        "source_url": card["source_url"],
        "sections": card["parts"],
        "text": card["text"],
    }


def validate_evidence(evidence_id: str | None = None, text: str | None = None) -> dict[str, Any]:
    """Validate a card on disk or a draft supplied as text."""
    errors: list[str] = []
    warnings: list[str] = []
    if text is not None:
        card_text = text
        path = None
        meta, body = parse_frontmatter(card_text)
        card_id = str(meta.get("id", ""))
    else:
        if not evidence_id or not EV_ID_RE.fullmatch(evidence_id):
            raise ValueError("provide evidence_id (EV-YYYY-NNN) or text")
        path = root() / "RESEARCH" / f"{evidence_id}.md"
        if not path.is_file():
            raise FileNotFoundError(f"unknown evidence card: {evidence_id}")
        card_text = _read(path)
        meta, body = parse_frontmatter(card_text)
        card_id = evidence_id

    if not EV_ID_RE.fullmatch(card_id):
        errors.append("frontmatter.id missing or malformed (expected EV-YYYY-NNN)")
    for key in ("status", "verified_by", "last_reviewed", "tags"):
        if not meta.get(key):
            errors.append(f"frontmatter.{key} is required")
    reviewed = str(meta.get("last_reviewed", ""))
    if reviewed and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed):
        errors.append("frontmatter.last_reviewed must be YYYY-MM-DD")
    if not isinstance(meta.get("tags"), list) or not meta.get("tags"):
        errors.append("frontmatter.tags must be a non-empty list")

    parts = sections(body)
    claim = find_section(parts, "Claim", "主张")
    source = find_section(parts, "Source", "来源")
    excerpt = find_section(parts, "Excerpt", "引述")
    caveats = find_section(parts, "Caveats", "说明")
    used_by = find_section(parts, "Used by", "引用方")
    h1 = next((l for l in body.splitlines() if l.startswith("# ")), "")
    if not h1.strip("# "):
        errors.append("missing H1 heading")
    elif card_id and card_id not in h1:
        errors.append("H1 must begin with the evidence ID")
    for name, value in (
        ("Claim", claim),
        ("Source", source),
        ("Excerpt", excerpt),
        ("Caveats", caveats),
        ("Used by", used_by),
    ):
        if not value:
            errors.append(f"missing section: ## {name}")
    if claim and not re.search(r"[\u4e00-\u9fff]", claim):
        errors.append("Claim must include both English and Chinese")
    if source and not URL_RE.search(source):
        errors.append("Source must contain an http(s) URL")
    if source and "Publisher" not in source:
        warnings.append("Source has no 'Publisher' line")
    if source and not re.search(r"\b(19|20)\d{2}-\d{2}-\d{2}\b", source):
        warnings.append("Source has no publication date")
    if excerpt and not re.search(r"^\s*>", excerpt, re.MULTILINE):
        errors.append("Excerpt must contain a verbatim blockquote line")
    if caveats and (len(caveats) < 20 or "<!--" in caveats):
        errors.append("Caveats must describe scope/uncertainty, not be a placeholder")
    if used_by and "Pending" in used_by:
        warnings.append("Used by is still pending — link a policy or campaign when one cites this card")

    if path is not None:
        all_ids = [EV_ID_RE.search(p.name).group(0) for p in evidence_files() if EV_ID_RE.search(p.name)]
        if all_ids.count(card_id) > 1:
            errors.append("duplicate evidence ID in RESEARCH/")
        index = _read(root() / "RESEARCH" / "README.md")
        if f"({card_id}.md)" not in index and f"[{card_id}]" not in index:
            warnings.append("card is not listed in RESEARCH/README.md index")

    return {
        "id": card_id,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "path": path.relative_to(root()).as_posix() if path else None,
    }


def next_evidence_id() -> dict[str, Any]:
    numbers = []
    for path in evidence_files():
        match = EV_ID_RE.search(path.name)
        if match:
            numbers.append(int(match.group(0).split("-")[-1]))
    year = _dt.date.today().year
    existing = [int(m.group(1)) for m in re.finditer(r"EV-(\d{4})-", _read(root() / "RESEARCH" / "README.md"))]
    if existing:
        year = max(max(existing), year)
    next_num = (max(numbers) if numbers else 0) + 1
    candidate = f"EV-{year}-{next_num:03d}"
    return {"id": candidate, "existing_cards": len(numbers)}


def _single_line(name: str, value: object, limit: int = 500) -> str:
    text = str(value if value is not None else "").strip()
    if "\n" in text or "\r" in text or CONTROL_RE.search(text):
        raise ValueError(f"{name} must be a single line without control characters")
    return text[:limit]


def _https_url(value: object) -> str:
    text = _single_line("source_url", value, 1000)
    try:
        parts = urllib.parse.urlsplit(text)
    except ValueError as exc:
        raise ValueError("source_url must be an https URL") from exc
    if parts.scheme.lower() != "https" or not parts.netloc:
        raise ValueError("source_url must be an https URL")
    if any(ch in text for ch in "<> \"'"):
        raise ValueError("source_url contains unsafe characters")
    return text


def scaffold_evidence(
    claim_en: str,
    claim_zh: str,
    source_url: str,
    publisher: str,
    excerpt: str,
    caveats: str,
    tags: list[str] | None = None,
    evidence_id: str | None = None,
    verified_by: str = "web-research-agent",
    publication_date: str = "",
    report: str = "",
) -> dict[str, Any]:
    """Return a ready-to-review card draft; never writes files."""
    card_id = _single_line("evidence_id", evidence_id or next_evidence_id()["id"], 64)
    if not EV_ID_RE.fullmatch(card_id):
        raise ValueError("evidence_id must look like EV-2026-001")
    safe_source = _https_url(source_url)
    claim_en = _single_line("claim_en", claim_en)
    claim_zh = _single_line("claim_zh", claim_zh)
    publisher = _single_line("publisher", publisher, 200)
    verified_by = _single_line("verified_by", verified_by, 100)
    publication_date = _single_line("publication_date", publication_date, 40)
    report = _single_line("report", report, 200)

    if tags is None:
        tags = ["uncategorised"]
    if not isinstance(tags, list) or not tags or len(tags) > 20:
        raise ValueError("tags must be a non-empty list of at most 20 strings")
    safe_tags = []
    for tag in tags:
        item = _single_line("tag", tag, 60)
        if any(ch in item for ch in ",[]"):
            raise ValueError("tags must not contain commas or brackets")
        safe_tags.append(item)
    tag_str = ", ".join(safe_tags)

    excerpt_lines = "\n".join(
        f"> {CONTROL_RE.sub(' ', line).strip()}" for line in excerpt.splitlines() if line.strip()
    ) or "> TODO: paste a short verbatim quote from the original source."
    caveat_lines = "\n".join(
        f"- {CONTROL_RE.sub(' ', line).strip()}" for line in caveats.splitlines() if line.strip()
    )
    if not caveat_lines:
        caveat_lines = "- TODO: state scope, uncertainty, and whether this is a projection or a measurement."
    today = _dt.date.today().isoformat()
    report_line = f"- Report: *{report}*\n" if report else ""
    date_line = f"- Publication date: {publication_date}\n" if publication_date else ""
    draft = (
        "---\n"
        f"id: {card_id}\n"
        "status: verified\n"
        f"verified_by: {verified_by}\n"
        f"last_reviewed: {today}\n"
        f"tags: [{tag_str}]\n"
        "---\n\n"
        f"# {card_id} — {claim_en}\n\n"
        "## Claim / 主张\n\n"
        f"{claim_en}\n\n"
        f"{claim_zh}\n\n"
        "## Source / 来源\n\n"
        f"- Original: [Source title]({safe_source})\n"
        f"- Publisher: {publisher}\n"
        f"{report_line}{date_line}\n"
        "## Excerpt / 引述\n\n"
        f"{excerpt_lines}\n\n"
        "## Caveats / 说明\n\n"
        f"{caveat_lines}\n\n"
        "## Used by / 引用方\n\n"
        "Pending — link this ID from any policy claim or campaign that uses it.\n"
    )
    check = validate_evidence(text=draft)
    return {"id": card_id, "draft": draft, "validation": check}


def check_evidence_chain() -> dict[str, Any]:
    """Cross-check EV -> POLICY/CAMPAIGNS references and Used by backlinks."""
    refs: dict[str, list[str]] = {}
    for path in tracked_files({".md"}):
        rel = path.relative_to(root()).as_posix()
        if not (rel.startswith("POLICY/") or rel.startswith("CAMPAIGNS/")):
            continue
        for found in set(EV_ID_RE.findall(_read(path))):
            refs.setdefault(found, []).append(rel)
    known = {EV_ID_RE.search(p.name).group(0) for p in evidence_files() if EV_ID_RE.search(p.name)}
    dangling = sorted({i for i in refs if i not in known})
    missing_backlink: list[dict[str, Any]] = []
    for path in evidence_files():
        card = _card(path)
        used = find_section(card["parts"], "Used by", "引用方").lower()
        for doc in refs.get(card["id"], []):
            name = Path(doc).name.lower()
            if name not in used and doc.lower() not in used:
                missing_backlink.append({"evidence_id": card["id"], "referenced_by": doc})
    return {
        "evidence_cards": len(known),
        "referenced_cards": len([i for i in refs if i in known]),
        "dangling_ev_references": dangling,
        "missing_used_by_backlinks": missing_backlink,
        "ok": not dangling and not missing_backlink,
    }


# --------------------------------------------------------------------------
# Link lint
# --------------------------------------------------------------------------
def validate_links() -> dict[str, Any]:
    broken: list[dict[str, Any]] = []
    checked = 0
    for path in tracked_files({".md"}):
        rel = path.relative_to(root()).as_posix()
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            for target in MD_LINK_RE.findall(line):
                if re.match(r"^(?:https?://|mailto:|//|#|\{\{)", target):
                    continue
                checked += 1
                file_part = target.split("#", 1)[0]
                if not file_part:
                    continue
                candidate = path.parent / file_part
                if Path(file_part).is_absolute() or re.match(r"^[A-Za-z]:[\\/]", file_part):
                    broken.append(
                        {"file": rel, "line": lineno, "target": target, "reason": "absolute links are not allowed"}
                    )
                    continue
                try:
                    resolved = candidate.resolve()
                except (OSError, RuntimeError):
                    resolved = candidate
                if not resolved.is_relative_to(root()):
                    broken.append(
                        {"file": rel, "line": lineno, "target": target, "reason": "target escapes the repository root"}
                    )
                    continue
                if _is_symlink_path(candidate):
                    broken.append(
                        {"file": rel, "line": lineno, "target": target, "reason": "symlink targets are not allowed"}
                    )
                    continue
                if not resolved.exists():
                    broken.append(
                        {"file": rel, "line": lineno, "target": target, "reason": "target does not exist"}
                    )
    return {"checked_links": checked, "broken": broken, "ok": not broken}


# --------------------------------------------------------------------------
# Translations
# --------------------------------------------------------------------------
def translation_status() -> dict[str, Any]:
    path = root() / "LANGUAGES.md"
    rows: list[dict[str, Any]] = []
    for cells in parse_tables(path):
        if len(cells) >= 8 and cells[1].startswith("`"):
            tag = cells[1].strip("`")
            rows.append(
                {
                    "language": cells[0],
                    "tag": tag,
                    "docs": dict(zip(CORE_DOCS, cells[2:6])),
                    "maintainer": cells[6],
                    "last_verified": cells[7],
                }
            )
    status: dict[str, Any] = {}
    if "## Priority languages" in _read(path):
        block = _read(path).split("## Priority languages", 1)[1].split("\n## ", 1)[0]
        status["priority_tags"] = re.findall(r"`([A-Za-z-]+(?:-[A-Za-z]+)?)`", block)
    locale_dirs = sorted(p.name for p in (root() / "locales").iterdir() if p.is_dir())
    claimed = {r["tag"] for r in rows if r["tag"] != "en"}
    status.update(
        {
            "rows": rows,
            "locale_dirs": locale_dirs,
            "claimed_but_missing_dir": sorted(claimed - set(locale_dirs)),
            "dir_without_status_row": sorted(set(locale_dirs) - claimed),
            "not_yet_started_priority": [
                t for t in status.get("priority_tags", []) if t not in claimed
            ],
        }
    )
    return status


def validate_translation(
    tag: str, title: str | None = None, changed_files: list[str] | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    changed = changed_files or []
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", tag or ""):
        errors.append("tag must be a BCP 47 code such as es or pt-BR")
    if title is not None:
        match = re.match(r"^i18n\(([^)]+)\):\s+\S", title)
        if not match:
            errors.append("PR title must be: i18n(<tag>): add <Language> translation")
        elif match.group(1) != tag:
            errors.append(f"PR title tag {match.group(1)!r} does not match {tag!r}")
    if changed and "LANGUAGES.md" not in changed:
        errors.append("translation PR must update LANGUAGES.md")
    folder = root() / "locales" / tag
    for doc in CORE_DOCS:
        path = folder / doc
        if changed and f"locales/{tag}/{doc}" not in changed:
            continue
        if not path.is_file():
            errors.append(f"missing locales/{tag}/{doc}")
            continue
        body = _read(path)
        if f"../../{doc}" not in body and f"../../README.md" not in body:
            warnings.append(f"locales/{tag}/{doc} has no link back to the English original")
    return {"tag": tag, "ok": not errors, "errors": errors, "warnings": warnings}


# --------------------------------------------------------------------------
# Runbook / repo / ranking / news / preflight
# --------------------------------------------------------------------------
def runbook_backlog() -> dict[str, Any]:
    path = root() / "RUNBOOK.md"
    section = ""
    items: list[dict[str, Any]] = []
    for line in _read(path).splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        symbols = [s for s in ("⬜", "🟡", "⏳", "⏸") if s in line]
        if symbols and not line.startswith("Status legend"):
            items.append(
                {"section": section, "status": symbols[0], "text": line.strip(" -|")[:240]}
            )
    counts: dict[str, int] = {}
    for item in items:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    return {"counts": counts, "items": items}


def repo_status() -> dict[str, Any]:
    cards = evidence_files()
    policies = sorted((root() / "POLICY").glob("PP-*.md"))
    campaigns = sorted((root() / "CAMPAIGNS").glob("*.md"))
    locales = sorted(p.name for p in (root() / "locales").iterdir() if p.is_dir())
    dirty = _run_git(["status", "--porcelain"]).splitlines()
    return {
        "branch": _run_git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "last_commit": _run_git(["log", "-1", "--format=%h %cs %s"]),
        "working_tree_dirty": bool(dirty),
        "dirty_entries": dirty[:20],
        "counts": {
            "evidence_cards": len(cards),
            "policies": len(policies),
            "campaign_docs": len(campaigns),
            "locale_dirs": len(locales),
            "tracked_files": len(_run_git(["ls-files"]).splitlines()),
        },
        "runbook_pending": runbook_backlog()["counts"],
    }


def rank_snapshot() -> dict[str, Any]:
    baseline: dict[str, str] = {}
    for cells in parse_tables(root() / "docs" / "search-baseline.md"):
        if len(cells) >= 3 and cells[0].startswith("`") and cells[2]:
            baseline[cells[0].strip("`")] = cells[2]
    current: dict[str, str] = {}
    files = sorted((root() / "docs").glob("rank-*.md"))
    for path in files:
        for cells in parse_tables(path):
            if len(cells) >= 3 and cells[0].startswith("`") and not cells[0].startswith("`Baseline"):
                rank = cells[2].split()[0].strip("*")
                current[cells[0].strip("`")] = rank
                if cells[1]:
                    baseline[cells[0].strip("`")] = cells[1].split()[0].strip("*")
    targets = [
        {"query": q, "baseline": baseline.get(q), "current": current.get(q)}
        for q in sorted(set(baseline) | set(current))
    ]
    return {
        "files": [p.name for p in files],
        "rows": targets,
        "note": "GitHub search does not support exact phrase matching; treat these as token-rank observations.",
    }


def news_status(tail: int = 12) -> dict[str, Any]:
    state_path = root() / ".workbuddy" / "ai-news" / "state.json"
    log_path = root() / ".workbuddy" / "ai-news" / "bot.log"
    result: dict[str, Any] = {"state_present": state_path.is_file()}
    if state_path.is_file():
        try:
            state = json.loads(_read(state_path))
            result.update(
                {
                    "posted_titles": len(state.get("posted_keys", [])),
                    "posted_urls": len(state.get("posted_urls", [])),
                    "rotation_index": state.get("rotation_index"),
                }
            )
        except (ValueError, OSError) as exc:
            result["state_error"] = str(exc)
    if log_path.is_file():
        count = max(1, min(int(tail), 200))
        try:
            with _ensure_readable(log_path).open("r", encoding="utf-8", errors="replace") as fh:
                lines = deque(fh, maxlen=count)
            result["log_tail"] = [redact(line.rstrip("\r\n"))[:240] for line in lines]
        except (OSError, ValueError) as exc:
            result["log_error"] = redact(str(exc))
    return result


def news_dry_run(per_run: int = 3, timeout: int = 90) -> dict[str, Any]:
    per_run = max(1, min(int(per_run), 20))
    timeout = max(1, min(int(timeout), 300))
    script = root() / "scripts" / "ai-news" / "news_bot.py"
    if not script.is_file():
        raise FileNotFoundError("scripts/ai-news/news_bot.py not found")
    try:
        proc = subprocess.run(
            [sys.executable, str(script), "dry-run", "--per-run", str(per_run)],
            cwd=str(root()),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        output = redact(proc.stdout + proc.stderr)
        return {
            "returncode": proc.returncode,
            "ok": proc.returncode == 0,
            "output": output[-4000:],
        }
    except subprocess.SubprocessError as exc:
        return {"ok": False, "error": redact(str(exc))}


def preflight_submission(
    title: str = "",
    body: str = "",
    files: list[str] | None = None,
    author_type: str = "",
    account_age_days: int | None = None,
    followers: int | None = None,
    public_repos: int | None = None,
) -> dict[str, Any]:
    """Local mirror of the two GitHub Actions checks. Advisory only: never auto-reject humans."""
    changed = files or []
    reasons: list[str] = []
    decision = "pass"
    content_paths = [p for p in changed if p.startswith(("RESEARCH/", "POLICY/", "CAMPAIGNS/"))]
    if content_paths and not URL_RE.search(body or ""):
        reasons.append("needs-source: PRs touching RESEARCH/POLICY/CAMPAIGNS need a URL in the body")
        decision = "block"
    translation_paths = [p for p in changed if p.startswith("locales/") or p == "LANGUAGES.md"]
    if translation_paths:
        match = re.match(r"^i18n\(([^)]+)\):\s+\S", title or "")
        if not match:
            reasons.append("translation PR title must be `i18n(<tag>): add <Language> translation`")
            decision = "block"
        elif not any(p.startswith(f"locales/{match.group(1)}/") for p in changed):
            reasons.append(f"title tag {match.group(1)} has no matching locales/ path")
            decision = "block"
        if "LANGUAGES.md" not in changed:
            reasons.append("translation PR must update LANGUAGES.md")
            decision = "block"
    added_urls = len(URL_RE.findall(body or ""))
    if added_urls > 12:
        reasons.append(f"too many links in body ({added_urls} > 12)")
        decision = "block"
    if author_type.lower() == "bot" or (title + body).lower().count("[bot]"):
        reasons.append("bot account: triage workflow closes these; no human content decision")
        decision = "bot"
    elif (
        account_age_days is not None
        and account_age_days < 7
        and followers == 0
        and public_repos == 0
    ):
        reasons.append("new account with no followers/repos: add needs-review label only")
        decision = "needs-review"
    return {
        "decision": decision,
        "reasons": reasons or ["no checks triggered"],
        "human_override_required": True,
        "note": "Advisory preflight only. The workflows mark; only maintainers may reject a human submission.",
    }


def repo_overview() -> dict[str, Any]:
    readme = _read(root() / "README.md")
    headline = next((l for l in readme.splitlines() if l.startswith("# ")), "")
    return {
        "repository": "FAI-Union/FckAI",
        "headline": headline.lstrip("# "),
        "rule": "every factual claim must carry a source; unsourced content gets needs-source",
        "canonical_docs": [
            "README.md",
            "MANIFESTO.md",
            "GOVERNANCE.md",
            "CODE_OF_CONDUCT.md",
            "RUNBOOK.md",
            "CONTRIBUTING.md",
            "LANGUAGES.md",
        ],
        "data_dirs": ["RESEARCH/", "POLICY/", "CAMPAIGNS/", "locales/", "docs/", "scripts/ai-news/"],
        "counts": repo_status()["counts"],
        "human_gates": ["publishing campaigns", "admin-only GitHub settings", "source verification", "merging PRs"],
        "toolkit_docs": "ai-tools/README.md",
    }


def search_repo(query: str, path_filter: str | None = None, limit: int = 50) -> dict[str, Any]:
    if not query:
        raise ValueError("query must not be empty")
    limit = max(1, min(int(limit), 200))
    matches: list[dict[str, Any]] = []
    needle = query.lower()
    for path in tracked_files():
        rel = path.relative_to(root()).as_posix()
        if path_filter and path_filter.lower() not in rel.lower():
            continue
        for lineno, line in enumerate(_read(path).splitlines(), 1):
            if needle in line.lower():
                matches.append(
                    {"file": rel, "line": lineno, "text": redact(line.strip())[:300]}
                )
                if len(matches) >= limit:
                    return {"query": query, "truncated": True, "matches": matches}
    return {"query": query, "truncated": False, "matches": matches}
