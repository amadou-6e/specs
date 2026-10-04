---
title: Run traces validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Run traces validation

The newer [workflow, agent and result interfaces](contract/interfaces.md)
are design targets. Existing pilot events do not prove complete Langflow
reconnection, repeated invocation correlation or same-session crash recovery.

No implementation test was executed in this authoring migration. Evidence is bounded
by its original version, task, grant and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Matched tools / skill read | 2026-10-01 pilot | Native starts/results observed; returned label conservatively offered |
| Partial capture | Pilot cancellation | 39 events retained; crash/reconnect untested |
| Raw identity / projection | #123 | Codex import and synthetic tests; Claude trace absent |
| IF-08 at-least-once redelivery and action-identity uncertainty | [EXP-09 synthetic result](../../experiments/agent-event-replay/iterations/2026-10-04/results.md) | Identical redelivery, conflicting IDs, keyless reorder and separate invocations preserved in a pinned SQLite fixture; unique-action count stayed absent. Native provider replay, production adapter and UI are not tested |
| IF-07 lifecycle redelivery | No new check | T10 remains a separate choice; receipt sequence is not stable across redelivery |
| Inner usage / governance | Pilot and #123 | Usage unknown; retention/export/access policy open |

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
