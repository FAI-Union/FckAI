# GitHub search rank snapshot — after P0/P1

Measured 2026-11-26 ~15:40 GMT+8 with [scripts/track_search_rank.py](scripts/track_search_rank.py), twice for the key queries to confirm stability. Compare with the pre-change [baseline](search-baseline.md).

| Query | Baseline rank | Current rank | Change |
| --- | ---: | ---: | --- |
| `AI accountability evidence` | 24 | **4** | ↑ 20 |
| `topic:ai-accountability` | 42 / 96 | **6** / 96 | ↑ 36 |
| `human-first AI` | 60 | 75 | ↓ 15 (low-value phrase) |
| `training data consent evidence` | 1 | **1** | held |
| `deepfake accountability evidence` | 1 | **1** | held |
| `FckAI in:name` | 1 | **1** | held |
| `AI accountability` | not in top 30 | not in top 100 | unchanged (expected) |
| `AI ethics` | not in top 30 | not in top 100 | unchanged (expected) |

## Interpretation

- The improvements are on **mid-tail and topic-filter searches**, which is exactly where metadata and index freshness matter. They are not proof that general discovery has improved yet.
- Head terms still require popularity signals (stars, watchers, forks) and external citations. Those remain at zero.
- `human-first AI` slipping slightly is acceptable: it is not a phrase people search for, and brand visibility is carried by `FckAI in:name` (#1) and the "Human-First AI Accountability" wording in name/description.
- Note: GitHub documentation says search does not support exact phrase matching. Presence checks with `in:readme` confirm **token** matching for `AI accountability evidence`, `AI energy cost`, `training-data consent` and `deepfake accountability`, not exact-phrase ranking.

## Next measurement

Run again after the first distribution wave (Show HN, Reddit, awesome-list outreach) and after the first 20 genuine stars. Success criteria remain in [search-baseline.md](search-baseline.md): top 3 for `AI accountability evidence`, top 10 for the topic query, and at least one external citation.
