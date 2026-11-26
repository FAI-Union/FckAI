# Wave 1 — publication pack

Status: ready to post, **not posted**. Prepared 2026-11-26.

Scope: the four community channels that can be posted without a prior relationship — Hacker News, Lobste.rs, Reddit r/technology, V2EX / 知乎. Newsletter, course and awesome-list outreach is wave 2 (needs named contacts).

Read [DISTRIBUTION.md](DISTRIBUTION.md) for the reasoning behind each angle. Do **not** paste identical text into two channels. Do **not** mention ranking, SEO, star exchange or vote coordination in a public post.

---

## Recommended order and spacing

| # | Channel | Why this position | Post URL |
| --- | --- | --- | --- |
| 1 | Hacker News — Show HN | Highest-signal technical audience; the schema/provenance angle fits | https://news.ycombinator.com/submit |
| 2 | Lobste.rs | Small, source-sensitive audience; the "caveats as schema" angle fits | https://lobste.rs/new |
| 3 | Reddit r/technology | Wider audience; use the energy example, not the HN jobs example | https://www.reddit.com/r/technology/submit |
| 4 | V2EX / 知乎 | Chinese-language audience; post on a different day from Reddit | V2EX: https://www.v2ex.com/new?tab=1 · 知乎: https://www.zhihu.com/creator/post |

Minimum spacing: one channel per day, HN first. If a post is downvoted into oblivion, do not repost the same text elsewhere the same day — wait and change the angle.

---

## 1. Hacker News — Show HN

**Title**

```
Show HN: FAI – an open evidence archive for AI accountability
```

**Body (paste as-is)**

```
We built a small, non-commercial archive where every claim about AI's real-world costs has to carry an original source, a publication date, a verbatim excerpt and caveats. Right now it has 21 cards across four areas: training-data consent, job displacement, AI energy cost and deepfake labelling.

One example that surprised us: the ILO–NASK Global Index estimates 1 in 4 jobs worldwide is exposed to generative AI, but explicitly says transformation is more likely than replacement. We reproduce that caveat rather than using the number as a scare headline: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-008.md

The loop we are trying to make work is: submit one sourced evidence card → a policy proposal cites its ID → a campaign links to the authorising discussion. If you know of a well-sourced card we are missing, the issue template takes about five minutes: https://github.com/FAI-Union/FckAI/issues/new?template=evidence.md
```

**Before posting:** confirm `EV-2026-008.md` and the issue template URL both resolve. Show HN posts must be something you built — this repo is maintained by the poster, so say so if asked.

---

## 2. Lobste.rs

**Title**

```
An evidence archive with mandatory sources and an explicit caveats field
```

**Body (paste as-is)**

```
FAI is a small repo that treats sourcing as a schema, not a norm: each `EV-YYYY-NNN.md` has frontmatter tags, a claim in two languages, a source URL, a verbatim quote and a `Caveats` section that is required by the contribution guide. Policy files reference evidence IDs; campaigns reference the authorising discussion.

The two most technically interesting cards are the CACM water-use estimate (modelled, not metered — and often misattributed to Nature) and the IEA scenario ranges. Both are in the index: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/README.md
```

**Before posting:** Lobste.rs requires an account; if the account is new, expect moderation. Do not title-case the title differently — the community is sensitive to promotional phrasing.

---

## 3. Reddit r/technology

**Title**

```
We made an AI evidence archive where every claim must link to a source — 21 cards so far
```

**Body (paste as-is)**

```
I got tired of AI debates where nobody links the underlying report. We started FAI as a non-commercial archive with a simple rule: no claim without an original source, date, excerpt and caveats.

The clearest example is energy: the IEA projects data-centre electricity demand could more than double to ~945 TWh by 2030, but the same report says the rise is small relative to the whole energy sector and could be offset by AI-enabled savings. Both sides of that sentence are in the card: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-001.md

If you want to contribute, add one sourced card. Unsourced submissions are tagged `needs-source` and are not used in decisions.
```

**Before posting:** check r/technology self-promotion rules at post time; if self-posts are restricted, use r/opensource with the same structure but a different opening sentence about the schema. Never post to both subreddits on the same day.

---

## 4a. V2EX（中文）

**标题**

```
我们做了一个每条主张都必须带原始来源的 AI 问责证据库
```

**正文（原样粘贴）**

```
做这个仓库的原因很简单：AI 讨论里太多数字被人从报告里抠出来当标题，却没人贴上下文。FAI 的规则是每张证据卡必须有原始链接、发布日期、原文摘录和"说明/局限"栏；没有来源的主张会被打上 `needs-source`，不进入决策。

例如 ILO–NASK 的"全球四分之一岗位受到生成式 AI 影响"，原文同时强调最可能的结果是岗位转型，而不是失业。我们把这句限制条件写在卡片里：https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-008.md

目前 21 张卡，覆盖训练数据同意、就业、能源与深度伪造。欢迎认领一张卡的中文摘要，或在 issue 里补一条我们漏掉的权威来源。
```

**发布位置：** V2EX「分享创造」或「开发者」节点。发布前确认节点规则允许项目分享。

---

## 4b. 知乎（中文）

**标题**

```
如何评价「每条 AI 主张都必须附带原始来源和局限说明」的证据库做法？
```

**正文（原样粘贴，自问自答形式）**

```
最近在做一个非商业的 AI 问责证据库，规则很死板：每张卡片必须有原始报告链接、发布日期、原文摘录，以及一个必填的「说明/局限」栏。没有来源的主张会被打上 needs-source，不进入决策。

举个具体例子：ILO–NASK 全球指数的标题是「全球四分之一岗位受到生成式 AI 影响」，但原文同时说最可能的结果是岗位转型而不是失业。我们要求这两句话必须一起出现在卡片里：https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-008.md

目前 21 张卡，覆盖训练数据同意、就业、能源和深度伪造。想问的是：这种把「局限」变成必填字段的做法，在中文语境的公共讨论里可行吗？欢迎直接指出卡片里被我们漏掉的限制条件。
```

**发布位置：** 知乎提问或文章均可。不要同时发 V2EX 和知乎同一天。

---

## Pre-flight checklist

- [ ] Every linked card exists and its source URL resolves (checked 2026-11-26; recheck on post day).
- [ ] Caveats are present in the post, not silently dropped.
- [ ] Channel-specific copy is used; no identical cross-post.
- [ ] No star exchange, no vote buying, no claims of official affiliation.
- [ ] Poster is logged in with an account that is allowed to post on that channel.

## After posting

Record in `CHANGELOG.md` under the dated entry: channel, post URL, exact timestamp, and the initial card/index links that received clicks. Check at +24h and +7d: stars, watchers, new issues, new evidence-card PRs, and referral traffic in GitHub Insights. Do not measure success by a single-day star spike.

## Not in wave 1

Newsletter, creator-rights groups, university courses and awesome-list outreach in [DISTRIBUTION.md](DISTRIBUTION.md) §§5–7 require named contacts and individual messages. They are wave 2; do not bulk-ping lists.
