---
title: Work Graph validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph validation

| Requirement | Current evidence | Status |
| --- | --- | --- |
| Import and preserve GitHub issue and native dependency evidence | [Laomedo PR #17](https://github.com/amadou-6e/laomedo/pull/17) connector tests and paginated live read | Observed for initial connector |
| Immutable snapshots and complete-graph readiness under filtering | PR #17 unit tests, installed-wheel test and CLI fixture import | Observed in read-only slice |
| Reviewed view-owned UI design and browser behavior | No reviewed Work Graph UI design or browser test | Pending |
| Explicit launch, run binding, rerun and resume | [#77](https://github.com/amadou-6e/laomedo/issues/77) frozen local stage adapter and [#82](https://github.com/amadou-6e/laomedo/issues/82) synthetic Work Graph gate checks | Partial local path; no production grant authority, live GitHub freshness check, saved-flow API integration or rerun/resume acceptance |
| Content-based staleness and current-graph readiness at dispatch | Nine credential-free product gate tests, one pinned Langflow synthetic stage test and a [read-only live GitHub refresh observation](https://github.com/amadou-6e/laomedo/blob/b589fec/experiments/exp82/observation.json) (2026-10-05) | Local adapter refused changed/unacknowledged content, blockers, unknown/cyclic/incomplete evidence and invalid synthetic grants before reservation; unchanged-content re-fetch and reordered dependency edges did not demand a choice. Pinned runs kept distinct bound/authorization graph IDs. Runner rejection and ambiguous timeout each retained one run/trace identity without replay, and a bypass negative control dispatched blocked work. A live source recheck on issue #82 returned complete evidence and refused before reservation because no grant authority was supplied. This does not prove production grant authenticity or an authorized real launch. |

The current evidence does not establish UI, agent dispatch or automatic issue
state changes. The [contract](contract/work-graph.md) remains a broader target.
