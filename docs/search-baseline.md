# GitHub search baseline / 搜索排名基线

Snapshot: 2026-11-26, before the P0/P1 changes were pushed. Measured with the GitHub REST repository search API (best-match default sort), using [scripts/track_search_rank.py](../scripts/track_search_rank.py). See the [post-change measurement](rank-2026-11-26-after.md) for current ranks.

| Query | total_count | Rank | Note |
| --- | ---: | ---: | --- |
| `AI accountability` | 2557 | not in top 30 | head term; 0-star cold start cannot win it |
| `AI ethics` | 3564 | not in top 30 | same |
| `deepfakes` | 12106 | not in top 30 | dominated by high-star tooling repos |
| `topic:ai-accountability` | 96 | 42 | topic is applied but popularity is low |
| `topic:ai-accountability stars:0` | 58 | 4 | competitive once equal-star filter is applied |
| `ai accountability in:description` | 2218 | not in top 30 | description matches, ranking still weak |
| `ai accountability in:readme` | 72239 | not in top 30 | README match alone is not enough |
| `AI accountability evidence` | 162 | 24 | best realistic near-term target |
| `training data consent evidence` | 1 | 1 | already #1 — protect this |
| `deepfake accountability evidence` | 1 | 1 | already #1 — protect this |
| `human-first AI` | 153 | 60 | weak brand phrase |
| `FckAI in:name` | 2 | 1 | brand is discoverable by exact name |

## What this says

- The **index layer is already correct**: description, topics and README are searchable, and the repo is indexed.
- The bottleneck is **popularity and external discovery**: stars, forks, watchers and external citations were all zero at baseline.
- Strategy: hold the long-tail #1 positions, push `AI accountability evidence` into the top 10, then attack the topic rankings once real contributors arrive.

## Weekly cadence

1. Run `python scripts/track_search_rank.py > docs/rank-YYYY-MM-DD.md` (use `GITHUB_TOKEN` if available).
2. Compare against this baseline; record stars, watchers, forks, evidence-card count and external citations in [CHANGELOG.md](../CHANGELOG.md).
3. Targets after 4 weeks: `AI accountability evidence` ≤ 10; `topic:ai-accountability` ≤ 20; the two long-tail #1 positions retained.
4. Targets after 8 weeks: `AI accountability evidence` ≤ 3; `topic:ai-accountability` ≤ 10; at least one external citation from a course, newsletter or awesome list.

Do not chase head terms with keyword stuffing or star exchanges. Relevant reading: [GitHub repository search fields](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories) and [about GitHub search](https://docs.github.com/en/search-github/getting-started-with-searching-on-github/about-searching-on-github).
