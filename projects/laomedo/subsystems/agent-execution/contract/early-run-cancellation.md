---
title: Early runner identity and cancellation handoff
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Early runner identity and cancellation handoff

This is the proposed additive boundary for [Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22).
The existing synchronous `POST /v1/runs` and resume path remain supported;
they do not acquire early identity retroactively. The first slice covers a
fresh Codex run on the authenticated, single-user local runner. It does not
redesign Docker permissions, model login, hosted tenancy or Langflow's graph
scheduler. The prospective [zero-model protocol](https://github.com/amadou-6e/laomedo/blob/7975ffaa1555d7baf39880a578128724e5a08f50/experiments/exp22/PROTOCOL.md)
is not execution evidence.

## Start and identity

`POST /v1/runs/async` accepts the same fresh-run body as the synchronous
endpoint plus a caller-generated canonical UUID `request_id`. The ID binds
the **complete canonical request** for this local runner, not one HTTP POST
attempt. Validate the request and skill references before dispatch. Persist a
new `run_id`, request ID/hash, status `prepared`, raw-event location and the
frozen input/skill snapshot before acknowledging. The authenticated response
is HTTP 202 with that queryable run ID and no claim that a model turn started
or finished. The worker may start only after the response is sent or its
transport attempt has conclusively ended. The same ID and identical body
returns the same run record without a second worker or model turn, even if
the first response was lost or the run became terminal; the same ID with a
different body returns HTTP 409. A different request ID is a new run, not a
safe retry of an uncertain one.

`GET /v1/runs/{run_id}` reports the saved state (`prepared`, `running`, or
terminal `completed|cancelled|failed|timeout|interrupted`) and known native
IDs/partial raw-event reference. Polling is read-only and does not dispatch.
A runner restart marks saved nonterminal runs `interrupted` (or explicitly
unknown if their fate cannot be resolved), preserves their IDs/events and
never automatically resumes or replays them. An acknowledgment timeout must
be resolved with the **same** `request_id`, not an uncorrelated new POST.

## Cancellation and evidence

`POST /v1/runs/{run_id}/cancel` for `prepared` may atomically prevent worker
creation/turn dispatch and report `cancelled` with positive local evidence.
For `running`, HTTP 202 means only `cancel_requested`; the runner must attempt
its supported native interrupt and container teardown. The consumer polls the
run record and reports remote cancellation only after the runner confirms
`cancelled` and retains the native/teardown evidence. A timeout, disconnected
client, Langflow `JOB_FAILED`, accepted cancel request, or missing run ID is
not confirmation. A terminal completed/failed/timeout record is not rewritten
to cancelled by a late request. Raw events committed before stop remain
queryable. A cancel/turn-start race must end in an explicit recorded outcome;
it cannot silently dispatch another turn.

The Langflow Codex node may expose an additive nonblocking start operation
that returns the early run reference, followed by its existing status/cancel
operations. A graph that waits for completion must retain that ID while
polling and must not treat cancellation of its own HTTP wait as remote stop.
The bounded controller must save the acknowledged ID before it resumes its
completion wait. If Stop was requested before acknowledgement, it forwards
that request as soon as the ID becomes available; it does not discard Stop or
claim a remote stop without the runner's terminal evidence.
Langflow UI Stop propagation has bounded installed-runtime observations below.
Do not generalize them to other components or outage points without evidence.

## Playground invocation join

For a visible Playground Send, Langflow starts the graph before the Codex
component contacts Laomedo. The first component-to-host bridge call is the
earliest available reservation point on this route. The component sends one
canonical client UUID, resolved runner inputs, saved-flow ID, observed graph
run ID, and stage ID. The host independently reads the saved-flow export,
reserves a Laomedo run, trace, invocation and frozen runner request, then
mints a distinct runner request UUID before its first native POST. A same-UUID,
same-body retry returns the original record without another POST. A changed
body conflicts. A failed or uncertain native POST is never replayed
automatically.

The saved-flow revision and the component-reported graph run ID are separate
fields. A saved export does not attest the graph currently executing in the
Playground editor. Record `executing_graph_verified=false` until a trusted
Langflow build boundary proves that identity. The component and its outputs
cannot declare completion or evidence completeness for the host. The host
accepts the native run ID and event reference only under the exact frozen
request binding. Native terminal status may be projected into the Laomedo
record with `completion_basis=native_runner_status` and
`evidence_complete=false`; semantic output verification is separate.

Stop addresses the client UUID. If Stop arrives before the host has seen that
UUID, the host persists an intent. A later first call with the same UUID is
reserved and immediately cancelled without any native POST. The intent
survives a host restart. If no POST has begun, the host cancels the reservation
without creating a native run. Once a POST may have reached the runner, the
host resolves only the frozen native request UUID through read-only lookup,
then cancels the exact bound run. A lookup returning `not found` is not proof
that an in-flight POST never arrived and must not be recorded as a successful
cancel. A lost acknowledgement remains `unknown` until the native request is
positively found and reconciled, or its non-execution is independently proven;
timeouts and repeated `not found` responses alone cannot prove that. The
host keeps the Stop intent and uses later read-only status or lookup calls to
reconcile; if the native run appears, it cancels that exact run. The frozen
turn still counts against its cap and is never redispatched. A restart
reopens the host ledger and Stop intent but does not trigger redispatch. The
client UUID, Laomedo run and trace IDs, invocation ID, native request/run IDs
and raw-event reference must remain queryable together when issued.

This bridge is an opt-in local route using the selected provider login and
existing runner turn limit. Its bearer token is local access control, not a
second operator sign-in or a same-user approval boundary. Activating it or
changing a saved flow's endpoint is a separate configuration action. A
credential-free fake runner proves routing and persistence; completing #22's
join claim requires a pinned installed Langflow run, process restart, exact
cross-store evidence and a bounded real-agent observation. Tests must include
Stop arriving before the first bridge call, after reservation, and during an
uncertain native POST, including a `not found` lookup while that POST is still
in flight.

## Acceptance boundary

Credential-free fake-transport and authenticated local-HTTP tests must cover
early acknowledgment, duplicate/lost-response identity, conflicting payload,
cancel before worker and during a blocked tool call, timeout/cancel races,
restart fencing, preserved partial events and turn-ledger counts. An explicit
negative control must fail if a second turn starts. These checks establish
the local mechanism only. Real-agent acceptance additionally requires a
separately frozen cap and positive native cancellation/container evidence for
both pre-thread and active-tool points, linked to IF-06/07 partial trace.
[Q11](../../langflow-integration/design/decision-readiness.md) remains open
until those observations exist.

The [2026-10-08 Phase C observation](../../../experiments/orphan-lease/iterations/2026-10-08/results.md) provides direct-runner native active-tool interrupt and exact-container stop evidence. It does not verify Langflow UI Stop propagation or the complete cross-store trace join, so this target contract is not marked fully accepted.

The later [2026-10-09 installed-graph result](../../../experiments/early-run-cancellation/iterations/2026-10-09/results.md) adds one real Codex turn cancelled by the pinned Langflow graph, with an exact request lookup/cancel audit, native `interrupted`, terminal confirmed runner cancellation and exact-container absence. It did not click the visible Playground Stop or establish the durable Langflow invocation-to-runner trace join. The target contract remains only partially observed.

The separate [visible Playground Stop result](../../../experiments/early-run-cancellation/iterations/2026-10-09-visible-stop/results.md) composes the browser click with one real Codex active-tool cancellation. Exact runner route identity, click-to-cancel-to-terminal ordering before browser disconnect, native `interrupted`, terminal confirmed cancellation, partial events and exact-container absence passed in that bounded local case. It still does not supply the durable Langflow invocation-to-runner cross-store trace join or the separate pre-thread real-agent point; the target contract remains partially observed.

The later [prepared-state visible Stop result](../../../experiments/early-run-cancellation/iterations/2026-10-09-prethread-stop/results.md) exercises the pre-thread point with a real runner record and a held acknowledgement. One visible click led to exact lookup and cancel before the native worker gate opened; no native model call or container launch followed. The active-tool and pre-thread points now have separate bounded positive observations. A durable Langflow invocation-to-runner cross-store trace join, and the broader #93 outage/credential checks, remain unverified; the target contract is still not fully accepted.

The later [host-join result](../../../experiments/early-run-cancellation/iterations/2026-10-09-host-join/results.md)
observed a durable Langflow/Laomedo/real-Codex identity binding across a
disposable server restart. The native turn failed before the task's first tool
call and the browser did not click Stop, so it does not compose that join with
the earlier positive Stop cases. The executing editor graph is not attested;
the target contract and #22/Q11 remain open.
