---
title: Claude Agent component
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Claude Agent component

The [central D17 record](../../../decisions/0002-subsystem-handoffs.md)
defers automatic mid-turn container recovery until a controlled real-agent
session-restart experiment observes resumed, repeated and lost effects. A
stored Claude session ID or a clean resume does not prove crash-safe recovery.
The first slice ends a crashed invocation with partial/unknown evidence;
user-requested relaunch is a new linked run. The read-only acceptance case
below is a separate mode, not the writable PR-producing checkout chosen for
the first single-agent slice.

Status: proposed. This component runs Claude Code through the Claude Agent
SDK in the isolated runner. It shares Laomedo's agent contract with Codex but
keeps provider-specific session and skill behavior explicit. UI controls and
states require a view-owned Draw.io spec.

## Contract

Consume `AgentRunSpec` and emit `AgentRunResult` from
[shared contracts](../../../architecture/shared-contracts.md). Required inputs are the frozen task/input,
workspace, model and effort selection, permission grant, limits, session
mode, and optional pinned skill bundle. Output includes Laomedo run ID,
Claude session ID, status, response, trace ref, file diff/ref, and observed
usage when the SDK exposes it.

## Configuration and validation

Select a supported Claude model and effort level or explicitly use a
recorded default. Validate the combination for the installed SDK and target
model; unsupported levels fail before dispatch. Record effective values per
run or turn rather than rewriting prior history. Native tools and permission
mode must come from the recorded grant. Prompt instructions cannot override
the filesystem and network boundary.

Use a runner-specific `CLAUDE_CONFIG_DIR` and controlled working directory.
Do not load skills, memories, or settings from the user's personal Claude
profile. When native project skills are selected, materialize only the pinned
bundle into the isolated project skill path and enable the required project
setting source. Record the discovered skills if the SDK reports them. If
rules or examples are supplied directly as context, label that delivery mode
separately from native skill loading.

## Run lifecycle

1. Freeze refs and validate settings and permissions.
2. Allocate a run ID and isolated workspace. Materialize the selected skill
   and freeze an effective workspace hash. Start a fresh SDK query, or resume
   a stored Claude session only after restoring its last post-run workspace
   snapshot and verifying profile, skill revision, and permission grant.
3. Capture SDK messages and tool activity as raw events and normalize them in
   [monitoring](../../run-traces/contract/README.md). Store session ID as soon as it
   becomes available.
4. Freeze output, changed files, usage data if available, and terminal status.

Session persistence must remain enabled for resumable runs. A fork is only
advertised when the adapter can create a distinct session and state exactly
what history is copied. Forking a conversation does not fork side effects in
its workspace, so workspace isolation is required separately. Failure or
cancellation keeps partial events and does not relabel the run as completed.

## Acceptance

- A task runs with a supported model/effort pair and a private Claude session.
- A native selected skill is discoverable in the isolated project; unrelated
  user skills are not loaded.
- Resume uses the same isolated session and last post-run workspace state;
  a fresh run has a new session and Laomedo run ID.
- Tool calls, responses, errors, and partial output can be inspected after
  completion or failure.
- A read-only task cannot write to the source skill or workspace.

## Implementation note

The SDK remains the target transport above. The local single-user subscription
prototype in Laomedo PR #180 instead uses the official Claude Code CLI stream
protocol, pinned to 2.1.310, following the user's explicit subscription choice.
It must not claim SDK transport or production credential-broker acceptance.
See the official
[Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python),
[sessions](https://code.claude.com/docs/en/agent-sdk/sessions), and
[skills](https://code.claude.com/docs/en/agent-sdk/skills).

For this prototype, the executable and native sessions live in a dedicated
Docker image and profile volume. Personal sessions, settings and memories are
not imported. Only the current subscription access credential may be mirrored locally with
explicit opt-in authorization; refresh ownership stays on the host and the
rotating refresh credential is never copied; this does not establish a general production
authentication policy or permit copying a personal profile. Reject an access credential that cannot cover the execution deadline, and refuse
to overwrite a profile holding an independently established login.

Native controller file and shell tools are disabled. All draft file operations
and commands run in a separate credential-free, network-free worker; external effects require an
explicit host-mediated grant. Pinned native skills are full read-only bundles.
Controller-side skill preprocessing and permission/model/session overrides are
refused before dispatch. A prompt alone cannot establish these boundaries.

Resume across a compatible API restart verifies the account subject, native
session, image, profile, system configuration, grant and completed snapshot.
This is explicit completed-session continuation, not automatic crash replay;
D17 still applies. The independent supervisor must clean owned controllers and
workers even when the API disappears. Cancellation is confirmed only after
cleanup verification; uncertain remote effects stay unknown.
Controllers and workers also enforce their deadline inside the container. An
unverified container owner is never marked done: heartbeats stop so independent
lease-loss cleanup retains responsibility for that owner.

Model and effort choices come from native account discovery. Requested effort
and native-observed effort are separate; missing native evidence stays unknown.
Execution deadlines include correction turns. Normal runner startup must never
install experiment-wide model-turn ceilings or exhausted verification ledgers.

Real Fresh, native Skill invocation and completed-session Resume are recorded
locally during implementation. These do not by themselves establish cancellation,
handoff, join, error-UI or full target-contract acceptance. PR review must retain
those evidence boundaries until each required path is verified.
