---
name: fai-repo-audit
description: Run a read-only health audit of the FAI repository — broken links, evidence-chain consistency, card schema, translation status, RUNBOOK backlog, git state, news bot state and search-rank reports. Use for routine maintenance checks, pre-release verification, or when asked what is broken or pending in the repo.
agent_created: true
---

# FAI repository audit

## Overview

One-pass, offline verification of the repository's content invariants. Produces a compact findings table rather than changing files. Fix only unambiguous defects (for example a wrong relative path) and say what was changed.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py repo-status
python D:/Git/FAI/ai-tools/cli.py validate-links
python D:/Git/FAI/ai-tools/cli.py evidence-chain
python D:/Git/FAI/ai-tools/cli.py translation-status
python D:/Git/FAI/ai-tools/cli.py runbook-backlog
python D:/Git/FAI/ai-tools/cli.py rank-snapshot
python D:/Git/FAI/ai-tools/cli.py news-status
python D:/Git/FAI/ai-tools/cli.py evidence-validate EV-2026-001  # repeat for every card
```

MCP equivalents: `repo_status`, `validate_links`, `check_evidence_chain`, `translation_status`, `runbook_backlog`, `rank_snapshot`, `news_status`, `validate_evidence`, `repo_overview`, `search_repo`.

## Audit procedure

1. `repo_status`: record branch, last commit and whether the working tree is dirty. Never overwrite unrelated local changes.
2. `validate_links`: all relative Markdown links must resolve. Report each broken link as `file:line → target`; fix only when the intended target is unambiguous.
3. Validate every card with `validate_evidence`, then run `check_evidence_chain`. Errors are blockers; `Used by is still pending` is a warning unless a policy or campaign cites the card.
4. `translation_status`: check that claimed languages have a `locales/<tag>/` directory, priority tags are tracked, and no directory lacks a status row.
5. `runbook_backlog`: list ⬜/🟡/⏳/⏸ items with their section. Distinguish real work from deliberately deferred or human-gated items.
6. `rank_snapshot`: compare baseline with stored rank reports. Never present a rank as proof of exact-phrase matching — GitHub search does not support phrase matching.
7. `news_status`: report dedupe counts and the sanitised log tail. Never read, print or copy `.workbuddy/secrets/github_pat.txt`.
8. Close with a table: `Check | Result | Evidence (file:line or tool output) | Next action`. Mark human gates explicitly.

## Rules

- Read-only by default. Any change must be small, explainable and followed by a re-run of the affected check.
- New maintenance actions must be recorded in `RUNBOOK.md` and `CHANGELOG.md` (project convention).
- Do not report an unverified claim as verified; do not claim a campaign was published or a GitHub admin setting was applied without evidence.

## References

- `RUNBOOK.md`, `CHANGELOG.md`, `RESEARCH/README.md`, `LANGUAGES.md`, `docs/search-baseline.md`
- Full toolkit documentation: `ai-tools/README.md`
