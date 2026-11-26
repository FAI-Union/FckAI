# Manual setup checklist / 需人工完成的设置

These items could not be changed from the current automation environment: the available GitHub token can read the repository but has no admin/issue-write scope for `FAI-Union`. Everything below is a human action at github.com. Verify each one with the check column.

| # | Action | Exact value | Verify |
| --- | --- | --- | --- |
| 1 | Repository description | `Open AI accountability and AI ethics evidence archive: sourced evidence on training-data consent, job displacement, energy cost and deepfakes. Non-commercial and checkable.` | `GET /repos/FAI-Union/FckAI` → `description` |
| 2 | Topics (max 20) | list below | `GET /repos/FAI-Union/FckAI` → `topics`, length 20 |
| 3 | Social preview | Upload `assets/social-preview.png` (1280×640) under Settings → Social preview | repo right sidebar shows the image |
| 4 | Org profile | Create public repo `FAI-Union/.github` with `README.md` (draft below) | https://github.com/FAI-Union shows the profile README |
| 5 | Seed issues | Already satisfied: issues #3–#7 carry `good first issue`. The 3 drafts below are **optional** additions for evidence work, not a blocker. | GitHub search `repo:FAI-Union/FckAI label:"good first issue"` returns ≥5 |
| 6 | Labels | Ensure `evidence`, `good first issue`, `needs-source`, `consensus-7d` exist | Issues → Labels |

## Topics to set

```
ai
artificial-intelligence
ai-accountability
ai-ethics
ai-governance
ai-policy
responsible-ai
ethical-ai
copyright
consent
deepfakes
transparency
evidence
open-data
sustainability
energy
explainable-ai
policy
fact-checking
human-first
```

Rationale: `ai` (≈198k repos), `ai-governance` (≈7.5k), `responsible-ai` (≈2.7k), `ai-ethics` (890), `copyright` (379), `ai-policy` (240), `deepfakes` (185) and `ai-accountability` (96) were measured on 2026-11-26. `i18n` and `advocacy` were dropped for low search intent; translations remain discoverable through `LANGUAGES.md`.

## CLI equivalent (if you have `gh` and admin access)

```bash
gh repo edit FAI-Union/FckAI \
  --description "Open AI accountability and AI ethics evidence archive: sourced evidence on training-data consent, job displacement, energy cost and deepfakes. Non-commercial and checkable." \
  --add-topic ai --add-topic artificial-intelligence --add-topic ai-accountability \
  --add-topic ai-ethics --add-topic ai-governance --add-topic ai-policy \
  --add-topic responsible-ai --add-topic ethical-ai --add-topic copyright \
  --add-topic consent --add-topic deepfakes --add-topic transparency \
  --add-topic evidence --add-topic open-data --add-topic sustainability \
  --add-topic energy --add-topic explainable-ai --add-topic policy \
  --add-topic fact-checking --add-topic human-first \
  --remove-topic i18n --remove-topic advocacy
```

## Org profile README draft

Save as `README.md` in `FAI-Union/.github`:

```markdown
# FAI · Human-First AI Accountability

Open, non-commercial, evidence-first.

We archive the real costs of AI — training-data consent, job displacement, energy cost and deepfakes — with sources anyone can check.

- Main repository: https://github.com/FAI-Union/FckAI
- Evidence index: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/README.md
- Landing page: https://fai-union.github.io/FckAI/
```

## Optional seed issue drafts

Existing issues #3–#7 already cover translation claims with the `good first issue` label. These three drafts widen the entry points to evidence work if an admin wants them.

**Issue 1** — title: `good first issue: add one sourced evidence card on AI energy disclosure`
Labels: `good first issue`, `evidence`

> **Time:** ~30 minutes. Pick one verifiable, publicly documented fact about AI energy use that is not already in `RESEARCH/README.md`. Open a PR adding `RESEARCH/EV-YYYY-NNN.md` with frontmatter (`id`, `status`, `verified_by`, `last_reviewed`, `tags`), bilingual claim, original source URL and date, a short verbatim quote, and caveats. PR body must include at least one source URL. Link the new card from `RESEARCH/README.md`.

**Issue 2** — title: `good first issue: translate EV-2026-008 into Spanish`
Labels: `good first issue`, `i18n`

> **Time:** ~30 minutes. Create `RESEARCH/EV-2026-008.es.md`, keeping the same ID, source URL and caveats. Update `LANGUAGES.md` and use PR title `i18n(es): add Spanish translation`. Read `CONTRIBUTING.md` first.

**Issue 3** — title: `good first issue: add a source to one needs-source claim`
Labels: `good first issue`, `needs-source`

> **Time:** ~30 minutes. Find an issue or card tagged `needs-source`, locate an authoritative primary source, and open a PR adding the source URL, publication date and a short verbatim quote. Do not change the claim to make it easier to source.

## Why these are manual

The current GitHub integration token can search and push file content, but `POST /orgs/FAI-Union/repos`, `POST /repos/FAI-Union/FckAI/issues` and repository PATCH all return 403. No automation should try to work around that; ask an org admin to run the steps above.
