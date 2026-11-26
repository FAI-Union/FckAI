---
name: fai-evidence
description: Create, validate and index sourced evidence cards in the FAI repository (RESEARCH/EV-*.md). Use when asked to add an evidence card, verify a factual claim and its original source, review RESEARCH/ evidence, update the research index, or fix the EV to POLICY/CAMPAIGNS chain. Enforces the project rule that every factual claim carries a source.
agent_created: true
---

# FAI evidence cards

## Overview

Maintains the FAI evidence archive: one `EV-YYYY-NNN.md` card per sourced factual claim, with English and Chinese claims, an original URL, a verbatim quote, caveats and a `Used by` section. The archive is the trust base for policies and campaigns.

## Tooling

Prefer the `fai` MCP tools. If the MCP server is not registered, run the equivalent CLI (replace the path if the checkout moved):

```bash
python D:/Git/FAI/ai-tools/cli.py evidence-list --tag energy
python D:/Git/FAI/ai-tools/cli.py evidence-next-id
python D:/Git/FAI/ai-tools/cli.py evidence-get EV-2026-001
python D:/Git/FAI/ai-tools/cli.py evidence-scaffold --claim-en "..." --claim-zh "..." --source-url "https://..." --publisher "..." --excerpt "..." --caveats "..." --tags energy
python D:/Git/FAI/ai-tools/cli.py evidence-validate EV-2026-022
python D:/Git/FAI/ai-tools/cli.py evidence-chain
```

MCP equivalents: `list_evidence`, `get_evidence`, `next_evidence_id`, `scaffold_evidence`, `validate_evidence` (accepts raw `text` for drafts), `check_evidence_chain`, `search_repo`, `preflight_submission`, `validate_links`.

## Workflow

1. Check for duplicates first: `list_evidence` with a tag or query and `search_repo` for the claim's key entities. A second card for the same fact is a bug.
2. Reserve the next ID with `next_evidence_id`. Do not renumber existing cards.
3. Source the claim from an original publisher (report, regulator, dataset or peer-reviewed paper). Record the exact publication date and a short verbatim quote. Search-engine snippets, summaries and other FAI cards are not original sources.
4. Generate a draft with `scaffold_evidence`. Check its `validation` result; fix errors before writing anything. The draft's `verified_by` is a placeholder — only a maintainer may replace it with a real handle after review.
5. Write the draft to `RESEARCH/<ID>.md`. Preserve the exact headings `## Claim / 主张`, `## Source / 来源`, `## Excerpt / 引述`, `## Caveats / 说明`, `## Used by / 引用方` and the frontmatter keys `id/status/verified_by/last_reviewed/tags`.
6. Add a row to `RESEARCH/README.md` under the matching four-domain heading, with the ID link, one-line claim, source link and backtick tags. Keep the "Last updated" count accurate.
7. Run `validate_evidence(<ID>)`, `check_evidence_chain` and `validate_links`. A `Pending` value in `Used by` is only acceptable when no policy or campaign cites the card yet.
8. Before proposing a PR, run `preflight_submission` with the changed paths and put the source URL in the PR body; the content-validation workflow requires it.

## Rules

- One factual claim per card. Distinguish projections from measured values in `Caveats`; state scope, jurisdiction and known exceptions.
- Claims and caveats are bilingual (English + Chinese). Never translate the ID, frontmatter keys, file paths or the `needs-source` label.
- Unsourced claims are labelled `needs-source` and cannot be used for decisions. Never invent or guess a source URL.
- Policies must cite an `EV-*` ID; cards must backlink the policies and campaigns that cite them (`check_evidence_chain` verifies both directions).
- Translations of a card keep the same ID with a locale suffix, e.g. `EV-2026-001.zh-CN.md`.

## References

- Canonical rules: `README.md`, `CONTRIBUTING.md#submitting-evidence`, `RESEARCH/README.md`, `.github/ISSUE_TEMPLATE/evidence.md`
- Full toolkit documentation: `ai-tools/README.md`
