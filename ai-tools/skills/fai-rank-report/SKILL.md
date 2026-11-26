---
name: fai-rank-report
description: Measure and report FAI's GitHub search rank using scripts/track_search_rank.py, compare against docs/search-baseline.md and previous rank snapshots, and write docs/rank-YYYY-MM-DD.md. Use for weekly rank checks, search visibility reports, or questions about which queries improved.
agent_created: true
---

# FAI search-rank reporting

## Overview

Search ranking is a weekly, offline-analysed metric. The tracker queries the GitHub REST repository search API for eight fixed queries; reports are stored in `docs/rank-YYYY-MM-DD.md` and compared with the 2026-11-26 baseline. Search visibility is a lagging indicator of genuine adoption, not a target to game.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py rank-snapshot          # offline baseline vs stored reports
GITHUB_TOKEN=<token> python scripts/track_search_rank.py --format markdown > docs/rank-YYYY-MM-DD.md
python scripts/track_search_rank.py --help              # delay / per-page / format / queries
```

MCP equivalents: `rank_snapshot`, `repo_status`, `search_repo`, `validate_links`, `repo_overview`.

## Procedure

1. Run `rank_snapshot` first to understand the existing baseline and the latest stored measurements. Report only real movements.
2. To refresh measurements, run `scripts/track_search_rank.py` with a `GITHUB_TOKEN` environment variable when available; without a token the API is rate-limited. Use `--delay` to avoid throttling. Never write a token into a tracked file, command log or report.
3. Save the raw script output as `docs/rank-YYYY-MM-DD.md`. Then add a short interpretation section: what moved, what held, and whether the change is causal (index refresh/metadata) or merely noise.
4. Compare against the documented targets: `AI accountability evidence` ≤10 after 4 weeks and ≤3 after 8 weeks; `topic:ai-accountability` ≤20 then ≤10; the two long-tail #1 positions retained at least one external citation by week 8.
5. Run `validate_links` after adding a report, and record the measurement in `CHANGELOG.md` if it is part of a monthly review.
6. Head terms `AI accountability` and `AI ethics` are not realistic targets at 0 stars. Say so plainly instead of inventing progress.

## Rules

- GitHub search does **not** support exact phrase matching; a rank only confirms token relevance. Never describe it as a phrase ranking.
- No keyword stuffing, no star exchanges, no buying stars, no automated self-promotion. Distribution copy must not mention ranking or SEO.
- A rank improvement is a byproduct of sourced content and real participation, never proof of adoption by itself.

## References

- `scripts/track_search_rank.py`, `docs/search-baseline.md`, `docs/rank-2026-11-26-after.md`, `RUNBOOK.md#5-weekly-metrics-review`
- Full toolkit documentation: `ai-tools/README.md`
