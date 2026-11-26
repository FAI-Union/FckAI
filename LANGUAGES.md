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
| हिन्दी (Hindi) | `hi` | العربية (Arabic) | `ar` | Español (Spanish) | `es` |
| Français (French) | `fr` | Português (Portuguese) | `pt` | বাংলা (Bengali) | `bn` |
| Русский (Russian) | `ru` | 日本語 (Japanese) | `ja` | ਪੰਜਾਬੀ (Punjabi) | `pa` |
| Deutsch (German) | `de` | 한국어 (Korean) | `ko` | Italiano (Italian) | `it` |
| Türkçe (Turkish) | `tr` | Tiếng Việt (Vietnamese) | `vi` | Bahasa Indonesia (Indonesian) | `id` |
| ไทย (Thai) | `th` | اردو (Urdu) | `ur` | Polski (Polish) | `pl` |
| Українська (Ukrainian) | `uk` | Nederlands (Dutch) | `nl` | فارسی (Persian) | `fa` |
| മലയാളം (Malayalam) | `ml` | தமிழ் (Tamil) | `ta` | తెలుగు (Telugu) | `te` |
| मराठी (Marathi) | `mr` | ગુજરાતી (Gujarati) | `gu` | ಕನ್ನಡ (Kannada) | `kn` |
| Bahasa Melayu (Malay) | `ms` | Filipino (Tagalog) | `fil` | Kiswahili (Swahili) | `sw` |
| עברית (Hebrew) | `he` | Ελληνικά (Greek) | `el` | Čeština (Czech) | `cs` |
| Svenska (Swedish) | `sv` | Magyar (Hungarian) | `hu` | Română (Romanian) | `ro` |
| Dansk (Danish) | `da` | Suomi (Finnish) | `fi` | Norsk (Norwegian) | `no` |
| Српски (Serbian) | `sr` | Hrvatski (Croatian) | `hr` | Български (Bulgarian) | `bg` |
| Slovenčina (Slovak) | `sk` | Slovenščina (Slovenian) | `sl` | Català (Catalan) | `ca` |
| Afrikaans | `af` | አማርኛ (Amharic) | `am` | Hausa | `ha` |
| Yorùbá (Yoruba) | `yo` | Igbo | `ig` | isiZulu (Zulu) | `zu` |
| Soomaali (Somali) | `so` | नेपाली (Nepali) | `ne` | සිංහල (Sinhala) | `si` |
| မြန်မာ (Burmese) | `my` | ខ្មែរ (Khmer) | `km` | ລາວ (Lao) | `lo` |
| Монгол (Mongolian) | `mn` | Oʻzbekcha (Uzbek) | `uz` | Қазақша (Kazakh) | `kk` |
| Azərbaycanca (Azerbaijani) | `az` | ქართული (Georgian) | `ka` | Հայերեն (Armenian) | `hy` |
| Shqip (Albanian) | `sq` | Македонски (Macedonian) | `mk` | Bosanski (Bosnian) | `bs` |
| Lietuvių (Lithuanian) | `lt` | Latviešu (Latvian) | `lv` | Eesti (Estonian) | `et` |
| Íslenska (Icelandic) | `is` | Gaeilge (Irish) | `ga` | Cymraeg (Welsh) | `cy` |
| Euskara (Basque) | `eu` | Galego (Galician) | `gl` | 繁體中文 (Traditional Chinese) | `zh-TW` |

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
