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

## Automated checks / 自动检查

Two GitHub Actions workflows screen every new issue and pull request:

- **Contribution triage** closes submissions from automated accounts (`suspected-bot`). Brand-new empty accounts and submissions without a source link are only labelled `needs-review` / `needs-source` — they are **never** rejected by the bot. A maintainer always decides.
- **Content validation** fails a PR that changes `RESEARCH/`, `POLICY/` or `CAMPAIGNS/` without a source URL in the description, or a translation PR that omits the `i18n(<tag>):` title format or the `LANGUAGES.md` update.

If a check is wrong, reply in the thread and mention a maintainer. Do not open a duplicate submission.

两个 GitHub Actions 工作流会对新 issue 和 PR 做初筛：机器账号直接关闭；新账号、无来源链接仅打标签，**不会**由机器人直接拒绝，一切由维护者人工决定。若判断有误请在原帖回复并 @ 维护者，不要重复提交。

## Maintainer response standard / 维护者响应标准

- **First response within 72 hours.** A short acknowledgement is enough; silence is not.
- Every PR receives an explicit next step: merge, revise with named items, or decline with a reason and a path to resubmit.
- On merge, thank the contributor publicly and @ them. Every contributor brings their own network.
- `good first issue` is reserved for ~30-minute tasks: add a missing source, translate one evidence card, fix a broken link.

## Evidence chain / 证据链

Three layers, one direction:

1. `RESEARCH/EV-<year>-<number>.md` — claim, source URL, publication date, excerpt, caveats, verifier, last-reviewed date.
2. `POLICY/PP-<year>-<number>.md` — every proposal cites at least one evidence ID.
3. `CAMPAIGNS/<YYYY-MM>-<name>.md` — every action links to the Discussion or Issue that authorised it. See `CAMPAIGNS/TEMPLATE.md`.

Unsourced claims are labelled `needs-source` and are not used as a basis for decisions (GOVERNANCE.md).

## Cadence / 节奏

Weekly: one sourced evidence card. Every two weeks: one Discussion on a live policy question. Monthly: one brief, a `CHANGELOG.md` entry, and a metrics review. Consistency is our trust signal.
