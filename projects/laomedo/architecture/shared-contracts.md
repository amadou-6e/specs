---
title: Shared component contracts
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Shared component contracts

Status: proposed. These are runtime and data contracts, not a UI layout. All
IDs are opaque; exact serialization and schema versioning remain an
implementation decision.

The [local pilot adapter](../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
implements a narrower request/result and persisted run record. Real Langflow
output links answer, run, native thread, skill revision, and trace reference.
It does not yet implement every record or generalized definition-version and
invocation correlation described below.

## Core records

| Record | Required fields | Rule |
| --- | --- | --- |
| `SkillSnapshotRef` | `skill_id`, `revision_id`, `tree_hash`, selected file paths and hashes | Identifies exact bytes; never resolves through `latest` during execution |
| `EditPolicyRef` | `policy_id`, `revision_id`, `hash` | Independent from instructions used by a skill consumer |
| `InputSnapshotRef` | `snapshot_id`, `hash`, media type | Preserves one text/structured handoff payload; multiple user-added files require separate hash-checked file refs in IF-05 |
| `WorkspaceSnapshotRef` | `snapshot_id`, `hash`, source revision | Identifies source files before skill materialization |
| `EffectiveWorkspaceRef` | `snapshot_id`, `hash`, source workspace ref, materialized skill ref | Identifies the files actually offered at dispatch |
| `AgentRunSpec` | `provider`, model selection, effort selection, input, skill and workspace refs, permission grant, session mode, limits | Frozen before dispatch and attached to every resulting event |
| `AgentRunResult` | `run_id`, status, native session ID if issued, effective workspace ref, post-run workspace ref, output ref, trace ref, file-change ref | May be partial on failure; unknown fields are not fabricated |
| `SkillDraftResult` | `draft_id`, base and proposed skill refs, policy ref, patch ref, validation results, edit run ID | Cannot silently promote itself |

Before dispatch, the runner resolves IDs to complete hashed refs, materializes
the selected skill, and freezes an `EffectiveWorkspaceRef`. After the turn,
it captures a separate post-run workspace snapshot. A resumed session starts
from that last post-run state, not the original pre-run source snapshot. For
`resume`, the request's workspace ref must identify that expected last
post-run state and match the session registry before dispatch.

The `AgentRunSpec` supports `fresh` and `resume` session modes. `fork` is
allowed only if the adapter can state what was copied and what was not. A new
invocation with captured input is labeled `fresh`, even when it resembles an
earlier run. `permissions` identifies a recorded grant, not a free-form
instruction in a prompt. `limits` include a timeout and, where the provider
supports it, turn and spend limits. Requested and effective model and effort
are both recorded; an omitted setting is not inferred as an explicit choice.

## Component edge rules

- Skill Revision emits `SkillSnapshotRef` and optionally exact selected rule
  and example records. It never emits a mutable path as the only identifier.
- Codex Agent and Claude Agent consume the same `AgentRunSpec` shape and emit
  `AgentRunResult`. Provider-specific raw events remain available separately.
- Skill Draft consumes a base `SkillSnapshotRef`, an `EditPolicyRef`, an edit
  request, and a selected agent adapter. It emits a proposed revision, not a
  replacement for the base.
- A flow run links its Langflow invocation ID, Laomedo `run_id`, native session
  ID, definition revision, input and workspace snapshots, and trace ref.
- When a source does not provide a field, record `unknown` with provenance.
  Distinguish unknown, unsupported, omitted, and a measured value of zero.

## Example run request

```json
{
  "provider": "codex",
  "model": { "selection": "explicit", "id": "provider-model-id" },
  "effort": { "selection": "explicit", "level": "high" },
  "input_ref": { "snapshot_id": "input-id", "hash": "sha256:input-hash", "media_type": "application/json" },
  "skill_ref": { "skill_id": "skill-id", "revision_id": "revision-id", "tree_hash": "sha256:tree-hash", "file_hashes": { "SKILL.md": "sha256:file-hash" } },
  "workspace_ref": { "snapshot_id": "workspace-id", "hash": "sha256:workspace-hash", "source_revision": "source-revision-id" },
  "permission_grant_ref": "read-only-grant-id",
  "session": { "mode": "fresh", "resume_id": null },
  "limits": { "timeout_seconds": 600 }
}
```

The adapter validates supported model/effort combinations before starting.
The request is immutable after dispatch. A **user-requested new run** after a
failure gets a new `run_id` and links to the failed run so partial traces are
not overwritten. This is not automatic same-invocation crash recovery. The
older D17 three-attempt idea is a [deferred target](../decisions/0002-subsystem-handoffs.md):
first-slice mid-turn container crashes terminate with partial/unknown evidence.
Only a controlled real-agent session-restart experiment can justify a later
recovery identity and effect policy. The example's read-only grant is
illustrative; the first-slice agent checkout is writable, with separate
protection of runner, skill and unrelated host paths. Its Docker mechanism is
not proved by this record.

## Ownership

The runner owns agent-invocation execution and native session persistence.
Langflow owns live workflow sequencing and run state. Closing the Laomedo UI
does not stop a run while Langflow remains live; a Langflow restart or crash
ends that run, rather than transferring workflow recovery to the runner.
Persisted result/trace records are historical evidence, not a second live
workflow-state authority. The skill registry owns
immutable bundles and drafts. Monitoring owns event storage and projections.
Langflow components are adapters to these records and must not contain the
only copy of any run identity, skill revision, or trace. This does not imply
that Laomedo keeps a resumable copy of Langflow's live run state.

See [sandboxing](../subsystems/agent-execution/contract/isolation.md) and
[monitoring](../subsystems/run-traces/contract/README.md) for the shared execution boundaries.
