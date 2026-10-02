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
  recovery_attempt: integer, native_session_ref?: Ref,
  source_event_id?: string, source_sequence?: integer,
  observed_at?: timestamp,
  kind: string, payload_ref?: Ref, normalized_summary?: string
}
```

`recovery_attempt` is within one invocation; zero denotes the initial attempt.
Run traces assigns receipt time and sequence on ingest. This event does not
claim whole-stream completeness. Native event taxonomy, content retention and
projection rules remain open.
