---
name: fai-policy-campaign
description: Draft FAI policy proposals and campaign/distribution documents that trace back to evidence IDs and an authorised discussion. Use when asked to write or review POLICY/PP-*.md, CAMPAIGNS/*.md, outreach copy, or to check the 7-day consensus and red-line requirements before publication.
agent_created: true
---

# FAI policy and campaign drafting

## Overview

Turns evidence cards into policy proposals and authorised public actions. The chain is strictly one-way: `RESEARCH` evidence → `POLICY` proposal → `CAMPAIGNS` action → distribution. Every step must be traceable and every public claim must cite an evidence ID.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py evidence-list
python D:/Git/FAI/ai-tools/cli.py evidence-chain
python D:/Git/FAI/ai-tools/cli.py validate-links
python D:/Git/FAI/ai-tools/cli.py preflight --title "..." --body "Source: https://..." --files POLICY/PP-2026-002.md
```

MCP equivalents: `list_evidence`, `get_evidence`, `check_evidence_chain`, `validate_links`, `preflight_submission`, `search_repo`.

## Policy workflow

1. Read `POLICY/README.md` and the closest existing proposal (`POLICY/PP-2026-001.md`) before drafting. A proposal needs: problem, proposed measure, evidence base (at least one real `EV-YYYY-NNN` ID), trade-offs, discussion link and a red-line check.
2. Confirm each cited EV ID exists with `get_evidence` and that its claim actually supports the measure. Do not stretch a projection into a measured fact.
3. Open with `Status`/`Opened` metadata and a Discussion or Issue link. `GOVERNANCE.md` requires a 7-day consensus window; no substantive objection means consensus, a split decision needs a 2/3 vote.
4. After merging, update the cited cards' `Used by` sections and re-run `check_evidence_chain`.

## Campaign workflow

1. Read `CAMPAIGNS/README.md`, `CAMPAIGNS/TEMPLATE.md` and any existing wave pack. Required fields: Status, Coordinator, Decision thread, Authorisation (linked decision + consensus date + decision rule), Evidence base (EV IDs), Action, Outcome, Red-line check.
2. Use `check_evidence_chain` to verify every cited EV ID resolves and is backed by a card. Campaign facts must link to the archive, not to a secondary summary.
3. Tailor copy per channel: one concrete pain + one verifiable evidence + one immediate action. `CAMPAIGNS/DISTRIBUTION.md` and `CAMPAIGNS/WAVE-1.md` show the established format.
4. Red lines: no harassment, threats, vandalism, impersonation of an official body, unsourced claims, ranking/SEO talk in public posts, star exchanges or buying stars.
5. **Publishing is a human action.** Prepare drafts and mark status `ready, not posted`. Never post to HN, Reddit, V2EX, 知乎 or a newsletter and never claim an item was posted unless a human confirms it.
6. Validate links and run `preflight_submission` with the source URL in the PR body before opening a PR.

## Human gates

Admin-only GitHub settings, external publication and acceptance of a policy are never automated. When a step needs a human, state exactly which URL/action needs confirmation and leave the artefact in a ready state.

## References

- `GOVERNANCE.md`, `POLICY/README.md`, `CAMPAIGNS/README.md`, `CAMPAIGNS/TEMPLATE.md`, `RUNBOOK.md#2-maintenance-turn-governance-into-executable-process`
- Full toolkit documentation: `ai-tools/README.md`
