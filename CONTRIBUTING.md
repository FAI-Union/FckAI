# Contributing

Thanks for helping build FAI. This project is open, non-commercial, and community-driven. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## Ways to contribute

- **Evidence**: submit sourced facts to `RESEARCH/`. Every factual claim needs an original source.
- **Policy**: draft proposals in `POLICY/`.
- **Campaigns**: document petitions, open letters, and events in `CAMPAIGNS/`.
- **Discussion**: open topics in Discussions or use the [issue templates](.github/ISSUE_TEMPLATE).
- **Translation**: see below.

## Translating

The repository's default language is **English**. All translations live in `locales/<language-tag>/`, using [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) language tags (e.g. `zh-CN`, `es`, `pt-BR`, `ar`).

### Steps

1. Check [LANGUAGES.md](LANGUAGES.md) — if your language already exists, improve the existing files instead of starting over.
2. Create the directory `locales/<tag>/` and translate these core documents, keeping the English structure and headings:
   - `README.md`
   - `MANIFESTO.md`
   - `GOVERNANCE.md`
   - `CODE_OF_CONDUCT.md`
3. In the translated `README.md`, include the language switcher table and point back to the English originals.
4. Add your language to the table in [LANGUAGES.md](LANGUAGES.md) and to the root [README.md](README.md) language table.
5. Open a pull request with the title `i18n(<tag>): add <Language> translation`.

### Translation guidelines

- **Fidelity over fluency**: preserve meaning, tone, and the exact wording of the five commitments and the red lines.
- **Keep terms consistent**: "accountability" / "consent" / "evidence" should use the same translation across all files.
- **Do not translate** code, file paths, front matter keys, or the tags `needs-source`.
- **Dates and numbers** may follow local conventions; keep the source link untouched.
- **Partial translations are welcome** — clearly mark untranslated sections and we will help complete them.

## Review process

Translation PRs are reviewed by a maintainer for accuracy and consistency, following the [Governance](GOVERNANCE.md) rules. Consensus-based decisions and records are kept in Issues/Discussions.
