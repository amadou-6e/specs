---
title: Claude Agent component
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-19
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

## Local proposal node (2026-10-19)

The first implemented node is a deliberately narrower **proposal mode**, using
Claude Code CLI 2.1.301 and the operator's existing Claude subscription. It does
not claim the isolated writable SDK target described below. Native shell/file
tools, MCP, personal customization sources, hooks, skills and auto memory are
disabled. The official CLI uses its normal login in place; Laomedo never reads,
copies or exports its credential files. Host execution is not a Docker sandbox.
The later isolated writable execution mode remains unimplemented.

The node reuses Task, Operation (fresh/start/resume/status/cancel), Model, Effort,
Skill References, Output Requirements, Output Requirements JSON, Output
Continuation Retries and Prior Run. Answer, Run Reference and Submission share
one dispatch per node build. Use the existing view layout with a Claude title;
[Claude node view](../design/claude-node.drawio) owns the controls and feedback
layout. The whole custom component category must be installed together.

Skills are immutable UTF-8 snapshots included in the prompt, explicitly recorded
as `prompt_snapshot` / `included_in_prompt`, never native discovery or proof of
instruction compliance. No native shell, file writes or direct GitHub operations
are available. Skill -> Claude -> the same Skill Operation and PR -> Claude ->
the same PR Operation carry proposals; only the authorized host operation service
can apply them. Its strict validation, selection, policy and revision history
remain authoritative. Multi-file edits remain a single atomic Skill operation.

Each run has provider `claude`, a fresh UUID session, a host run/attempt identity,
pinned runtime/model/effort and source/workspace hashes. Native JSON terminal
receipts and answers are retained privately. Adapter-normalized activity records
are labelled with provider and normalization version; host attempt IDs must not
be described as native Claude turn IDs. Unknown model resolution, token metrics
and API-equivalent costs remain unknown. A terminal CLI receipt establishes this
proposal invocation's completion, not general SDK/tool-trace parity.

Pinned output requirements use the existing host evaluator. A rejected JSON form
can receive at most the configured correction count, on the same Claude session,
with each dispatch booked before launch in the durable total-turn ledger. No
parser repair, blind transport retry or replay of host writes is allowed. A
native precheck tool is not installed in this mode; post-turn validation is
recorded separately. The default turn budget is zero until host configuration
explicitly enables it.

Resume requires the same provider/runtime, runner instance, subscription subject
hash, model/effort, native session and unchanged post-run snapshot/pinned skills.
Restarted/interrupted/failed runs do not auto-resume. Cancel stops the owned CLI
process tree; a request acknowledgement is separate from observed process exit.
A prepared cancellation must prevent later dispatch. Reads/status do not book a
model turn. Credentials and raw CLI transcripts must stay out of exported graphs.

Live acceptance must demonstrate a real selected Skill -> Claude -> Skill edit,
host-created parent/diff/provenance and independent readback. A successful initial
answer does not demonstrate a correction being exercised. Internal controls do
not substitute for live acceptance. A separate PR operation uses its existing
repository authorization; the Skill demonstration alone does not prove live PR
operation acceptance.

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

The local proof of concept has no Claude adapter yet. A short SDK spike must
verify event coverage, model/effort validation, skill discovery, and session
storage before finalizing this adapter's estimate. See the official
[Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python),
[sessions](https://code.claude.com/docs/en/agent-sdk/sessions), and
[skills](https://code.claude.com/docs/en/agent-sdk/skills).
