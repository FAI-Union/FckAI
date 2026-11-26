# Governance Rules

This document defines how this alliance makes decisions, who decides, and how members leave.

## Core principles

- **Consensus first**: seek agreement through discussion rather than a simple majority vote.
- **Evidence first**: factual claims must carry sources; unsourced content is tagged `needs-source` and is not used as a basis for decisions.
- **Transparent traceability**: all decisions are discussed publicly in Issues or Discussions and recorded there.

## Roles

| Role | How to become one | Permissions |
| --- | --- | --- |
| Contributor | At least one merged contribution | Open issues, join discussions |
| Maintainer | Nominated by an existing maintainer, approved by consensus | Merge PRs, apply labels, review content |
| Coordinator | Rotates among maintainers, three-month term | Chair discussions, summarize consensus, publish official documents |

These roles map to GitHub teams in the `FAI-Union` organization:

- `core` — repository admins and CODEOWNERS target; final escalation.
- `maintainers` — merge PRs, apply labels, review content.
- `translators` — claim and review files under `locales/`.

A role is not effective until the corresponding team membership is granted. Promote by adding the member to the team and recording it in a Discussion.

## Decision process

1. Any member may propose a motion in Discussions.
2. The proposal stays open for discussion for at least 7 days.
3. If there is no clear objection, consensus is formed and recorded.
4. If there is substantive disagreement, the coordinator organizes a vote; a two-thirds majority carries.
5. Once approved, maintainers execute the decision and leave a record in CAMPAIGNS/.

## Contributor promotion

- Three consecutive months of constructive contribution with no code-of-conduct violations.
- Nominated by two maintainers and posted for 7 days in Discussions.
- Promotion is granted if there is no strong objection during the posting period.

## Leaving

- Any member may leave at any time without giving a reason.
- A maintainer inactive for three consecutive months becomes a contributor.
- Serious code-of-conduct violations are handled under section 4 of CODE_OF_CONDUCT.md.

## Route disagreements

If members reach an irreconcilable split between "moderate advocacy" and "hardline action", prefer a fork over infighting inside the repository. A forked project may not reuse the FAI or "AI Accountability Union" name.
