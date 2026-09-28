# Claude Agent component

Status: proposed. This component runs Claude Code through the Claude Agent
SDK in the isolated runner. It shares Laomedo's agent contract with Codex but
keeps provider-specific session and skill behavior explicit. UI controls and
states require a view-owned Draw.io spec.

## Contract

Consume `AgentRunSpec` and emit `AgentRunResult` from
[shared contracts](contracts.md). Required inputs are the frozen task/input,
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
   [monitoring](../monitoring/run-traces.md). Store session ID as soon as it
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

The local proof of concept has no Claude adapter yet. A short SDK spike must
verify event coverage, model/effort validation, skill discovery, and session
storage before finalizing this adapter's estimate. See the official
[Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python),
[sessions](https://code.claude.com/docs/en/agent-sdk/sessions), and
[skills](https://code.claude.com/docs/en/agent-sdk/skills).
