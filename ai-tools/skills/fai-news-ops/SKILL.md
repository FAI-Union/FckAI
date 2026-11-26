---
name: fai-news-ops
description: Operate and troubleshoot the hourly FAI AI-company news bot — inspect dedupe state, preview unseen headlines with dry-run, publish a batch, and handle Discussion category or PAT problems safely. Use for news_bot.py, companies.json, AI company Discussions, or the hourly news automation.
agent_created: true
---

# FAI AI-company news operations

## Overview

`scripts/ai-news/news_bot.py` fetches Bing News RSS first (resolving the original article URL) with Google News as fallback, deduplicates by normalised title and URL against local state and the 100 most recent Discussions, then publishes three items per run, rotating across ten company categories. Posts carry a disclaimer: FAI does not verify third-party claims.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py news-status
python D:/Git/FAI/ai-tools/cli.py news-dry-run --per-run 3
python scripts/ai-news/news_bot.py setup          # only verifies the 10 categories
python scripts/ai-news/news_bot.py dry-run --per-run 3
python scripts/ai-news/news_bot.py run --per-run 1  # publishes; human-triggered only
```

MCP equivalents: `news_status`, `news_dry_run`, `repo_status`, `search_repo`.

## Procedure

1. `news_status` first: confirm state exists, note dedupe key/URL counts, rotation index and the sanitised log tail. State and logs live in gitignored `.workbuddy/ai-news/`.
2. Preview with `news_dry_run` (or the direct `dry-run` command). Verify three unseen items in distinct categories and that each URL points to the original article, not an aggregator redirect.
3. Publishing is triggered by the existing WorkBuddy automation (hourly, `python scripts/ai-news/news_bot.py run --per-run 3`) or explicitly by a human. Do not silently change cadence, batch size or company list; `companies.json` is the canonical configuration.
4. After a publish, re-check `news_status` and confirm the Discussion appears in the matching category. Update nothing in tracked files unless the script/config itself changes.

## Known constraints and traps

- GitHub has **no API or CLI** to create Discussion categories. `setup` only validates them. New categories must be created in the Discussions web UI; never claim this was automated.
- The fine-grained PAT lives in gitignored `.workbuddy/secrets/github_pat.txt` and must have **Discussions: Read and write** for the `FAI-Union` organisation. Never print it, copy it into a tracked file, or include it in a report or screenshot.
- The bot reads `GH_PAT` or the local secret file; a token with only Metadata/Administration cannot post. The local file must be user-only (ACL on Windows, `chmod 600` on POSIX); the bot warns or refuses when permissions are too broad.
- RSS fields are single-line sanitised and rendered as inline code/autolinks; links must be http(s). Do not reintroduce raw headline/source/URL interpolation into `discussion_body()`.
- Duplicates are keyed by title and URL and by up to 2,000 recent Discussion titles. Do not reset `state.json` to force a repost.
- Third-party headlines are not FAI-verified evidence. Never move a news item into `RESEARCH/` without a fresh original-source review.

## References

- `scripts/ai-news/news_bot.py`, `scripts/ai-news/companies.json`, `RUNBOOK.md#26-ai-company-news-feed-hourly`
- Full toolkit documentation: `ai-tools/README.md`
