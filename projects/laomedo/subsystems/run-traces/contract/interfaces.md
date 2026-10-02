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
