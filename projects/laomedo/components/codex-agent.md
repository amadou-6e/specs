# Codex Agent component

Status: proposed. This component runs Codex as a flow step through the
isolated runner. It is distinct from using Codex to design the flow. A
view-owned Draw.io spec must define its controls and states before UI work.

## Contract

Consume `AgentRunSpec` and emit `AgentRunResult` as defined in
[shared contracts](contracts.md). The spec contains a frozen input snapshot,
workspace snapshot, optional `SkillSnapshotRef`, model and effort selection,
permission grant, session mode, and limits. Output contains Laomedo run ID,
native Codex thread ID, status, final response or structured output, trace
ref, post-run file diff/ref, and observed usage when available.

## Configuration and validation

The user may select a supported model and reasoning effort or explicitly use
the runner's recorded defaults. Resolve defaults at dispatch and store both
requested and effective values. Reject unsupported model/effort combinations
before starting; do not silently downgrade effort. A changed model on resume
must be recorded as a new turn setting, not rewritten into earlier turns.

The first release supports read-only runs and a separate draft-skill edit mode.
Its available tools, filesystem access, network access, approval behavior,
timeout, and workspace are determined by a recorded permission grant and
[runner isolation](../sandboxing/runner-isolation.md), not by prompt text.
No profile or credential from the user's normal Codex installation is used.
The selected credential mode and broker reference follow
[runner authentication](../sandboxing/runner-authentication.md); no raw token
belongs in `AgentRunSpec` or its trace.

## Run lifecycle

1. Resolve and validate all refs, capability settings, and permission grant.
2. Allocate a Laomedo run ID and private profile. Materialize the pinned
   skill, then capture an effective workspace hash that includes every file
   offered to Codex. Preserve the source workspace hash separately.
3. For `fresh`, start a new Codex thread. For `resume`, look up the native
   thread ID from a prior run and verify provider, profile, last post-run
   workspace snapshot, and permission compatibility before continuing.
4. Stream native thread/turn/item events to
   [monitoring](../monitoring/run-traces.md) as they arrive. Preserve provider
   payloads and normalize a second view for cross-provider inspection.
5. Freeze final output, file diff, actual settings, and terminal status.

An interrupted run may have a native thread ID and partial output. Store both.
Retrying a failed step creates a new Laomedo run ID; resume is a distinct
operation with explicit linkage. A copied prompt is not an exact thread fork.
If the Codex API cannot provide a requested fork, report unsupported and offer
a fresh invocation with captured input.

## Skill delivery

Materialize the pinned bundle under the isolated workspace's Codex skill
discovery path when compatible. Record the materialized path and file hashes
in `EffectiveWorkspaceRef`; do not claim that the pre-run workspace hash
describes the added files. The runner must verify Codex's skill search paths
for its installed version, including project, profile, and home directories,
and exclude personal skills before claiming isolation. `CODEX_HOME` alone
must not be assumed to suppress every other discovery path.
If a selected rule/example is injected as text instead, report that delivery
mode and do not claim native skill execution. An offered skill is not proof
that Codex read it; use observed file or skill events where available.

## Acceptance

- A read-only task runs with a selected model and effort and records the
  requested and effective values and native thread ID.
- Two runs do not add sessions to the user's personal Codex profile.
- Only the pinned skill is discoverable; no skills from the user's personal
  Codex profile or home directory are loaded.
- A resume continues only the matching isolated thread and retains prior
  events; a fresh retry has a separate run ID.
- Inspectors can open tool calls, results, errors, output, and partial events
  without relying on a final-response-only bridge.
- A read-only run cannot change its source workspace or skill revision.

## Implementation note

The current local bridge proves a final-response call through the Codex Python
SDK. It uses the user's default profile and only hashes `SKILL.md`, so it is
not an acceptable implementation of this contract. The SDK's streamed turn
events are a starting point; Codex App Server may better support a richer
trace client. See [Codex SDK](https://developers.openai.com/codex/sdk/) and
[App Server](https://developers.openai.com/codex/app-server/).
