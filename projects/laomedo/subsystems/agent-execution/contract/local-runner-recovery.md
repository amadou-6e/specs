---
title: Local runner API recovery from connection errors
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-25
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

A local runner transport error opens prerequisite-aware recovery in the app's
connection-error panel. Offer **Start local runner** only after Docker is healthy
and the configured runner is confirmed offline. Recovery is not a graph element, node setting, canvas
banner or Agent activity control. It does not require nodes, graph wiring or
browser-supplied runner URLs. The app's live backend handles recovery of the
separate local runner API; restarting Langflow itself is outside this contract.

The trusted host selects exactly one configured runner service. Authenticated
status/start routes resolve that configuration when no URL is supplied. Legacy
explicit URLs must still match the exact configured loopback endpoint; browser
commands, paths, credentials and arbitrary endpoints are never executed.
No configuration means an explanation with no recovery button. Unverified
listeners or authentication mismatches must not be replaced.

The error panel checks Docker prerequisites and runner availability before offering
recovery. Confirmed runner-offline with healthy Docker permits one explicit start request; while it is pending or starting, repeated clicks
are disabled. Polling reports readiness or failure and clears its own recovered alerts; the
original build error stays visible until dismissed.
Stale availability responses must not overwrite a newer restart state. A failed
restart reports what happened without referring to a separate operator or inventing a fix.

Restart launches only the configured API process. It never dispatches or retries an Agent task or graph execution, rewrites historical verification evidence nor
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

## Prepared native Codex app launch

The prepared-installation `laomedo-app` command accepts explicit trusted-host
paths for the runner-service JSON, matching built frontend, component directory
and persistent app state. It is a native single-user loopback launch path, not
an installer or a hosted identity boundary. Runtime data and the host file stay
outside Git. Missing host configuration, frontend or component assets, a missing
source directory or absent supervisor binding refuse this launch before the app
binds. App and runner ports must differ.

The command derives the recovery service file, Codex API token path
(`runner state/api-token`), registry and default endpoint for new Codex nodes
from that one host configuration. Neither token contents nor credentials appear
in command arguments or graph data. Explicit CLI arguments are authoritative;
dotenv, secret-directory and ambient launch-setting overrides cannot retarget
them. The app binds only to `127.0.0.1`, using the existing explicit local
auto-login mode. This is not private multi-user access or GitHub account login.

The normal Codex default image/version pins remain enforced. A trusted operator
may provide the existing CLI's full `sha256:` `image_id` for a reviewed local
rebuild; reject malformed identities, other providers and Git-workspace image
overrides. Recovery forwards the exact ID to normal preflight, which verifies
the local tag/immutable identity and CLI version without login material before
opening the API. Browser values never select an image or bypass this check.
The absolute `lease_service` path binds normal Codex execution to an independently
started supervisor; the app and runner do not start that supervisor as a runner
child. Existing Claude configuration and other provider launch paths are unchanged.

Starting the app does not start the runner, submit a graph/task, provision login
or declare the model list available. The existing explicit recovery action still
owns runner startup and authenticated readiness. Model refresh establishes
discovery only when the real model list loads; it submits no Agent task. No
configuration retains the existing unmanaged state and no Start action; guidance
must describe the configuration needed rather than promise an unavailable action.
Recovery requests from the current app use the host-selected service without a
node URL. Legacy explicitly supplied service URLs must still match exactly.

New Codex nodes use the derived loopback endpoint. Saved graphs retain their
Runner URL and selections; opening them does not silently migrate values. A
saved endpoint from another installation must be checked explicitly. The app
retains the selected state's existing `flow.db` and signing-key state. Activity
defaults to `state/activity.db` so sibling installations do not share a new
database; an explicit private `--activity-db` path retains an existing database
stored elsewhere. Do not silently copy or merge activity histories.

Closing the app does not terminate the independent runner, supervisor or active
work. Automatic dependency/frontend preparation, credential provisioning,
installation-wide stop and full first-use readiness remain separate work in
[Laomedo #204](https://github.com/amadou-6e/laomedo/issues/204). This increment
does not establish PR/Skill-service configuration or full graph execution.

Acceptance must separately verify same-file token/endpoint bindings, persistence,
invalid setup and port conflicts, actual Start and model refresh with no task,
and truthful managed/unmanaged guidance. Fixture controls support these checks
but do not replace the actual browser/runner path or owner validation.

## Docker prerequisites and recovery actions

The **Docker prerequisites** page in the owning Draw.io specifies the additional
states and action hierarchy. The following copy is normative; implementation and
live acceptance are tracked separately in validation.md.

| Confirmed condition | Recovery code and title | Explanation and recovery | Available action |
| --- | --- | --- | --- |
| Docker executable unavailable to the app | `runner_docker_not_installed` — **Docker is not available** | “The app could not find Docker on this machine.” “Install Docker, or make your existing installation available to this app.” | **Install Docker** links to <https://docs.docker.com/get-started/get-docker/>; **Dismiss**. |
| Executable exists; configured engine cannot be reached | `runner_docker_unavailable` — **Docker is not running** | “The configured Docker engine could not be reached.” “Start Docker Desktop (or the Docker service for this context), then wait until it is ready.” | Prompt the user to start Docker; **Dismiss**. No runner-start control. |
| Docker engine healthy; configured runner endpoint confirmed offline | `runner_local_offline` — **Local runner is offline** | “Docker is ready, but the local runner is not running.” | **Start local runner** invokes the host-configured local start route; **Dismiss**. |
| Docker health times out, access is denied, or the check is ambiguous | `runner_docker_check_unconfirmed` — **Docker availability is unconfirmed** | “The app could not confirm whether Docker is ready.” “Check Docker Desktop and this app’s access to Docker.” | **Dismiss**; no install claim or runner-start control. |

Every state retains the affected node and operation beside its title. For Docker
prerequisites and runner-offline states, retain one compact sentence: "The previous
run's outcome is unconfirmed." A recovered service does not resolve the old run.
The install action indicates an external destination and has the accessible name
"Install Docker (opens in a new tab)". Its action row stays separate from the text.

Precedence is explicit: (1) no trusted configuration means unmanaged, with no
Docker/start controls; (2) an unknown listener or authentication/provider mismatch
means identity unverified, and must never be replaced; (3) an owned starting or
cancelling process retains its busy state without another prerequisite check;
(4) a matching ready runner is identified separately from Docker readiness: if
Docker is unavailable show its prerequisite recovery while retaining
`runner_state: ready`, never claim the runner is offline or offer Start;
(5) only a confirmed absent runner listener plus healthy Docker permits Start.
A Docker failure accompanying a confirmed offline runner retains
`runner_state: offline`. Remote Docker contexts use the same host-selected context;
copy refers to the configured engine/service, not a guessed local process.

The missing-executable condition must not be presented as proof that Docker was
uninstalled: an existing installation might not be on the app's PATH. The stable
code is retained, while the title and explanation state only what was observed.
The install link is a fixed, official destination; it does not download, install
or open an elevated installer automatically. Launching Docker is a user action,
not a hidden side effect of recovery. If a server-side check is unavailable, do
not infer Docker's state from a failed runner HTTP request alone.

Docker checks use the trusted host's Docker context and environment, never a URL,
command, executable or arguments supplied by the browser or model. Read-only
checks are bounded; permission failures, malformed replies and timeouts fail to
the unconfirmed state. No raw CLI stderr, filesystem paths, credentials, URLs or
stack traces enter the popup or notification history. Technical details retain
the original `runner_transport_failed` and safe node/operation/run/request ids;
add the separately allowlisted `recovery_code` without replacing the original.

The app polls for prerequisite changes while the panel is open, at no more than
one Docker check per two seconds. Docker checks have a five-second process
deadline, a short cached result, and single-flight exclusion; a concurrent caller
gets an unconfirmed state instead of waiting behind another slow check. Never
probe Docker during an owned runner startup/cancellation. The card updates
automatically when Docker becomes ready. Starting Docker
or completing installation does not retry the graph. Once Docker is confirmed
healthy and no runner listener exists, reveal **Start local runner**. Recheck
Docker immediately before spawning, even if a recent UI poll said it was ready.
An existing unverified listener or authentication mismatch remains protected.
Never start a duplicate service while a prior start or cancellation is pending.

Starting the runner shows a throbber and **Cancel**, with no stale failure advice
or Technical details. A start response is an acknowledgement, not readiness.
Only an authenticated, matching-provider ready health response permits the online
state. An unsuccessful process exit shows a descriptive failure; it must not keep
spinning indefinitely or refer to a nonexistent operator. If Docker becomes
unavailable, return to the matching prerequisite message. When online, say
“The local runner is online. Check the existing run before starting new work.”
Do not retain “Once reconnected” or duplicate the same recovery advice.

All four recovery codes require shared catalogue entries and explicit safe
`recovery_code` coverage. Regression checks must cover both the prerequisite
producer and the runner-service producer, not rely on Agent-only coverage. Test
fallback, original-code preservation, redaction, state precedence and spawn-time
rechecks. Missing code mappings or a recovery control that is not available block
acceptance. The new Draw.io page includes online and start-failure states and
explicitly reuses the existing **Busy states and cancellation** behavior.

## Execution and graph outcome integrity

Graph build completion is not proof that the Agent executed successfully. A
Status operation reads an existing run; it must not be described as a new Agent
execution or used as acceptance for Fresh/Start/Resume. A runner transport failure
must show a failed or unconfirmed outcome with its descriptive recovery panel,
not a successful completion merely because the graph request returned HTTP 200.
An observed `RUN_ERROR` or failed node result remains a failure if a later
`RUN_FINISHED` closes the event stream. End-of-stream, a start acknowledgement,
old completed receipts and a recovered service must never promote that failure
to success. Recovery never silently redispatches the original operation.

## Popup placement and dismissal (implementation acceptance pending)

The selected A design and [shared popup standard](popup-cards.md) govern this
implementation slice. PR #183 implements the dedicated recovery popup; live
acceptance and the required independent review remain to be recorded. This is
not a claim that the branch is merged or that all popup cards conform.
The recovery popup must be anchored to the bottom-right of the visible viewport,
with 16 px insets plus device safe areas. Its width and height must fit the
available viewport at every resize, zoom level and on-screen keyboard change.
Long content and expanded diagnostics scroll inside the popup; its dismiss
control and action row stay visible. The cross-surface stack is a follow-up requirement owned by Laomedo #186,
as recorded in [the shared popup standard](popup-cards.md); it is not
implemented by this single-popup slice.

Provide Dismiss while idle and Cancel while checking, restarting or cancelling,
with an accessible name and keyboard activation. Escape invokes that same state-appropriate action. Closing restores the previously focused element, or the canvas if unavailable.
The popup does not automatically dismiss. Dismissal closes only the notification: it does not cancel work, interrupt an
API restart or retry the graph. The separate busy-state Cancel action below
requests startup cancellation and closes only after confirmation. Geometry and narrow-screen examples are on the
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
The managed service and installed adapter must use the same launch contract.
The container-based Claude adapter requires its configured image, an authenticated
dedicated Claude profile volume, and a running independent lease supervisor at the
configured path. The app must not combine container launch arguments with the older
host-executable adapter. Custom host Claude profile directories are not forwarded,
and recovery must not copy login material. Every authenticated app user can start
the one configured API; the machine owner controls who can access the local app.
Routed output failures
currently do not open the app build-error panel; this limitation is not live
acceptance for that path.


## Cancelling connection checks and startup

While checking or restarting, show a spinner and **Cancel** instead of Dismiss.
Hide recovery guidance, stale alerts and Technical details during that busy state.
Cancelling an initial connection check closes the panel and aborts its polling.
Cancelling a restart sends an authenticated `POST /api/v1/laomedo/runner-service/cancel-start`
with the manager-issued `startup_id`; it is not graph/model cancellation.

The manager accepts only the matching, owned startup attempt, before its API
listener opens. Listener publication and cancellation share an OS file lock,
preventing listener publication after an accepted cancellation. Cancellation is
cooperative: initialization and its child-process cleanup finish, then the API
exits before binding. A ready, unknown or different process is never terminated.
Show Cancelling until the process exit is confirmed, retaining a descriptive
unconfirmed outcome if confirmation times out. The panel closes after confirmed startup cancellation; a failed or
late cancellation reports its outcome and keeps the panel available. No automatic
restart, replacement process, graph retry or model request follows cancellation.
These cancellation changes require fresh real-path and reviewer validation before
acceptance; earlier restart evidence does not establish cancellation behavior.

Startup-control lock/marker files are local attempt metadata, not authorization
gates or experiment allowances. Windows OS locking can time out; that produces
an unconfirmed result rather than bypassing readiness coordination.

Recovery status, start and cancellation HTTP requests use a 10-second request
timeout. A request timeout ends the optimistic busy indicator and reports an
unconfirmed outcome; it must not preserve a stale starting snapshot or block
future status polling indefinitely. A timeout is not proof of backend readiness,
process termination or remote graph cancellation.

The recovery request deadline covers the entire client promise, including
authentication and response/error interceptors. A network-only timeout is
insufficient when an interceptor itself never settles. Preserve a completed
startup response independently of React rendering so Cancel can identify its
attempt between request completion and the next rendered state.


## Existing error popup migration

The Draw.io `Shared error popup` page extends A to node Error details, ordinary
flow failures and application error notifications. They share its compact card,
light red left contour and visible-viewport bottom-right stack. Primary actions and dismissal stay in
the footer; the subtle copy icon sits in the header. Concurrent cards scroll within viewport bounds. No automatic expiry
or click-on-text dismissal interferes with reading, selecting or copying.

Copy error includes the shared explanation, recovery and safe diagnostics only.
Unrecognized Laomedo failures retain the safe Agent fallback and original safe
code. Native application errors retain their own title and every message in the
shared card; they do not receive Agent-specific run or runner guidance. Obvious
credential values, trace lines and structured technical payloads are omitted. Clipboard success is confirmed
before showing the brief checkmark; failure offers manual selection through the icon tooltip and screen-reader status. Dismiss and Escape close
a card. Node details focus an already-open matching error rather than duplicating
it. Transport failures retain the recovery controls and cancellation semantics.
The matching native flow toast is omitted when the graph card already presents
the same event; notification history retains the safe description and code.

Error cards use a subtle header copy icon rather than a labelled footer button.
Successful copying swaps the icon for a checkmark for two seconds; it never adds
a visible Copied text row or changes card height. The accessible name/tooltip and
screen-reader status acknowledge success or failure. Recovery copies only safe
diagnostics; ordinary cards copy the explanation and safe diagnostics. Burst coalescing and a queue cap are
not implemented in this slice; concurrent cards remain viewport-bound and scroll.


### Confirmed recovery colour

Keep the card's left contour light red (`#F87171`) during checking, startup,
prerequisite failures and unconfirmed outcomes. After the authenticated service
check reports `ready`, with no pending check or error, change that contour to
light green (`#4ADE80`). A process being spawned or a spinner stopping is not
proof of readiness. Retain the text confirmation, safe details and Dismiss;
colour alone does not communicate success. A later failed check restores red.
This indicates restored connectivity, not completion or automatic retry of the
previous graph run.

## Model catalogue recovery after explicit startup

When a node reports `runner_model_catalog_unavailable_check_runner_connection`, its Start local runner action starts only the trusted configured runner. Once that explicit startup reaches authenticated ready state, automatically request the existing read-only model catalogue refresh for that same node exactly once. Do not require a second manual refresh and never execute the graph or submit an Agent task. Initial readiness polling alone must not trigger discovery.

While discovery is pending, show Loading available models. Dismiss the notice only after that node reports catalogue-loaded. If discovery fails, keep the notice and explicit Refresh models retry available; do not restart an already-online runner. Confirmed failed startup, cancellation, node replacement and unrelated run recovery must not trigger automatic discovery. An unconfirmed start response or transient status failure preserves the explicit read-only recovery intent for at most two minutes: continue checking readiness and refresh once only if authenticated ready is confirmed within that window. Do not replay the start request. Expiry clears the automatic intent and leaves manual recovery available. Scope retry intent to the originating node and clear it before dispatch to prevent repeated refreshes on polling.

The editable design page Model catalogue startup recovery owns these transitions; existing transport/run recovery and cancellation semantics remain unchanged.
