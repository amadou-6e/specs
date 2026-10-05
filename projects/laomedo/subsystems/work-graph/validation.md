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
| Explicit launch, run binding, rerun and resume | [#77](https://github.com/amadou-6e/laomedo/issues/77) frozen local stage adapter and [#82](https://github.com/amadou-6e/laomedo/issues/82) Work Graph gate and zero-turn Docker checks | Live GitHub freshness, saved-flow API and isolated local stage combined for one no-model run; operator authentication, model-backed grants, rerun/resume and hosted acceptance remain unverified |
| Content-based staleness and current-graph readiness at dispatch | Nine credential-free product gate tests, two pinned Langflow synthetic stage tests and a [read-only live GitHub refresh observation](https://github.com/amadou-6e/laomedo/blob/b589fec/experiments/exp82/observation.json) (2026-10-05) | Local adapter refused changed/unacknowledged content, blockers, unknown/cyclic/incomplete evidence and invalid synthetic grants before reservation; unchanged-content re-fetch and reordered dependency edges did not demand a choice. Pinned runs kept distinct bound/authorization graph IDs. Runner rejection and ambiguous timeout each retained one run/trace identity without replay, and a bypass negative control dispatched blocked work. A callable saved-flow entrypoint passed a built graph through the product gate with a synthetic GitHub source and grant. A live source recheck on issue #82 returned complete evidence and refused before reservation because no grant authority was supplied. This does not prove production grant authenticity or an authorized real launch. |

The current evidence does not establish UI, agent dispatch or automatic issue
state changes. The [contract](contract/work-graph.md) remains a broader target.

The local #82 branch also has a one-use SQLite grant ledger and typed work-key
confirmation CLI. Credential-free tests refuse an in-repository grant path,
a mismatched graph and replay. The first pinned Langflow fixture executed
in-process and did not establish isolation.

A subsequent zero-turn Docker route, recorded in the
[sanitized isolated observation](https://github.com/amadou-6e/laomedo/blob/74b4b8b/experiments/exp82/isolated-observation.json), kept the grant ledger, GitHub login and
disposable Langflow API token on the host. A worker with network disabled,
read-only package/flow mounts and scratch tmpfs reported graph/component
hashes before reservation. The host recorded one dispatch and the expected
no-model output. A one-second timeout left the run `unknown` with one attempt,
and the named container was absent afterwards. A disposable-server run then
combined a live read-only GitHub re-fetch, saved-flow API export, grant
redemption and Docker stage; the installed CLI path completed the same
zero-turn route without printing the API token. These are local integration
observations, not proof of an authenticated human operator, Windows ACL
isolation, resistance to forged worker protocol messages from malicious
component code, model-turn enforcement or a hosted/multi-user launch.
