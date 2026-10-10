---
title: Work Graph validation
status: draft
kind: validation
owners: [laomedo-maintainers]
last_reviewed: 2026-10-06
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph validation

## Release-interview target coverage

[Application execution](contract/application-execution.md) defines the next
Langflow-only demonstration and later application scope. Reuse existing issue
ingestion and frozen snapshots. No new end-to-end run was performed by the
interview repair; Output Contract/failure routing and downstream draft PR
publication require new composed acceptance. Standalone board/chat UI remains
parked by the owner, and existing bounded readiness evidence is unchanged.

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

Review of Laomedo PR #86 found that snapshot-ID grant binding made every
`refreshed` launch fail when the launch re-fetch changed only `fetched_at`.
The revised local ledger binds the reviewed work and transitive-prerequisite
content digest while keeping the reviewed snapshot ID for evidence. A
credential-free test issues a real ledger grant from changed reviewed content,
re-fetches the same content under another timestamp, and dispatches the
`refreshed` selection once. A changed-content negative control refuses before
reservation or grant consumption. Old snapshot-ID-only grants are not
redeemable after the schema update. This is a local run-scoping result, not
human authentication. The later product decision retired #95's separate
human-authentication requirement; any same-user process can mint this grant
and launch a stage. The historical test result is unchanged.
The implementation at [Laomedo `da1c88a`](https://github.com/amadou-6e/laomedo/commit/da1c88ae7f247be39fd51fc2d234b6a4ac3c8754)
merged into `develop` as [`d69c9a2`](https://github.com/amadou-6e/laomedo/commit/d69c9a26d5bd591d2e99fb7f4a76b825fc66c343).
Its host suite passed 172 tests with four optional-runtime skips; the
credential-free Docker grant probe passed, and both Python 3.10 and 3.13
installed-wheel CI jobs passed on rerun.

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

A [later hardening observation](https://github.com/amadou-6e/laomedo/blob/ce6af7a/experiments/exp82/hardening-observation.json)
shows that the one-use grant now binds to the host OS principal rather than a
caller-supplied name, refuses a different principal, and redirects ordinary
component `print` output away from the stage protocol. A crafted print-based
completion message was ignored. These checks do not prove human intent from
another same-principal host process or extend the zero-turn path to model
agents. A [further stdout control](https://github.com/amadou-6e/laomedo/blob/f54b45b/experiments/exp82/fd-observation.json)
also discarded a forged raw write to file descriptor 1 while preserving the
real output. Code sharing the worker process may still discover or manipulate
other open descriptors; adversarial protocol integrity remains unproven.
The worker also pins `--pull=never` and a numeric non-root user. This does not
expand the tested flow to untrusted custom component code; #96 owns that
boundary. The local CLI requires a disposable auto-login-enabled Langflow
server and cannot use the earlier auto-login-disabled deployment as-is.

For #96, test the host/executor split with a pinned zero-turn Docker fixture.
Freeze the expected graph and component digests on the host, then inject
component writes to ordinary stdout, raw file descriptor 1, enumerated open
descriptors and inherited pipes. A forged `ready` line must not reserve or
dispatch a stage when validation fails. A forged `complete` line followed by
a failing executor must not produce a completed run. Verify one durable
run/trace identity for dispatch failure and timeout, no replay, exact container
cleanup and unchanged image, user, network, mount and capability settings.
Report container output as untrusted data and distinguish a successful Docker
process exit from verified semantic execution.
Add a component that emits forged lines and attacker-chosen text, then calls
`os._exit(0)` before the graph output node. It should record `completed` only
on a `process_exit` basis with incomplete evidence, while keeping the forged
text confined to untrusted result data.
