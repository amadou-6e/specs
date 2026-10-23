---
title: Local runner API recovery from connection errors
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-23
applies_to: [laomedo]
supersedes: null
related: []
---

# Local runner API recovery from connection errors

Tracks [Laomedo #182](https://github.com/amadou-6e/laomedo/issues/182) and
[implementation PR #183](https://github.com/amadou-6e/laomedo/pull/183).
The [editable recovery states](../design/local-runner-recovery.drawio) own UI
geometry, controls and transitions. General failure semantics belong to
[descriptive node errors](node-errors.md).

A local runner transport error offers **Restart local backend** in the app's
connection-error panel. Recovery is not a graph element, node setting, canvas
banner or Agent activity control. It does not require nodes, graph wiring or
browser-supplied runner URLs. The app's live backend handles recovery of the
separate local runner API; restarting Langflow itself is outside this contract.

The trusted host selects exactly one configured runner service. Authenticated
status/start routes resolve that configuration when no URL is supplied. Legacy
explicit URLs must still match the exact configured loopback endpoint; browser
commands, paths, credentials, budgets and arbitrary endpoints are never executed.
No configuration means an explanation with no recovery button. Unverified
listeners or authentication mismatches must not be replaced.

The error panel checks availability before offering recovery. Offline permits
one explicit restart request; while it is pending or starting, repeated clicks
are disabled. Polling reports readiness or failure and clears recovered errors.
Stale availability responses must not overwrite a newer restart state. A failed
restart retains an explicit API-only retry with actionable host guidance.

Restart launches only the configured API process. It neither dispatches nor
retries a graph/model operation, changes an allowance, resets a ledger nor
replaces an already-online listener. The error panel hides the generic graph
Retry action for this connection failure. After recovery, advise inspecting the
existing run before new work; report exhaustion separately from offline state.
Recorded results remain available after the approved allowance is exhausted.
Technical details retain the safe original transport code without raw payloads.

## Acceptance and evidence

Check authentication, exact endpoint allowlisting, host-selected defaults,
repeated actions, failure feedback and stale overlapping polls. Verify the real
user path: actual transport failure, recovery button, real API availability,
and subsequent recorded-result inspection with unchanged ledger and allowance.
Browser acceptance must use real integrations; fixtures are internal controls
only. Do not spend a model turn or change authorization merely to demonstrate
recovery. Record live provider coverage and remaining gaps explicitly.
