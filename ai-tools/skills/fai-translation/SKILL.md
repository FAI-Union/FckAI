---
name: fai-translation
description: Add, review or validate FAI translations in locales BCP 47 tag directories and keep LANGUAGES.md in sync. Use when asked to translate README/MANIFESTO/GOVERNANCE/CODE_OF_CONDUCT, claim a language, fix a translation PR, or check the i18n title format and backlink requirements.
agent_created: true
---

# FAI translation workflow

## Overview

Root English files are authoritative. Translations live in `locales/<tag>/` and are community maintained. The project prioritises ten languages (`es fr de ja ko pt-BR ar hi ru zh-TW`) but accepts claims in any language with no speaker-count threshold.

## Tooling

```bash
python D:/Git/FAI/ai-tools/cli.py translation-status
python D:/Git/FAI/ai-tools/cli.py translation-validate zh-TW --title "i18n(zh-TW): add Traditional Chinese translation" --files LANGUAGES.md locales/zh-TW/README.md
python D:/Git/FAI/ai-tools/cli.py validate-links
python D:/Git/FAI/ai-tools/cli.py preflight --title "i18n(zh-TW): add Traditional Chinese translation" --files locales/zh-TW/README.md LANGUAGES.md
```

MCP equivalents: `translation_status`, `validate_translation`, `validate_links`, `search_repo`, `preflight_submission`, `repo_status`.

## Workflow

1. Run `translation_status` to see existing rows, locale directories, priority languages not started and inconsistencies. Verify the tag is a BCP 47 code (`pt-BR`, not `pt_br`).
2. A language is claimed through an `[i18n]` issue. Add the language to `LANGUAGES.md` with status `⏳`, the maintainer handle and the current `Last verified` date; five seeded good-first issues (#3–#7) already exist for the priority batch — check before opening a new one.
3. Translate the four core documents into `locales/<tag>/`: `README.md`, `MANIFESTO.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`. Partial translations are allowed only when marked clearly.
4. Include a language-switch table in the translated README, and link every translated file back to its English original with a relative `../../<FILE>.md` path. `locales/zh-CN/` is the worked example.
5. Do **not** translate evidence IDs (`EV-2026-001`), frontmatter keys, file paths, code, tag names, or the literal label `needs-source`. Fidelity to the English claim takes priority over fluency.
6. Update `LANGUAGES.md` and the language table in the root README where applicable. Set `Last verified` only after an actual review against the English original.
7. Run `validate_translation` with the final title and changed-file list, then `validate_links` and `preflight_submission`. The PR title must be exactly `i18n(<tag>): add <Language> translation`; content-validation also requires `LANGUAGES.md` in the diff.

## Rules

- Never silently claim a translation is complete or verified. Stale translations are flagged, not trusted.
- Never translate a factual claim into a stronger statement; if unsure, keep the English sentence and mark it for maintainer review.

## References

- `CONTRIBUTING.md#translating`, `LANGUAGES.md`, `locales/zh-CN/`, `.github/ISSUE_TEMPLATE/translation.md`, `RUNBOOK.md#23-translations-10-not-75`
- Full toolkit documentation: `ai-tools/README.md`
