# Languages / 语言列表

The default language of this repository is **English**. All content in the root directory is the authoritative original; translations under `locales/` are community-maintained and may lag behind.

本仓库默认语言为 **英语**。根目录内容为权威原文，`locales/` 下的译文由社区维护，可能滞后于原文。

## Status / 状态表

Legend / 图例: ✅ complete 完成 · 🟡 partial 部分 · ⏳ in progress 进行中 · — not started 未开始

| Language 语言 | Tag | README | MANIFESTO | GOVERNANCE | CODE_OF_CONDUCT | Maintainer |
| --- | --- | --- | --- | --- | --- | --- |
| English (default) | `en` | ✅ | ✅ | ✅ | ✅ | core team |
| 简体中文 | `zh-CN` | ✅ | ✅ | ✅ | ✅ | community |

## Add a language / 新增语言

Any language is welcome — there is no minimum speaker count. Use a [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) tag (e.g. `zh-TW`, `es`, `fr`, `ja`, `ko`, `ar`, `hi`, `pt-BR`) and follow the [translation guide](CONTRIBUTING.md#translating).

欢迎任何语言，无使用人数门槛。使用 [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) 标签（例如 `zh-TW`、`es`、`fr`、`ja`、`ko`、`ar`、`hi`、`pt-BR`），并遵循[翻译指南](CONTRIBUTING.md#translating)。

Add your language to the table above and to the root [README.md](README.md#languages) in the same pull request.

请在同一个 Pull Request 中把你的语言加入上表和根目录 [README.md](README.md#languages) 的语言表格。

## Layout / 目录结构

```
README.md              <- English default / 英文原文
MANIFESTO.md
GOVERNANCE.md
CODE_OF_CONDUCT.md
CONTRIBUTING.md
LANGUAGES.md
locales/
  <tag>/
    README.md
    MANIFESTO.md
    GOVERNANCE.md
    CODE_OF_CONDUCT.md
```
