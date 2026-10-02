# Run monitoring and agent traces

Status: proposed. Monitoring is a separate subsystem because a Langflow node
trace records the outer call, not necessarily the Codex or Claude activity
inside it. This document specifies stored evidence; a trace UI needs its own
view-owned Draw.io specification.

Current evidence: the
[local pilot](../implementation/local-skill-agent-pilot.md) retains matched
native commands, a completed skill read, and partial events from cancellation.
Real Langflow output carries run/thread and trace refs; inner usage remains
`unknown`. Automated skill-read projection, full normalized monitoring, and
browser inspection remain incomplete. AGENTVIZ is deferred for this iteration.

## Identity and event model

Allocate a Laomedo `run_id` before dispatch. Correlate it with flow
invocation ID, component ID, provider and native session ID, parent run or
draft ID, definition revision, input snapshot, skill revision, policy
revision, source and effective workspace snapshots, and last post-run
workspace snapshot. Keep both raw provider events and a
normalized event projection. A normalized event has:

| Field | Meaning |
| --- | --- |
| `event_id`, `run_id`, `sequence` | Stable identity and order within one run |
| `source` and `source_event_id` | Provider or runner origin and original ID if supplied |
| `kind` | Start, message, tool call/result, file change, skill access, approval, usage, error, end |
| `observed_at`, `source_time` | Receipt time and native timestamp when available |
| `payload_ref` | Stored raw payload, subject to access control |
| `provenance` | `observed`, `declared`, or `inferred`, with derivation for inference |

Store raw events append-only before deriving display records. Preserve native
ordering and equal timestamps using sequence and source IDs. Never invent a
missing tool result, skill read, or parent/child relationship. Event schemas
are versioned so later parsers can reproject stored raw traces without
changing the original evidence. Run status is a separate state machine:
`queued`, `running`, `completed`, `failed`, `cancelled`, `timed_out`, or
`interrupted`. A failed run can still have a final message and partial diff.

## Required inspection data

The run summary shows requested and effective model/effort, provider and
native session ID, start/end, status, limits, selected skill and file hashes,
permission grant, input/source/effective/post-run workspace refs, final
output, file diff, and usage or
cost only when supported. The event sequence allows inspection of messages,
tool arguments/results, errors, approvals, and observed skill access. It
links a skill draft to the edit run and its validation/evaluation runs.

“Offered skill” means the files were materialized or supplied in context.
“Used skill” requires source evidence of a read or invocation. If such
evidence is unavailable, usage is unknown. Langflow's trace links to the
Laomedo run; it is not treated as the only agent trace. AGENTVIZ import can
consume a derived export, but a derived graph must preserve event provenance.

## Reliability and access

Write a terminal status even if the provider exits unexpectedly. If event
capture stops early, mark the trace incomplete and retain the last sequence
number. A retry is a new run linked to the prior run. Duplicate provider
events from reconnect or resume must not create duplicate normalized events.
Usage totals, costs, and missing counters remain distinct from zero.

Prompts, files, tool output, and raw traces may contain sensitive data.
Restrict reads by run ownership and grant; keep credentials and tokens out of
event payloads and exports. Record any redaction as a transformation, not as
the original event. Exact retention and export rules remain open decisions.

## Acceptance

- Two flow executions produce separate run IDs and event histories.
- A tool call and its result remain linked when timestamps are equal or zero.
- A crash retains all received events and marks the trace incomplete.
- Codex and Claude traces expose common event kinds while preserving raw
  provider records and unsupported fields.
- A selected but unread skill is not labeled as observed usage.
- Reprojection after a parser change leaves raw events and run identity intact.
