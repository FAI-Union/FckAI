# Distribution kit / 分发材料包

Status: prepared, **not posted**. Ready-to-paste copy with post URLs, order and checks is in [WAVE-1.md](WAVE-1.md). Posting is a human action — see [RUNBOOK.md](../RUNBOOK.md) §3.4 and the red lines in [README.md](../README.md).

Every channel gets the same structure: **one concrete pain + one verifiable evidence card + one immediate action**. Do not paste identical copy everywhere. Do not buy votes, do not coordinate star exchanges, do not mention "ranking" or "SEO" in public posts.

---

## 1. Hacker News — Show HN

**Title:** Show HN: FAI – an open evidence archive for AI accountability

**Body:**

> We built a small, non-commercial archive where every claim about AI's real-world costs has to carry an original source, a publication date, a verbatim excerpt and caveats. Right now it has 21 cards across four areas: training-data consent, job displacement, AI energy cost and deepfake labelling.
>
> One example that surprised us: the ILO–NASK Global Index estimates 1 in 4 jobs worldwide is exposed to generative AI, but explicitly says transformation is more likely than replacement. We reproduce that caveat rather than using the number as a scare headline: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-008.md
>
> The loop we are trying to make work is: submit one sourced evidence card → a policy proposal cites its ID → a campaign links to the authorising discussion. If you know of a well-sourced card we are missing, the issue template takes about five minutes: https://github.com/FAI-Union/FckAI/issues/new?template=evidence.md

---

## 2. Reddit r/technology

**Title:** We made an AI evidence archive where every claim must link to a source — 21 cards so far

**Body:**

> I got tired of AI debates where nobody links the underlying report. We started FAI as a non-commercial archive with a simple rule: no claim without an original source, date, excerpt and caveats.
>
> The clearest example is energy: the IEA projects data-centre electricity demand could more than double to ~945 TWh by 2030, but the same report says the rise is small relative to the whole energy sector and could be offset by AI-enabled savings. Both sides of that sentence are in the card: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-001.md
>
> If you want to contribute, add one sourced card. Unsourced submissions are tagged `needs-source` and are not used in decisions.

**Note:** do not post to multiple subreddits on the same day with identical text. r/opensource and r/technology need different angles.

---

## 3. Lobste.rs

**Title:** An evidence archive with mandatory sources and an explicit caveats field

**Body:**

> FAI is a small repo that treats sourcing as a schema, not a norm: each `EV-YYYY-NNN.md` has frontmatter tags, a claim in two languages, a source URL, a verbatim quote and a `Caveats` section that is required by the contribution guide. Policy files reference evidence IDs; campaigns reference the authorising discussion.
>
> The two most technically interesting cards are the CACM water-use estimate (modelled, not metered — and often misattributed to Nature) and the IEA scenario ranges. Both are in the index: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/README.md

---

## 4. V2EX / 知乎（中文）

**标题：** 我们做了一个每条主张都必须带原始来源的 AI 问责证据库

**正文：**

> 做这个仓库的原因很简单：AI 讨论里太多数字被人从报告里抠出来当标题，却没人贴上下文。FAI 的规则是每张证据卡必须有原始链接、发布日期、原文摘录和"说明/局限"栏；没有来源的主张会被打上 `needs-source`，不进入决策。
>
> 例如 ILO–NASK 的"全球四分之一岗位受到生成式 AI 影响"，原文同时强调最可能的结果是岗位转型，而不是失业。我们把这句限制条件写在卡片里：https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-008.md
>
> 目前 21 张卡，覆盖训练数据同意、就业、能源与深度伪造。欢迎认领一张卡的中文摘要，或在 issue 里补一条我们漏掉的权威来源。

---

## 5. AI-ethics newsletter / creator-rights group

**Subject:** One sourced card for your next issue: AI power-demand projections

**Body:**

> If your next issue needs a citable projection on AI energy demand, here is a card with the IEA source, date, verbatim quote and caveats already extracted: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-001.md
>
> For emissions scenarios rather than demand, use EV-2026-015: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/EV-2026-015.md
>
> FAI is non-commercial and does not ask for promotion — only that the caveats travel with the number. If you know of a report we have missed, send it our way.

---

## 6. University courses / seminars

**Subject:** Ready-made, caveated evidence cards for AI-ethics seminars

**Body:**

> We maintain 21 short evidence cards in English, each with an original source, date, quote and a required `Caveats` section. They are designed for classroom debate: students can check the primary source and argue about the interpretation rather than the number. Index: https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/README.md
>
> If you use them in a course, we would appreciate a link back to the index so students can see updates.

---

## 7. Awesome-list outreach

Targets to approach individually (check the list's scope first; do not bulk-ping):

| List | Angle |
| --- | --- |
| `awelist/awesome-ai-ethics` | Evidence-first AI ethics resource |
| `EthicalML/awesome-artificial-intelligence-regulation` | Policy proposals cite evidence IDs |
| AI energy / sustainability lists | IEA and CACM cards with caveats |
| Deepfake / media-literacy lists | EU AI Act Art. 50 and CAC labelling cards |

Template:

> Hi — I maintain FAI, a non-commercial archive of sourced evidence on AI accountability. It currently has 21 cards with original sources and explicit caveats across training-data consent, jobs, energy and deepfakes. If it fits your list, the index is https://github.com/FAI-Union/FckAI/blob/main/RESEARCH/README.md. If not, no problem — and if you know a better resource for a gap we have, I would like to hear about it.

---

## 8. Check before posting

- The card you cite exists, and its source URL resolves.
- Caveats are included in the post, not silently dropped.
- Channel-specific copy is used; no cross-posting identical text.
- No star exchange, no vote buying, no claims of official affiliation.
- Log the post in [CHANGELOG.md](../CHANGELOG.md) under the dated entry.
