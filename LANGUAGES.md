# Languages / 语言列表

The default language of this repository is **English**. All content in the root directory is the authoritative original; translations under `locales/` are community-maintained and may lag behind.

本仓库默认语言为 **英语**。根目录内容为权威原文，`locales/` 下的译文由社区维护，可能滞后于原文。

## Status / 状态表

Legend / 图例: ✅ complete 完成 · 🟡 partial 部分 · ⏳ in progress 进行中 · — not started 未开始

| Language 语言 | Tag | README | MANIFESTO | GOVERNANCE | CODE_OF_CONDUCT | Maintainer |
| --- | --- | --- | --- | --- | --- | --- |
| English (default) | `en` | ✅ | ✅ | ✅ | ✅ | core team |
| 简体中文 | `zh-CN` | ✅ | ✅ | ✅ | ✅ | community |

## Wanted languages / 待翻译语言

The major world languages below have no translation yet. Any language is welcome — there is no minimum speaker count. Claim one by opening a `[i18n]` issue, then follow the [translation guide](CONTRIBUTING.md#translating).

以下世界主要语言尚无译文。欢迎任何语言，无使用人数门槛。开一个 `[i18n]` issue 认领，然后遵循[翻译指南](CONTRIBUTING.md#translating)。

| Language | Tag | Language | Tag | Language | Tag |
| --- | --- | --- | --- | --- | --- |
| Afrikaans | `af` | አማርኛ (Amharic) | `am` | العربية (Arabic) | `ar` |
| Azərbaycanca (Azerbaijani) | `az` | Български (Bulgarian) | `bg` | বাংলা (Bengali) | `bn` |
| Bosanski (Bosnian) | `bs` | Català (Catalan) | `ca` | Čeština (Czech) | `cs` |
| Cymraeg (Welsh) | `cy` | Dansk (Danish) | `da` | Deutsch (German) | `de` |
| Ελληνικά (Greek) | `el` | Español (Spanish) | `es` | Eesti (Estonian) | `et` |
| Euskara (Basque) | `eu` | فارسی (Persian) | `fa` | Suomi (Finnish) | `fi` |
| Filipino (Tagalog) | `fil` | Français (French) | `fr` | Gaeilge (Irish) | `ga` |
| Galego (Galician) | `gl` | ગુજરાતી (Gujarati) | `gu` | Hausa | `ha` |
| עברית (Hebrew) | `he` | हिन्दी (Hindi) | `hi` | Hrvatski (Croatian) | `hr` |
| Magyar (Hungarian) | `hu` | Հայերեն (Armenian) | `hy` | Bahasa Indonesia (Indonesian) | `id` |
| Igbo | `ig` | Íslenska (Icelandic) | `is` | Italiano (Italian) | `it` |
| 日本語 (Japanese) | `ja` | ქართული (Georgian) | `ka` | Қазақша (Kazakh) | `kk` |
| ខ្មែរ (Khmer) | `km` | ಕನ್ನಡ (Kannada) | `kn` | 한국어 (Korean) | `ko` |
| ລາວ (Lao) | `lo` | Lietuvių (Lithuanian) | `lt` | Latviešu (Latvian) | `lv` |
| Македонски (Macedonian) | `mk` | മലയാളം (Malayalam) | `ml` | Монгол (Mongolian) | `mn` |
| मराठी (Marathi) | `mr` | Bahasa Melayu (Malay) | `ms` | မြန်မာ (Burmese) | `my` |
| नेपाली (Nepali) | `ne` | Nederlands (Dutch) | `nl` | Norsk (Norwegian) | `no` |
| ਪੰਜਾਬੀ (Punjabi) | `pa` | Polski (Polish) | `pl` | Português (Portuguese) | `pt` |
| Română (Romanian) | `ro` | Русский (Russian) | `ru` | සිංහල (Sinhala) | `si` |
| Slovenčina (Slovak) | `sk` | Slovenščina (Slovenian) | `sl` | Soomaali (Somali) | `so` |
| Shqip (Albanian) | `sq` | Српски (Serbian) | `sr` | Svenska (Swedish) | `sv` |
| Kiswahili (Swahili) | `sw` | தமிழ் (Tamil) | `ta` | తెలుగు (Telugu) | `te` |
| ไทย (Thai) | `th` | Türkçe (Turkish) | `tr` | Українська (Ukrainian) | `uk` |
| اردو (Urdu) | `ur` | Oʻzbekcha (Uzbek) | `uz` | Tiếng Việt (Vietnamese) | `vi` |
| Yorùbá (Yoruba) | `yo` | 繁體中文 (Traditional Chinese) | `zh-TW` | isiZulu (Zulu) | `zu` |

## Add a language / 新增语言

Use a [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) tag (e.g. `zh-TW`, `es`, `fr`, `ja`, `ko`, `ar`, `hi`, `pt-BR`) and follow the [translation guide](CONTRIBUTING.md#translating). A language not listed above is equally welcome.

使用 [BCP 47](https://www.rfc-editor.org/rfc/rfc5646) 标签（例如 `zh-TW`、`es`、`fr`、`ja`、`ko`、`ar`、`hi`、`pt-BR`），并遵循[翻译指南](CONTRIBUTING.md#translating)。上表未列出的语言同样欢迎。

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
