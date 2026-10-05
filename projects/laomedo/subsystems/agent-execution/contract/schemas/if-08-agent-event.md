---
title: IF-08 agent event payload
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# IF-08: agent event

Agent execution sends an event to [run traces](../../../run-traces/contract/interfaces.md).
See the [interface contract](../interfaces.md#if-08--emit-agent-telemetry).

```text
AgentEvent {
  run_id: string, stage_id: string, invocation_id: string,
  native_session_ref?: Ref,
  source_event_id?: string, source_sequence?: integer,
  observed_at?: timestamp,
  kind: string, payload_ref?: Ref, normalized_summary?: string
}
```

The first slice does not automatically restart a crashed invocation. Run traces
assigns receipt time and sequence on ingest, but that receipt sequence changes
on redelivery and cannot prove event identity. `source_event_id` and
`source_sequence` are optional native fields: when absent, do not invent a
producer-stable key or promise deduplication. Under the first-slice
[T07 policy](../../../run-traces/contract/interfaces.md#if-08--agent-activity-events),
preserve every committed raw delivery with explicit action-identity uncertainty;
do not silently collapse conflicting payloads or report a confirmed unique
action count from optional IDs. This event does not claim whole-stream
completeness. Native event taxonomy, content retention, source-specific key
verification and detailed projection rules remain open; the policy still
requires [EXP-09](https://github.com/amadou-6e/laomedo/issues/39) evidence.
