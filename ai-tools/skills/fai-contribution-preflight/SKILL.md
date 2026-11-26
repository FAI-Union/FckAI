---
name: fai-contribution-preflight
description: Simulate FAI's contribution-triage and content-validation checks before opening or reviewing an issue/PR: source URL requirement, i18n title format, link limit, bot/new-account labels. Use for PR preflight, triaging a new issue, or explaining why a submission was labelled needs-source or needs-review.
agent_created: true
---

# FAI contribution preflight

## Overview

Mirrors `.github/workflows/contribution-triage.yml` and `.github/workflows/content-validation.yml` locally so contributors can fix problems before CI runs. The workflows **mark and comment**; only a maintainer may reject a human submission.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py preflight \
  --title "evidence: new source" \
  --body "Source: https://example.org/report" \
  --files RESEARCH/EV-2026-022.md
```

MCP equivalents: `preflight_submission`, `validate_evidence`, `validate_translation`, `validate_links`, `search_repo`, `get_evidence`.

## Checks

1. **Source URL** — any PR touching `RESEARCH/`, `POLICY/` or `CAMPAIGNS/` must contain an `http(s)` URL in the body; otherwise the decision is `block` with reason `needs-source`.
2. **Translation** — a PR touching `locales/` or `LANGUAGES.md` needs a title `i18n(<tag>): add <Language> translation`, a matching `locales/<tag>/` path and a `LANGUAGES.md` update. Then run `validate_translation` with the tag and changed files.
3. **Link limit** — more than 12 URLs in a PR body fails content validation; flag link-farm patterns.
4. **Bot accounts** — accounts of type Bot or with `[bot]` in the login are closed by the triage workflow. This is not a human-content judgement.
5. **New accounts** — account age under 7 days with zero followers and zero public repos gets `needs-review`, not rejection.
6. **Evidence schema** — for a new card, run `validate_evidence` on the draft before preflight. `preflight_submission` checks the PR envelope; `validate_evidence` checks the card's content.

## Response rules

- Report the decision (`pass`, `needs-review`, `block`, `bot`), each reason and the exact fix. Never auto-reject a human.
- Respect the 72-hour first-response commitment: every PR gets a clear next step.
- Use the issue templates (`evidence.md`, `proposal.md`, `translation.md`) and direct blank issues to Discussions via `.github/ISSUE_TEMPLATE/config.yml`.
- Do not create labels, close issues or post comments on GitHub as part of a preflight; only a maintainer or the workflow may do that.

## References

- `.github/workflows/contribution-triage.yml`, `.github/workflows/content-validation.yml`, `CONTRIBUTING.md`, `GOVERNANCE.md`
- Full toolkit documentation: `ai-tools/README.md`
