---
title: EXP-16 results
status: complete
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Group | Cases | Observed |
| --- | --- | --- |
| Fresh, pinned and refreshed ready inputs | `ready_fresh`, `stale_pinned`, `stale_refreshed` | One mock call each. Pinned kept the original graph ID and input; refreshed retained the new graph ID and changed input. |
| Unacknowledged staleness | `stale_no_choice` | Refused with no run reservation or mock call. |
| Open blocker and override | `opened_pinned`, `opened_refreshed`, `opened_override`, `override_missing_rationale`, `override_wrong_edge` | Both unoverridden choices refused. An exact-edge, nonempty rationale allowed one mock call and remained in the run and raw event. Missing rationale or wrong edge refused. |
| Hidden, unknown, cyclic and incomplete prerequisites | `hidden_open_blocker`, `unresolved_override`, `cycle_override`, `incomplete_source` | All refused with zero reservations or calls. The filtered selected item still reported `blocked` and retained its hidden context edge. |
| Mock grant binding | `grant_expired`, `grant_wrong_work`, `grant_wrong_graph`, `grant_wrong_runner`, `grant_unauthorized` | All refused before reservation or dispatch. |
| Mock runner outcome | `mock_runner_rejection`, `mock_runner_unknown` | One call and one durable run each. Run and trace refs remained, stream stayed partial, and no retry occurred. |

The frozen matrix contains 20 cases: four completed mock calls, 14 pre-dispatch refusals, one failed mock call and one unknown mock outcome. Every case matched its handwritten expected decision, and all durable-counter, retained-binding, snapshot-artifact and trace-identity checks were true. The current-source recheck prevented a stale pinned choice from bypassing a newly opened prerequisite. A changed but still-ready source required explicit pinned or refreshed choice; those choices retained different snapshot IDs (`1ba21698…` versus `93f30572…`).

This demonstrates that the installed snapshot and synthetic durable stores can be composed under an explicit mock preflight. The preflight and simple grant-field validation were written for the experiment, so a pass does **not** establish the real adapter's behavior, grant authenticity, native component version, authorization to launch, or model execution. EXP-03 failed native component attestation, and [#77](https://github.com/amadou-6e/laomedo/issues/77) owns fail-closed enforcement in the real stage adapter. No definitive blocker remains for the bounded mock experiment; the real integration is a separate no-go claim.
