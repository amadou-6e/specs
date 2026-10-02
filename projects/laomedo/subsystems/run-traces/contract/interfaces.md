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

The deduplication, lifecycle-source and crash-durability guarantees below are
contested or unverified; see [decision readiness](../design/decision-readiness.md)
before implementing IF-07, IF-08 or IF-11.

## IF-07 — workflow lifecycle events

Consume events from [Langflow integration](../../langflow-integration/contract/interfaces.md):
run and graph revision identity, stage and invocation identity when applicable,
status transition, source event ID/time if supplied, and receipt time. Store
unknown native IDs explicitly. Reconnecting a UI must not start another run or
rewrite past events.

## IF-08 — agent activity events

Consume raw/native or normalized events from
[agent execution](../../agent-execution/contract/interfaces.md), correlated to
run, stage, invocation and native session. Distinct loop invocations have
separate event histories even when they use the same configured stage or
session. Keep partial events from crash, denial or interruption. Preserve
native source identifiers and receipt sequence so replay/deduplication does
not fabricate duplicate actions.

The execution overview reads agent invocation timing and status and opens
single-invocation telemetry. Its exact waterfall/card layout is undecided and
belongs to a view-owned Draw.io design. It is separate from the embedded
Langflow authoring/execution graph.

## IF-11 — trace and digest reference for results

Provide [results and artifacts](../../results-artifacts/contract/interfaces.md)
the trace identity, digest/projection reference, event-stream completeness,
last observed sequence and run/invocation correlation. An incomplete trace
must remain labeled incomplete even when an agent emitted a final message.
Unknown usage or cost is not recorded as zero.

The earlier [shared contract](../../../architecture/shared-contracts.md)
says a retry gets a new run identity. The newer
[decision record](../../../architecture/subsystem-decision-record.md) requires
up to three crash-recovery attempts within the same invocation and session.
Those may be distinct operations, but the identity and event sequence rules
must be reconciled before implementation. No raw telemetry content/retention
policy was settled by the interface discussion.

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
  stream_state: "complete" | "partial" | "unknown",
  invocations: [{ stage_id: string, invocation_id: string,
                  native_session_ref?: Ref, event_count: integer,
                  stream_state: "complete" | "partial" | "unknown" }],
  usage?: { value: number, unit: string, source: string }
}
```

`usage` is absent when unknown, not zero. `complete` describes evidence
receipt, not whether the agent achieved the user's goal. Content-retention
and native-to-normalized event projection remain open.
