# Shared component contracts

Status: proposed. These are runtime and data contracts, not a UI layout. All
IDs are opaque; exact serialization and schema versioning remain an
implementation decision.

## Core records

| Record | Required fields | Rule |
| --- | --- | --- |
| `SkillSnapshotRef` | `skill_id`, `revision_id`, `tree_hash`, selected file paths and hashes | Identifies exact bytes; never resolves through `latest` during execution |
| `EditPolicyRef` | `policy_id`, `revision_id`, `hash` | Independent from instructions used by a skill consumer |
| `InputSnapshotRef` | `snapshot_id`, `hash`, media type | Preserves the effective handoff payload, including any structured fields |
| `WorkspaceSnapshotRef` | `snapshot_id`, `hash`, source revision | Identifies files visible before a run; a post-run snapshot is separate |
| `AgentRunSpec` | `provider`, model selection, effort selection, input, skill and workspace refs, permission grant, session mode, limits | Frozen before dispatch and attached to every resulting event |
| `AgentRunResult` | `run_id`, status, native session ID if issued, output ref, trace ref, file-change ref | May be partial on failure; unknown fields are not fabricated |
| `SkillDraftResult` | `draft_id`, base and proposed skill refs, policy ref, patch ref, validation results, edit run ID | Cannot silently promote itself |

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
  "input_ref": "input-snapshot-id",
  "skill_ref": "skill-id@revision-id",
  "workspace_ref": "workspace-snapshot-id",
  "permission_grant_ref": "read-only-grant-id",
  "session": { "mode": "fresh", "resume_id": null },
  "limits": { "timeout_seconds": 600, "max_turns": 20 }
}
```

The adapter validates supported model/effort combinations before starting.
The request is immutable after dispatch. A retry gets a new `run_id` and links
to the failed run so partial traces are not overwritten.

## Ownership

The runner owns execution and session persistence. The skill registry owns
immutable bundles and drafts. Monitoring owns event storage and projections.
Langflow components are adapters to these records and must not contain the
only copy of any run, skill revision, or trace.

See [sandboxing](../sandboxing/runner-isolation.md) and
[monitoring](../monitoring/run-traces.md) for the shared execution boundaries.
