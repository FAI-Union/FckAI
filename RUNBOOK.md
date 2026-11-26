# FAI Runbook

Maintainer operating manual for `FAI-Union/FckAI`. This is the single source of truth for **how we maintain the project and how we grow it**. Strategy comes from the growth review on 2026-11-26; every item has a status and a concrete acceptance test.

Status legend: ✅ done · 🟡 in progress · ⬜ todo · ⏸ manual (needs a human at github.com) · 🚫 deliberate no

Last updated: 2026-11-26

---

## 0. Snapshot and north star

Baseline taken 2026-11-26 (day one of the repo):

| Metric | Value |
| --- | --- |
| Stars / forks / issues | 0 / 0 / 0 |
| Commits | 5 |
| Repos in org | 1 |
| Maintainer followers | 0 |

This is a **cold start**, not an algorithm problem. For an advocacy/archive repo, star growth is a byproduct of a working loop:

> sourced evidence → policy proposal → public campaign → distribution → new contributors → more evidence

**North star is not stars.** It is: 10 active contributors, 30 verifiable evidence cards, 5 languages, 1 external citation. Stars follow.

🚫 **Never**: buy stars, join star-exchange groups, use unsourced claims, attack individuals, or impersonate an official body. The only asset this project has is trust.

---

## 1. Diagnostics and fixes

| # | Finding | Action | Acceptance test | Status |
| --- | --- | --- | --- | --- |
| 1.1 | Discussions linked everywhere but disabled | Enable Discussions via API; keep links in README / GOVERNANCE | `has_discussions: true`, no 404 on `/discussions` | ✅ |
| 1.2 | 75-language table dominated the README first screen | Collapse into 10 priority languages + link to LANGUAGES.md | README first 40 lines contain the value proposition and 30-second path | ✅ |
| 1.3 | "FckAI" reads as anti-AI at first glance | Put "Human-First AI Accountability" in the first line and repo description | First screen states what we are **for** before what we oppose | ✅ |
| 1.4 | Pages / social preview / topics / org profile missing | Enable Pages from `/docs`; set topics; upload banner; create org profile README | Landing page live, topics 20/20, preview image set, org profile visible | ✅ verified 2026-11-26 15:40 — see [docs/manual-setup.md](docs/manual-setup.md) |
| 1.5 | No protection against bot/low-effort submissions | Two Actions workflows + interaction limits + branch protection | Mock tests 10/10 pass; `existing_users`; protected `main` | ✅ |

---

## 2. Maintenance: turn governance into executable process

### 2.1 Three-layer evidence chain

- **RESEARCH/** — one evidence card per file. Mandatory fields: `Claim`, `Source URL`, `Published date`, `Excerpt`, `Caveats`, `Verified by`, `Evidence ID`.
- **POLICY/** — every proposal must reference at least one `Evidence ID` (e.g. `EV-2026-001`).
- **CAMPAIGNS/** — every action must link to the Discussion or Issue that authorised it.
- PRs without a source URL fail `content-validation`; unsourced claims get `needs-source` and are not used in decisions.

Acceptance test: a PR touching `RESEARCH/`, `POLICY/` or `CAMPAIGNS/` with no URL in the body must fail the check. ✅ (local mock verified)

### 2.2 Roles and permissions

`GOVERNANCE.md` defines Contributor / Maintainer / Coordinator. Mirror that in GitHub teams:

| Team | Purpose |
| --- | --- |
| `core` | Repo admin, final escalation, CODEOWNERS target |
| `maintainers` | Merge PRs, apply labels, review content |
| `translators` | Claim and review language files |

- "Consensus in 7 days" → label `consensus-7d` + a checklist item in the proposal issue template.
- Coordinator rotation → public milestone with the month and the coordinator's handle.
- ≥2 maintainers at all times; a maintainer inactive for 3 months drops to contributor (already in GOVERNANCE.md).

Status: ⬜ create teams and wire CODEOWNERS to `@FAI-Union/core`.

### 2.3 Translations: 10, not 75

Priority batch: `es / fr / de / ja / ko / pt-BR / ar / hi / ru / zh-TW`.

- One `[i18n]` issue to claim, one PR to deliver, title `i18n(<tag>): add <Language> translation`.
- `content-validation` enforces the title format and a `LANGUAGES.md` update.
- Mark the last verified date in `LANGUAGES.md`; stale translations are flagged, not silently trusted.
- Other languages stay "welcome, no minimum speaker count" but get no maintainer bandwidth.

Status: ✅ README collapsed; ⬜ LANGUAGES.md priority section + issue templates.

### 2.4 Fixed cadence

| Rhythm | Deliverable |
| --- | --- |
| Weekly | 1 sourced evidence card |
| Every 2 weeks | 1 Discussion on a live policy question |
| Monthly | 1 brief + `CHANGELOG.md` entry + metrics review |

A dead repo is worse than a small repo: consistency is the trust signal.

Status: ⬜ create templates and `CHANGELOG.md`.

### 2.5 Contributor experience

- First response ≤72h; every PR gets an explicit next step.
- Rejections include a reason and a path to resubmit.
- Merge → public thanks + @ the contributor.
- `good first issue` only for 30-minute tasks: "add a source", "translate one evidence card".

Status: 🟡 automated checks documented in CONTRIBUTING.md; 5 seeded `good first issue` items (#3–#7) exist and are verified; ⬜ first-response SLA.

### 2.6 AI-company news feed (hourly)

- Ten company categories now exist in [Discussions](https://github.com/FAI-Union/FckAI/discussions/categories): OpenAI, Anthropic, Google DeepMind, Meta AI, xAI, Mistral AI, DeepSeek, Alibaba Qwen, ByteDance Doubao, Moonshot AI.
- `scripts/ai-news/news_bot.py` pulls Bing News RSS first (resolving the original article URL) with Google News as fallback, dedupes by normalized title + URL against `.workbuddy/ai-news/state.json` and the 100 most recent Discussions, then publishes **3 items per run**, rotating across companies so each post lands in its own category.
- Every post carries the headline, original link and a disclaimer that FAI does not verify third-party claims. No unsourced claims are introduced (red line in README).
- The WorkBuddy automation `FAI AI 公司新闻同步到 Discussions` runs hourly. It reads the token from `.workbuddy/secrets/github_pat.txt` (gitignored); that fine-grained PAT needs **Discussions: read/write**. `python scripts/ai-news/news_bot.py setup` only verifies categories — GitHub exposes no category-creation API, so new categories must be added in the Discussions UI.
- Acceptance test: `python scripts/ai-news/news_bot.py dry-run --per-run 3` shows three unseen items in distinct categories; `run --per-run 1` creates a Discussion visible in the matching category and updates the dedupe state. Verified 2026-11-26 (discussions #8–#10, #12).

Status: ✅ categories created, bot and automation live; ⬜ consider grouping the ten categories under one Discussion section.

### 2.7 Repository AI toolkit (MCP + skills)

- `ai-tools/` holds a standard-library Python MCP server (17 tools), an equivalent CLI, seven WorkBuddy skills and a test suite. The canonical sources are tracked; local MCP registration and installed skills are generated copies (`python ai-tools/install.py`).
- Coverage: evidence cards and index, EV → POLICY/CAMPAIGNS chain, relative links, translations, RUNBOOK backlog, rank snapshots, news-bot state/dry-run and PR preflight. Tools are read-only or produce in-memory drafts; no tool reads or prints the news-bot token.
- Red lines are unchanged: source verification, publication, admin-only GitHub settings and PR merges stay human actions. Bot/new-account triage only labels; humans are never auto-rejected.
- Acceptance test: `python -m unittest discover -s ai-tools/tests -v` passes (10 tests, including an MCP stdio handshake); `python ai-tools/install.py --dry-run` is idempotent; `validate-links` reports zero broken relative links.

Status: ✅ implemented 2026-11-26; ⬜ each contributor registers the `fai` MCP server in their own client after restart.

### 2.8 Security hardening for automation and AI tools

- `ai-tools/` is versioned in git; both workflows pin `actions/github-script` to commit `f28e40c7f34bde8b3046d885e986cb6290c5673b` (v7). `pull_request_target` is split into a PR-only job with no checkout and an explicit "never execute PR code" guard; `issues` and PR write scopes are separated.
- The news bot sanitises every untrusted RSS field before publishing: control characters and newlines are removed, fields are rendered as inline code/autolinks, non-http(s) links are rejected, DTD/entity declarations and RSS responses over 5 MiB are refused. Duplicate scanning covers up to 2,000 recent Discussions.
- The PAT file is user-only (Windows ACL tightened 2026-11-26; POSIX mode 0600 enforced at runtime). Logs and tool output redact token patterns plus live `GH_PAT`/`GITHUB_TOKEN` values.
- Toolkit file reads skip symlinks and paths outside `FAI_REPO_ROOT`; link lint rejects absolute/escaping/symlink targets. MCP input is validated against `inputSchema` with numeric bounds; `install.py` uses `sys.executable` and atomically replaces `mcp.json`.
- `content-validation.yml` reads the full head/base blobs of all added **and modified** Markdown files and counts the URL delta, so truncated/omitted patches cannot bypass the 12-link threshold; unreadable blobs fail closed.
- Follow-up review 2026-11-26: DTD/entity detection covers the entire (≤5 MiB) RSS response, not just the first 8 KiB; MCP rejects non-object `params`, non-string tool names and over-long string/array arguments instead of crashing; see [docs/security-review-2026-11-26.md](docs/security-review-2026-11-26.md).
- Acceptance test: `python -m unittest discover -s ai-tools/tests -v` passes **18 tests** (including frontmatter-injection, path-escape, redaction, RSS-sanitisation, DTD-offset, malformed-MCP-message and argument-bound regressions); `python scripts/ai-news/news_bot.py dry-run --per-run 1` publishes nothing.

Status: ✅ implemented 2026-11-26; ⬜ re-run `install.py` and restart the client after merging so contributors pick up the absolute-interpreter MCP entry and the hardened dispatcher.

---

## 3. Growth: cold start and distribution

### 3.1 Fix conversion first

README first screen must answer: who we are / why now / what you can do in 5 minutes. Then a 30-second path: **Star → claim a language → submit one sourced evidence card**.

Status: ✅

### 3.2 Metadata

- Description with searchable terms: AI accountability, training-data consent, deepfake, energy disclosure.
- 10–20 topics.
- 1280×640 social preview generated from `assets/fai-banner.png`.
- Pages landing page: manifesto + one hard evidence + participation CTA; all external links point there.

Status: ✅ all verified 15:40 — homepage and Pages live; canonical, OG/Twitter, hreflang, JSON-LD, `robots.txt` and `sitemap.xml` return 200; `/docs/zh-CN/` live; topics 20/20; social preview uploaded; org profile live. One cosmetic cleanup remains: the applied description duplicates one clause — see [docs/manual-setup.md](docs/manual-setup.md#verification--2026-11-26-1540-gmt8). Search impact is tracked in [docs/rank-2026-11-26-after.md](docs/rank-2026-11-26-after.md).

### 3.3 Real cold start

Trending ranks **relative growth rate**, not total stars. Invite 20–30 people who genuinely agree to participate in the same week. Never buy stars. 🚫 star exchanges.

Status: ⬜ human action, owner.

### 3.4 Tailored distribution

Channels: Hacker News, Reddit r/technology / r/opensource, Lobste.rs, V2EX, 知乎, AI-ethics newsletters, creator-rights groups, university AI-ethics courses.

Each channel gets: **one concrete pain + one verifiable evidence + one immediate action**. Never paste the same copy everywhere.

Status: 🟡 wave 1 is packed and ready-to-paste in [CAMPAIGNS/WAVE-1.md](CAMPAIGNS/WAVE-1.md) — HN, Lobste.rs, Reddit r/technology, V2EX and 知乎, with post URLs, spacing and a pre-flight checklist. Copy rationale stays in [CAMPAIGNS/DISTRIBUTION.md](CAMPAIGNS/DISTRIBUTION.md); wave 2 (newsletter, courses, awesome lists) needs named contacts. Nothing has been posted — posting remains a human action.

### 3.5 Citable artefacts

Turn evidence into shareable cards / data tables (e.g. "AI energy disclosure tracker"). Publish a monthly brief. Other people citing our data is the most durable star source for a content repo.

Status: ✅ first citable artefact is live — 21 sourced evidence cards with a canonical index at [RESEARCH/README.md](RESEARCH/README.md). Monthly brief still ⬜.

### 3.6 Newsjacking with discipline

Within 24–48h of a major model release, copyright case, or bill: publish a sourced position piece. No unverified claims, no personal attacks. Red lines in README are binding.

Status: ⬜ ongoing.

### 3.7 Contributor flywheel

`good first issue` → claim → merge → public thanks → contributor brings their own network. Track repeat-contributor rate, not just star count.

Status: ⬜ seed 3–5 good-first issues after templates land.

---

## 4. Channel matrix (copy/paste starters)

| Channel | Angle | CTA |
| --- | --- | --- |
| Hacker News (Show HN) | "We archive sourced evidence of AI's real-world costs" | Read the manifesto, submit one sourced card |
| Reddit r/technology | One specific harm + one source | Join the Discussion thread |
| Lobste.rs | Technical accountability / provenance | Review `RESEARCH/` |
| V2EX / 知乎 | 中文语境：训练数据同意权与就业冲击 | 认领一个中文证据卡 |
| AI-ethics newsletter | Monthly brief excerpt | Subscribe via repo Watch |
| University courses | Ready-made evidence cards for seminars | Use `RESEARCH/` as course material |

---

## 5. Weekly metrics review

Record in `CHANGELOG.md`:

- Stars, forks, watchers, open issues/PRs
- Evidence cards, proposals, campaigns
- Contributors (new / returning)
- Traffic sources from GitHub Insights
- First-response time and repeat-contributor rate

Conversion (visit → star → contribute) matters more than a single-day star spike.

Search ranking is measured separately with [scripts/track_search_rank.py](scripts/track_search_rank.py) against the [2026-11-26 baseline](docs/search-baseline.md). Run it weekly, save the output as `docs/rank-YYYY-MM-DD.md`, and record only real movements — the head terms `AI accountability` and `AI ethics` are not realistic targets until we have genuine stars and external citations.

---

## 6. Execution log

| Date | Action | Result |
| --- | --- | --- |
| 2026-11-26 | Initial repo, i18n structure, 75-language list | pushed |
| 2026-11-26 | Bot triage + content validation workflows, CODEOWNERS | `de22907`, 10/10 mock pass |
| 2026-11-26 | Discussions, signoff, Actions write, interaction limits, branch protection | verified via REST |
| 2026-11-26 | Runbook created; assets, README, metadata, templates applied | this commit |
| 2026-11-26 | P0/P1 discoverability pass: keyword-first README, Pages SEO + zh-CN landing page, 20 new sourced evidence cards, distribution kit, rank tracker, manual setup checklist | files in `RESEARCH/`, `docs/`, `scripts/`, `CAMPAIGNS/`; remote metadata still admin-gated |
| 2026-11-26 | Wave 1 publication pack prepared; newsletter copy corrected to cite the demand card (EV-2026-001) instead of the emissions card | `CAMPAIGNS/WAVE-1.md`; not posted |
| 2026-11-26 | Ten AI-company Discussion categories created in UI; hourly news bot + dedupe state + WorkBuddy automation wired; PAT upgraded to Discussions read/write | `scripts/ai-news/`, discussions #8–#10 and #12 |
| 2026-11-26 | Repository AI toolkit: MCP server + CLI + 7 skills + tests, installed locally; fixed one broken rank-report link and three missing `Used by` backlinks found by the new checks | `ai-tools/`, `RESEARCH/` EV-001/008/015, `docs/rank-2026-11-26-after.md` |
