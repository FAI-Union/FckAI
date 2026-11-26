# FAI AI toolkit

Repository-specific AI tooling for `FAI-Union/FckAI`. The canonical source lives here and is tracked in git; the local MCP registration and installed skills are generated copies.

- **MCP server** (`mcp_server.py`): 17 read-only/draft-only tools over stdio JSON-RPC.
- **CLI** (`cli.py`): every tool is also available as a command, so skills work without MCP.
- **Skills** (`skills/`): seven WorkBuddy skills encoding the repository's workflows and red lines.
- **Deps**: Python 3 standard library only. No network call except the explicit news dry-run. No secret is read or printed by any tool.

## Install locally

```bash
python D:/Git/FAI/ai-tools/install.py            # merge MCP config + copy skills
python D:/Git/FAI/ai-tools/install.py --dry-run  # preview only
```

- MCP config: `~/.workbuddy/mcp.json` (existing entries are preserved). Server name: `fai`.
- Skills: `D:/Git/FAI/.workbuddy/skills/` (gitignored project scope; canonical copies are in `ai-tools/skills/`).
- Restart WorkBuddy after first registration.

To point the tools at another checkout, set `FAI_REPO_ROOT` in the environment (or in the MCP entry's `env`).

## Verify

```bash
python -m unittest discover -s D:/Git/FAI/ai-tools/tests -v
```

Tests cover the 21-card schema, link lint, evidence chain, translation checks, preflight rules, secret redaction, rank diff, an MCP stdio handshake (`initialize` → `tools/list` → `tools/call`) and security regressions (draft injection, path escape, argument bounds, RSS sanitisation).

## MCP tools and CLI equivalents

| MCP tool | CLI command | Purpose |
| --- | --- | --- |
| `repo_overview` | `repo-overview` | Mission, canonical docs, counts, human gates |
| `repo_status` | `repo-status` | Branch, last commit, dirty tree, content counts |
| `search_repo` | `search <query> [--path-filter P]` | Full-text search over tracked text files |
| `list_evidence` | `evidence-list [--tag T] [--query Q]` | List cards with source URL and tags |
| `get_evidence` | `evidence-get <EV-YYYY-NNN>` | Read a full card |
| `validate_evidence` | `evidence-validate <EV-YYYY-NNN>` | Schema/source/quote/caveat/index check |
| `next_evidence_id` | `evidence-next-id` | Next unused ID |
| `scaffold_evidence` | `evidence-scaffold --...` | Generate a valid card draft (stdout only) |
| `check_evidence_chain` | `evidence-chain` | EV ↔ POLICY/CAMPAIGNS cross-check |
| `validate_links` | `validate-links` | Broken relative Markdown links |
| `translation_status` | `translation-status` | LANGUAGES.md rows, locales, priority gaps |
| `validate_translation` | `translation-validate <tag> [--title T] [--files ...]` | i18n PR rules |
| `runbook_backlog` | `runbook-backlog` | Pending RUNBOOK items |
| `rank_snapshot` | `rank-snapshot` | Baseline vs stored rank reports (offline) |
| `news_status` | `news-status` | Sanitised news-bot state and log tail |
| `news_dry_run` | `news-dry-run [--per-run 3]` | Preview unseen headlines (network) |
| `preflight_submission` | `preflight --title ... --body ... --files ...` | Simulate CI triage/validation |

All JSON output is machine-readable; the server sends one JSON object per stdout line and logs nothing to stdout.

## Skills

| Skill | Triggers |
| --- | --- |
| `fai-evidence` | Add/validate evidence cards, update the research index |
| `fai-policy-campaign` | Draft policies, campaigns and channel copy; check consensus and red lines |
| `fai-translation` | Add or review a locale, keep LANGUAGES.md in sync |
| `fai-repo-audit` | Routine read-only repo health check |
| `fai-news-ops` | News bot state, dry-run, publishing and PAT/category troubleshooting |
| `fai-rank-report` | Weekly rank measurement and baseline comparison |
| `fai-contribution-preflight` | Pre-PR triage simulation and explanation of labels |

Each skill loads only when its description matches; detailed rules stay in the repository docs it points to, not duplicated inside the skill.

## Safety boundaries

- Tools never write tracked files. `scaffold_evidence` returns a draft; a human/agent writes it explicitly.
- No tool reads `.workbuddy/secrets/github_pat.txt`; log output is redacted for token patterns and live `GH_PAT`/`GITHUB_TOKEN` values.
- File reads skip symlinks and paths outside the repository; `validate_links` rejects absolute/escaping/symlink targets.
- MCP calls are checked against `inputSchema` with numeric bounds; CLI helpers apply the same caps.
- `install.py` uses the current `sys.executable` and writes `mcp.json` atomically.
- Publishing campaigns, changing GitHub admin settings, verifying a source and merging PRs stay human actions.
- Bot/new-account handling mirrors the workflows: labels and comments only; humans are never auto-rejected.
- GitHub has no API to create Discussion categories; `news_bot.py setup` only validates them.

## Maintenance

When adding a tool or skill, update this file, `RUNBOOK.md` and `CHANGELOG.md`, add a test, rerun the suite and rerun `install.py`.
