---
title: Run-trace interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Run-trace interfaces

Run traces own raw event storage, normalized projections and correlation for
inspection. Their [existing event model](README.md#identity-and-event-model)
remains canonical draft detail. See the [interface map](../../README.md).

## IF-07 — workflow lifecycle events

Consume events from [Langflow integration](../../langflow-integration/contract/interfaces.md):
run and graph revision identity, stage and invocation identity when applicable,
status transition, source event ID/time if supplied, and receipt time. Store
unknown native IDs explicitly. Reconnecting a UI must not start another run or
rewrite past events. IF-07 source IDs may be absent; receipt sequence is
assigned after arrival and cannot identify a redelivery. Producer-stable keys,
or an explicit no-dedup policy with visible uncertainty, remain open.

The proposed [post-timeout reconciliation](../../langflow-integration/contract/timeout-reconciliation.md)
retains `408`, `JOB_FAILED` and a later effect as separate correlated receipts.
Neither a native terminal job status nor HTTP 500 proves that effects stopped.
The proposed [runner binding](../../langflow-integration/contract/runner-correlation.md)
adds a namespaced runner ID and private raw-event pointer to the already
reserved invocation. A missing runner acknowledgement leaves that identity
unknown, not an inferred match.

## IF-08 — agent activity events

Consume raw/native or normalized events from
[agent execution](../../agent-execution/contract/interfaces.md), correlated to
run, stage, invocation and native session. Distinct loop invocations have
separate event histories even when they use the same configured stage or
session. Keep partial events from crash, denial or interruption. Preserve
available native source identifiers and the separate receipt sequence. Neither
optional native IDs nor receipt order guarantee deduplication; mark potential
replays uncertain instead of silently counting them as distinct actions or
fabricating a stable identity. The first-slice policy is
[at-least-once receipts with explicit uncertainty](../../../decisions/0003-agent-event-replay.md):
retain every committed delivery, including conflicting repeated IDs. A
source-specific producer-key guarantee requires separate verification before
any deduplication. This choice does not settle IF-07 lifecycle deduplication.

The execution overview reads agent invocation timing and status and opens
single-invocation telemetry. Its exact waterfall/card layout is undecided and
belongs to a view-owned Draw.io design. It is separate from the embedded
Langflow authoring/execution graph.

## Selected first inspection slice, 2026-10-14

Historical first prototype, superseded by the user's 2026-10-15 direction below.
The PR-specific agent and its viewer toolbar coupling are removed from the product.

The user selected an Agent activity viewer in the app. For the native Codex PR
agent, its toolbar opens retained invocation history without dispatching an
agent or contacting GitHub. Show status, capture completeness, start/end times,
native session identity, received-event count, observed usage and ordered native
event receipts. Missing usage/session identity is unknown; event count is not
a unique-action count. Display native text as text, never executable markup.
Refresh reads the selected invocation; it does not change or restart it.

Host-enabled capture reserves a durable invocation identity before the native
process starts. Retain committed receipts from failed/cancelled/timed-out turns.
Each invocation has a new identity, even for the same flow node. Reads require
the signed-in owner and exact flow/node/invocation scope. Graph data cannot
choose the database path or read another owner's events. History is bounded to
the latest 50 invocations; events are paged in receipt order. No automatic expiry
or raw export is introduced.

This bounded slice captures the native CLI stream for the PR agent. It does not
complete the Docker runner bridge, Claude projection, crash-prefix experiments,
or the multi-agent overview. `complete` means clean local stream capture with a
native terminal event, not successful PR mutation or verified goal completion.
An unfinished stored invocation stays partial; a backend crash cannot be inferred
from an inspection request and must not cause redispatch.

## Selected graph-wide inspection direction, 2026-10-15

The Agents tab inspects all original-agent activity for one selected graph
execution on a shared Gantt timeline. Preserve node invocation, session and turn
identities, including repeated turns and observed subagents. Expand lanes for
messages, tools, errors and waiting intervals; selecting a segment opens readable
details. Render message text normally and JSON/code with highlighting and folding.
Use local time and relative durations, retaining exact timestamps for inspection.

Bind OpenTelemetry logs/spans/metrics to native execution events using verified
identifiers. Show input/output/cache token counts and monetary cost over time
when available, distinguishing provider vs calculated estimates from billing.
Unknown or redacted values remain explicit. Do not double-count cumulative token
snapshots or duplicate native/OTel representations. Parent relationships require
observed source identity; parallel execution alone does not establish parentage.

The [feasibility assessment](../design/graph-agent-observability.md) records real
host protocol observations and the original Docker-runner blocker. The editable
[Agents tab design](../design/agent-activity.drawio) replaces the one-node modal
as the target. Neither the design nor the earlier CLI adapter proves a working
graph-wide original-agent integration. That product acceptance remains open.

## IF-11 — trace and digest reference for results

Provide [results and artifacts](../../results-artifacts/contract/interfaces.md)
the trace identity, digest/projection reference, event-stream completeness,
last observed sequence and run/invocation correlation. An incomplete trace
must remain labeled incomplete even when an agent emitted a final message.
Unknown usage or cost is not recorded as zero.

The [shared contract](../../../architecture/shared-contracts.md) uses a new
run identity for a user-requested retry. The [decision record](../../../decisions/0002-subsystem-handoffs.md)
preserves automatic same-invocation crash recovery only as a **deferred
target**. The first slice does not restart a crashed turn. Before any later
recovery, the native-session restart experiment and event identity rules must
be reconciled. No raw telemetry content/retention policy was settled by the
interface discussion.

## Interrupted-trace retention

[Owner interview A14](../../../decisions/0006-release-packages.md) selects keeping
partial traces from failed/stopped runs until explicit user deletion, with no
automatic expiry. Keep run/invocation identity, source provenance and partial/
unknown completeness when the execution container is removed. Storage and
deletion mechanics, disk-pressure handling, redaction/export and retention for
other trace classes still need design. A retained partial trace is not resumable
workflow state or evidence that no external effect occurred.

## Approximate payload

IF-07 and IF-08 use the producer sketches in
[Langflow integration](../../langflow-integration/contract/interfaces.md#approximate-payloads)
and [agent execution](../../agent-execution/contract/schemas/if-08-agent-event.md).
The trace-to-results handoff is approximately (see
[notation](../../README.md#payload-sketch-conventions)):

```text
IF-11 TraceLink {
  run_id: string, trace_ref: Ref, digest_ref?: Ref,
  event_count: integer, last_received_sequence?: integer,
  action_uniqueness: "uncertain" | "verified",
  unique_action_count?: integer,
  stream_state: "complete" | "partial" | "unknown",
  invocations: [{ stage_id: string, invocation_id: string,
                  native_session_ref?: Ref, event_count: integer,
                  stream_state: "complete" | "partial" | "unknown" }],
  usage?: { value: number, unit: string, source: string }
}
```

`event_count` counts received deliveries, not unique native actions.
`unique_action_count` is absent while `action_uniqueness` is `uncertain`;
neither omission nor uncertainty means zero actions. `usage` is absent when
unknown, not zero. `complete` describes evidence
receipt, not whether the agent achieved the user's goal. Content-retention
and native-to-normalized event projection remain open.
