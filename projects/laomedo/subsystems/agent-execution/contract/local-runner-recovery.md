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
commands, paths, credentials and arbitrary endpoints are never executed.
No configuration means an explanation with no recovery button. Unverified
listeners or authentication mismatches must not be replaced.

The error panel checks availability before offering recovery. Offline permits
one explicit restart request; while it is pending or starting, repeated clicks
are disabled. Polling reports readiness or failure and clears its own recovered alerts; the
original build error stays visible until dismissed.
Stale availability responses must not overwrite a newer restart state. A failed
restart retains an explicit API-only retry with actionable host guidance.

Restart launches only the configured API process. It neither dispatches nor
retries a graph/model operation, rewrites historical verification evidence nor
replaces an already-online listener. The error panel hides the generic graph
Retry action for this connection failure. After recovery, advise inspecting the
existing run before new work. Historical experiment limits are not persistent
service authorization gates; bound verification in a separate harness.
Technical details retain the safe original transport code and available allowlisted
run/request UUIDs without raw payloads. Recovery composes with the shared node-error
presenter in the app error panel only; node popovers keep descriptive errors without
recovery controls. One combined overlay owns the native error-panel transformation.
A health timeout is not proof of an offline process: probe the listener, and refuse
startup while a listener is present or its absence cannot be established.

## Popup placement and dismissal (implementation acceptance pending)

The selected A design and [shared popup standard](popup-cards.md) govern this
implementation slice. PR #183 implements the dedicated recovery popup; live
acceptance and the required independent review remain to be recorded. This is
not a claim that the branch is merged or that all popup cards conform.
The recovery popup must be anchored to the bottom-right of the visible viewport,
with 16 px insets plus device safe areas. Its width and height must fit the
available viewport at every resize, zoom level and on-screen keyboard change.
Long content and expanded diagnostics scroll inside the popup; its dismiss
control and action row stay visible. Multiple notifications stack upward within
a bounded scrollable region rather than overflowing the screen.

Provide a visible Dismiss or close control with an accessible name and keyboard
activation. Escape dismisses the focused popup and restores the previously focused element, or the canvas if it is unavailable.
The popup does not automatically dismiss. Dismissal closes only the notification: it does not cancel work, interrupt an
API restart or retry the graph. Geometry and narrow-screen examples are on the
**Popup placement and dismissal** page of the owning Draw.io.

## Acceptance and evidence

Check authentication, exact endpoint allowlisting, host-selected defaults,
repeated actions, failure feedback and stale overlapping polls. Verify the real
user path: actual transport failure, recovery button, real API availability,
and subsequent recorded-result inspection without a new model turn. Preserve
historical verification evidence without using it as runtime authorization.
Browser acceptance must use real integrations; fixtures are internal controls
only. Do not spend a model turn merely to demonstrate recovery; use a harness that
permits only the intended Status/API actions. Record live provider coverage and remaining gaps explicitly.

## Dependencies and authority

The shared presenter requires implementation PR #184 and its contract in specs
PR #392. Claude API startup additionally requires the adapter from implementation
PR #180; an installation without that adapter must use the supported Codex service.
The CLI uses the host's ordinary login; custom Claude profile directories are not
forwarded. Every authenticated app user can start the one configured API, so the
host operator must authorize those users for this control. Routed output failures
currently do not open the app build-error panel; this limitation is not live
acceptance for that path.
