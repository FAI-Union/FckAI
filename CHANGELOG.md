# Changelog

Monthly review record for the FAI project. See [RUNBOOK.md](RUNBOOK.md#5-weekly-metrics-review) for the metrics we track.

## 2026-11

- Launched `FAI-Union/FckAI` with English-default i18n structure and zh-CN translation.
- Added bot triage and content-validation workflows; local mock tests 10/10 pass.
- Enabled Discussions, web commit signoff, Actions write permissions, interaction limits (`existing_users`) and `main` branch protection.
- Published RUNBOOK.md; added FAI logo, banner, avatar and favicons.
- Onboarded first sourced evidence card `EV-2026-001` (IEA energy projection) and first policy draft `PP-2026-001`.
- Reframed the README around "Human-First AI Accountability" with a 30-second participation path; collapsed 75-language table to 10 priority languages.
- Created GitHub Pages landing page at `/docs` (https://fai-union.github.io/FckAI/).
- Created `core`, `maintainers`, `translators` teams; set 18 topics and a searchable description; seeded 5 language-claim good-first issues (#3–#7).
- Fixed the over-broad ruleset that had blocked all branch creation; it now protects only `main`, with PR merges allowed.
- P0/P1 discoverability pass: README lead and evidence index rewritten around searchable phrases; `/docs` landing page fixed (image 404) and given canonical, OG/Twitter, hreflang, JSON-LD, `robots.txt`, `sitemap.xml` plus a zh-CN page.
- Evidence archive expanded from 1 to 21 sourced cards across copyright/consent, jobs, energy and deepfakes; each card has tags, a verbatim quote and a `Caveats` section. See [RESEARCH/README.md](RESEARCH/README.md).
- Added [CAMPAIGNS/DISTRIBUTION.md](CAMPAIGNS/DISTRIBUTION.md) with channel-specific outreach drafts that are ready but not posted; added [scripts/track_search_rank.py](scripts/track_search_rank.py) and a [search baseline](docs/search-baseline.md).
- Documented admin-only steps (description, 20 topics, social preview, org profile) in [docs/manual-setup.md](docs/manual-setup.md); the automation token has no admin/issue-write scope.
- 15:40 verification: admin steps applied and checked (topics 20/20, custom social preview, org profile). Fixed 5 broken relative links in evidence cards and index (`bd1b60c`). Measured rank movement in [docs/rank-2026-11-26-after.md](docs/rank-2026-11-26-after.md): `AI accountability evidence` 24 → 4, `topic:ai-accountability` 42 → 6; long-tail #1 positions held; head terms unchanged. The applied description duplicates one clause — cleanup suggested in manual-setup.md.
- Wave 1 distribution pack in [CAMPAIGNS/WAVE-1.md](CAMPAIGNS/WAVE-1.md): ready-to-paste copy for HN, Lobste.rs, Reddit r/technology, V2EX and 知乎, with post URLs and a one-channel-per-day order. **Not posted.** Corrected the newsletter draft to cite EV-2026-001 (power demand) instead of EV-2026-015 (emissions), which had been described as an energy-cost figure.
- Added 10 AI-company Discussion categories (OpenAI, Anthropic, Google DeepMind, Meta AI, xAI, Mistral AI, DeepSeek, Alibaba Qwen, ByteDance Doubao, Moonshot AI) plus an hourly news bot in [scripts/ai-news/](scripts/ai-news/) that fetches sourced headlines, dedupes them and publishes three per run to the matching category. GitHub has no API to create categories, so the one-time setup was done in the Discussions UI; the PAT used by the bot now has Discussions read/write. First posts: discussions #8–#10, #12.
- Added [ai-tools/](ai-tools/README.md): a standard-library MCP server (17 tools) plus equivalent CLI, seven WorkBuddy skills and 10 regression tests covering the evidence schema, EV → POLICY/CAMPAIGNS chain, Markdown links, translations, RUNBOOK backlog, rank reports, news-bot state and PR preflight. Tools are read-only/draft-only and never expose the bot token. The tool's link and chain checks found and fixed one broken relative link in the rank report and three missing `Used by` backlinks on EV-2026-001/008/015.
- Security hardening pass (2026-11-26): pinned GitHub Actions to a commit SHA, split `pull_request_target` permissions and forbade PR-code checkout; sanitised news-RSS output and capped feed size; tightened the PAT file ACL and generalised secret redaction; blocked symlink/root-escape reads and frontmatter injection; added MCP schema/bounds checks, atomic MCP config writes and full-blob link counting. Regression suite now has 15 tests.
- Second security review (2026-11-26): fixed four residual gaps — malformed MCP messages no longer crash the stdio server, DTD detection covers the full RSS response, the CI link-farm check counts added URLs from head/base blobs for modified files and fails closed, and MCP string/array arguments are bounded. Suite now has 18 tests; full findings in [docs/security-review-2026-11-26.md](docs/security-review-2026-11-26.md).

### Metrics snapshot (2026-11-26, after P0/P1)

| Metric | Value |
| --- | --- |
| Stars / forks | 0 / 0 |
| Evidence cards | 21 |
| External sources cited | 20 |
| Policy proposals | 1 |
| Translations | en, zh-CN (plus zh-CN landing page) |
| Contributors | 1 |
| Search rank: `AI accountability evidence` | 4 (was 24 at baseline) |
| Search rank: `topic:ai-accountability` | 6 (was 42) |
| Search rank: two long-tail queries | #1 each (held) |
