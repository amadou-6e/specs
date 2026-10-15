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
| IF-08 at-least-once redelivery and action-identity uncertainty | [EXP-09 synthetic result](../../experiments/agent-event-replay/iterations/2026-10-04/results.md) | Pinned SQLite fixture preserves redelivery, conflicts, reorder and separate invocations. Amended negative control rejects the historical projector's dropped receipt and a fabricated unique-action count. Native provider replay, production adapter and UI are not tested |
| IF-07 lifecycle redelivery | No new check | T10 remains a separate choice; receipt sequence is not stable across redelivery |
| Inner usage / governance | Pilot and #123 | Usage unknown; retention/export/access policy open |

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.

## Native Codex activity viewer, 2026-10-14

Historical observation of a PR-specific prototype, not original-agent acceptance.
The user selected removal of that adapter from the product on 2026-10-15.

The user selected the in-app Agent activity viewer. The implemented slice is
bounded by the [inspection contract](contract/interfaces.md#selected-first-inspection-slice-2026-10-14)
and [editable modal design](design/agent-activity.drawio).

A real native Codex CLI turn ran through the local Langflow build/events API,
using actual PR context read through the connected GitHub integration. The
inspection flow contained only the native agent; its proposed operation was not
connected to a GitHub write node. One turn completed, four native JSON receipts
were retained, native session identity and usage were present, and the stored
local stream closed as complete. This establishes this native capture path,
not PR mutation acceptance or general provider completeness.

Edge opened the actual app's node toolbar viewer and displayed the retained
native events, session and usage. Refresh caused zero build requests. The
[reference screenshot](design/references/agent-activity-native.png) records this real
inspection. The production frontend build passed. Seven internal storage/API
tests and three viewer tests passed; these separately cover owner isolation,
receipt preservation/pagination, partial retention, unknown usage, empty/error
states and plain-text rendering. Three existing PR inspection tests also passed.
Jest required a temporary Node resolver wrapper for Windows file resolution;
the production overlay does not include that workaround.

The existing PR inspection service returned `unauthorized`, so its context was
read through the GitHub connector instead. No credentials or host grant were
changed. Claude, Docker-runner capture, native cancellation/crash acceptance,
multi-agent overview, deletion UI and remote publication remain unfinished.
Old embedded node source must be updated before future turns use this capture;
this feature cannot recreate previously deleted temporary events.

## Graph-wide telemetry feasibility, 2026-10-15

The [assessment](design/graph-agent-observability.md) records a real three-turn
host App Server probe: two completed turns, one interrupted turn, native
messages and one command result, three usage updates and 14 OTLP batches.
One native tool item ID matched an OTLP call ID. No cost attribute was observed.
The ephemeral-thread history refusal is retained as a negative result, not hidden
or retried. Source and analyzer hashes pin the content-free implementation
observations; no raw private telemetry or message content is committed.

Docker was unavailable, and the host CLI version differs from the pinned runner.
Original-agent graph integration, parallel agents, subagents, Claude, reconnect
and the graph-wide UI remain unverified. An independent Claude review is required
before publication/merge; its findings and final revisions are recorded separately.
