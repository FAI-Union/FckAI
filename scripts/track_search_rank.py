#!/usr/bin/env python3
"""Track where FAI-Union/FckAI ranks for a fixed set of GitHub repository searches.

Usage:
    python scripts/track_search_rank.py
    python scripts/track_search_rank.py --delay 7 --format json
    GITHUB_TOKEN=... python scripts/track_search_rank.py   # higher rate limit

No third-party dependencies. Results are printed to stdout; redirect to a file
to keep a weekly baseline, e.g. python scripts/track_search_rank.py > rank-2026-11-27.md
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request

TARGET = "FAI-Union/FckAI"
API = "https://api.github.com/search/repositories"

QUERIES = [
    ("head: AI accountability", "AI accountability"),
    ("head: AI ethics", "AI ethics"),
    ("topic: ai-accountability", "topic:ai-accountability"),
    ("mid: AI accountability evidence", "AI accountability evidence"),
    ("long: training data consent evidence", "training data consent evidence"),
    ("long: deepfake accountability evidence", "deepfake accountability evidence"),
    ("long: human-first AI", "human-first AI"),
    ("brand: FckAI in:name", "FckAI in:name"),
]


def fetch(query, per_page):
    url = f"{API}?q={urllib.parse.quote(query)}&per_page={per_page}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "fai-search-rank-tracker",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def measure(query, per_page):
    data = fetch(query, per_page)
    items = data.get("items", [])
    rank = next(
        (i + 1 for i, item in enumerate(items) if item.get("full_name") == TARGET),
        None,
    )
    return {
        "query": query,
        "total_count": data.get("total_count"),
        "rank": rank,
        "in_top_n": rank is not None,
        "per_page": per_page,
    }


def render_markdown(rows):
    lines = [
        "# GitHub search rank snapshot",
        "",
        f"Target: `{TARGET}`",
        "",
        "| Query | total_count | Rank | Status |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in rows:
        rank = row["rank"] if row["rank"] is not None else f">{row['per_page']}"
        status = "ok" if row["in_top_n"] else "needs work"
        lines.append(
            f"| `{row['query']}` | {row['total_count']} | {rank} | {status} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delay", type=float, default=6.0, help="seconds between requests (default 6 to respect unauthenticated rate limits)")
    parser.add_argument("--per-page", type=int, default=100, choices=[30, 100])
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--queries", help="comma-separated search queries to run instead of the default set")
    args = parser.parse_args()

    pairs = QUERIES
    if args.queries:
        pairs = [("custom", q.strip()) for q in args.queries.split(",") if q.strip()]

    rows = []
    for index, (label, query) in enumerate(pairs):
        try:
            row = measure(query, args.per_page)
            row["label"] = label
        except Exception as exc:  # network, rate limit, or API error
            row = {
                "label": label,
                "query": query,
                "total_count": None,
                "rank": None,
                "in_top_n": False,
                "per_page": args.per_page,
                "error": str(exc),
            }
        rows.append(row)
        if index < len(pairs) - 1 and args.delay > 0:
            time.sleep(args.delay)

    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
