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
and the [modal design at its historical revision](https://github.com/amadou-6e/specs/blob/70ca134/projects/laomedo/subsystems/run-traces/design/agent-activity.drawio).
The current [Agents tab target](design/agent-activity.drawio) supersedes that modal.

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
One native tool item ID matched an OTLP call ID. No cost attribute was observed
in log attributes; the probe did not search span attributes for monetary cost.
The ephemeral-thread history refusal is retained as a negative result, not hidden
or retried. Source and analyzer hashes pin the content-free implementation
observations; no raw private telemetry or message content is committed.

Docker was unavailable, and the host CLI version differs from the pinned runner.
Original-agent graph integration, parallel agents, subagents, Claude, reconnect
and the graph-wide UI remain unverified. An independent Claude review is required
before publication/merge; its findings and final revisions are recorded separately.

## Original Docker agents graph inspection, 2026-10-15

The [bounded contract slice](contract/interfaces.md#original-agent-graph-inspection-slice-2026-10-15)
now has real local graph evidence. It supersedes the Docker/concurrency/subagent
unverified statements above for this specific runtime and slice only.

[Content-free implementation evidence](https://github.com/amadou-6e/laomedo/blob/a9fb992/examples/agent-activity/evidence.json)
records graph execution `a7abc7a4-7698-43fa-afe2-9f4c6ceabfd5`: three original
Codex node invocations, four native turns including one explicitly linked child,
two concurrent runners, one shared native thread resumed in a later node, genuine
README shell reads and completed messages. The pinned CLI is 0.159.2 on the
reviewed rebuilt image, not a claim of historical image parity.

The final native usage totals are 111,870 input (85,248 cached) and 409 output
tokens across the three invocations, with child usage independently observed.
The Standard API-equivalent estimate is USD 0.00371918 using the dated catalog;
this is not a subscription charge. Local OTLP produced 3,280 retained records.
These are internal runtime observations, not 3,280 agent actions or extra charges.

An initial real verification found cross-invocation resume capture. The recovered
failure led to frozen dispatch cursors and durable source boundaries; those first
QA receipts are not acceptance. A separate regression removes phantom turns from
usage-only updates. Edge displayed the actual completed graph's shared timeline,
child turn, messages, command output and usage without JavaScript errors. Making
Prior Run visible preserves the saved resume edge when the graph opens.

Internal storage/API, runner and sandbox tests are separate evidence and use
fixtures only for negative/regression cases. Frontend builds pass; the broad
upstream TypeScript check has unrelated baseline errors and is not claimed clean.
Review and final-head checks remain required before merge. Raw task content,
native events, OTLP payloads and login material stay outside Git. The evidence
file was added at a9fb992 after its recorded runtime source commit 9f85367.

Open gates: Claude/other providers, OTLP metrics and flush completeness, crash
reconciliation, deletion UI, external collectors and the rest of the target's
filters, linked navigation and rich time-series controls. This validation does
not promote draft lifecycle maturity or claim those interactions are delivered.

### Competing-resume negative check

The independent review found that cursor-only boundaries could associate one
accepted resume with another node that was refused. This was repaired with unique
runner-accepted attempt IDs, authoritative acceptance-time baselines and per-attempt
stream bounds. Inspection never adopts a neighbouring attempt merely because its
source cursor matches. A repeated reference to a captured attempt is not new usage.

The [real contention evidence](https://github.com/amadou-6e/laomedo/blob/8811091/examples/agent-activity/resume-contention-evidence.json)
records execution `98e65dae-11b8-4c99-a915-f779fad659c9`: one fresh original
Docker turn followed by two competing resume nodes. One resume completed, the
other was refused with zero retained receipts and turns. Usage and monetary cost
are unassigned for the refusal, not measured zero. The accepted invocation's
messages, usage and terminal evidence remained separate. Normalized source hashes
pin the tested mechanism. This is real provider evidence, separate from the HTTP,
projection, schema concurrency, truncation and live-polling regression tests.
