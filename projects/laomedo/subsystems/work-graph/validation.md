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
| Content-based staleness and current-graph readiness at dispatch | Five credential-free product gate tests and one pinned Langflow synthetic stage test (2026-10-05) | Local adapter refused changed/unacknowledged content, blockers, unknown/cyclic/incomplete evidence and invalid synthetic grants before reservation; unchanged-content re-fetch did not demand a choice. Pinned runs kept distinct bound/authorization graph IDs. This does not prove live GitHub freshness or real grant authenticity. |

The current evidence does not establish UI, agent dispatch or automatic issue
state changes. The [contract](contract/work-graph.md) remains a broader target.
