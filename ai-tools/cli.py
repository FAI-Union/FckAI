#!/usr/bin/env python3
"""Command-line front end for the FAI AI toolkit.

Every MCP tool has an equivalent CLI command, so skills still work when the
MCP server is not registered:

  python D:/Git/FAI/ai-tools/cli.py evidence-validate EV-2026-001
  python D:/Git/FAI/ai-tools/cli.py links
  python D:/Git/FAI/ai-tools/cli.py preflight --title "..." --files RESEARCH/EV-2026-022.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import core as fai  # noqa: E402


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FAI repository AI toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("repo-overview", help="mission, docs, counts, human gates")
    sub.add_parser("repo-status", help="branch, commit, dirty tree, content counts")
    sub.add_parser("runbook-backlog", help="pending RUNBOOK items")
    sub.add_parser("validate-links", help="broken relative Markdown links")
    sub.add_parser("evidence-chain", help="EV -> POLICY/CAMPAIGNS cross-check")
    sub.add_parser("translation-status", help="LANGUAGES.md + locales summary")
    sub.add_parser("rank-snapshot", help="offline baseline vs rank reports")
    sub.add_parser("news-status", help="sanitised news bot state and log tail")

    p = sub.add_parser("search", help="search tracked text files")
    p.add_argument("query")
    p.add_argument("--path-filter")
    p.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("evidence-list", help="list evidence cards")
    p.add_argument("--tag")
    p.add_argument("--query")

    p = sub.add_parser("evidence-get", help="read one evidence card")
    p.add_argument("evidence_id")

    p = sub.add_parser("evidence-validate", help="validate a card by ID")
    p.add_argument("evidence_id")

    p = sub.add_parser("evidence-next-id", help="next unused EV ID")

    p = sub.add_parser("evidence-scaffold", help="generate a card draft (stdout only)")
    for name in ("claim_en", "claim_zh", "source_url", "publisher", "excerpt", "caveats"):
        p.add_argument(f"--{name.replace('_', '-')}", required=True)
    p.add_argument("--tags", nargs="*")
    p.add_argument("--evidence-id")
    p.add_argument("--verified-by", default="web-research-agent")
    p.add_argument("--publication-date", default="")
    p.add_argument("--report", default="")

    p = sub.add_parser("translation-validate", help="check a translation PR")
    p.add_argument("tag")
    p.add_argument("--title")
    p.add_argument("--files", nargs="*")

    p = sub.add_parser("news-dry-run", help="preview unseen headlines without publishing")
    p.add_argument("--per-run", type=int, default=3)
    p.add_argument("--timeout", type=int, default=90)

    p = sub.add_parser("preflight", help="simulate PR/issue checks")
    p.add_argument("--title", default="")
    p.add_argument("--body", default="")
    p.add_argument("--files", nargs="*")
    p.add_argument("--author-type", default="")
    p.add_argument("--account-age-days", type=int)
    p.add_argument("--followers", type=int)
    p.add_argument("--public-repos", type=int)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cmd = args.command
    simple = {
        "repo-overview": fai.repo_overview,
        "repo-status": fai.repo_status,
        "runbook-backlog": fai.runbook_backlog,
        "validate-links": fai.validate_links,
        "evidence-chain": fai.check_evidence_chain,
        "translation-status": fai.translation_status,
        "rank-snapshot": fai.rank_snapshot,
        "news-status": fai.news_status,
        "evidence-next-id": fai.next_evidence_id,
    }
    if cmd in simple:
        _emit(simple[cmd]())
        return 0
    if cmd == "search":
        _emit(fai.search_repo(args.query, args.path_filter, args.limit))
    elif cmd == "evidence-list":
        _emit(fai.list_evidence(args.tag, args.query))
    elif cmd == "evidence-get":
        _emit(fai.get_evidence(args.evidence_id))
    elif cmd == "evidence-validate":
        _emit(fai.validate_evidence(args.evidence_id))
    elif cmd == "evidence-scaffold":
        _emit(
            fai.scaffold_evidence(
                claim_en=args.claim_en,
                claim_zh=args.claim_zh,
                source_url=args.source_url,
                publisher=args.publisher,
                excerpt=args.excerpt,
                caveats=args.caveats,
                tags=args.tags,
                evidence_id=args.evidence_id,
                verified_by=args.verified_by,
                publication_date=args.publication_date,
                report=args.report,
            )
        )
    elif cmd == "translation-validate":
        _emit(fai.validate_translation(args.tag, args.title, args.files))
    elif cmd == "news-dry-run":
        _emit(fai.news_dry_run(args.per_run, args.timeout))
    elif cmd == "preflight":
        _emit(
            fai.preflight_submission(
                title=args.title,
                body=args.body,
                files=args.files,
                author_type=args.author_type,
                account_age_days=args.account_age_days,
                followers=args.followers,
                public_repos=args.public_repos,
            )
        )
    else:  # pragma: no cover - argparse enforces the choices
        raise SystemExit(f"unknown command: {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
