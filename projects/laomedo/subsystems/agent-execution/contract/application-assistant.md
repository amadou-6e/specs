---
title: Persistent application assistant and Laomedo MCP
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-16
applies_to: [laomedo]
supersedes: null
related: []
---

# Persistent application assistant and Laomedo MCP

Proposal for [specs #423](https://github.com/amadou-6e/specs/issues/423) and
[Laomedo #282](https://github.com/amadou-6e/laomedo/issues/282). The owner selected
a long-lived normal chat backed directly by an existing provider, with Laomedo
MCP tools. The assistant itself has no Langflow workflow. This is an explicit
exception to the earlier all-agent-interactions-through-Langflow direction.
Langflow still owns workflows that the assistant creates. Implementation starts
only after the owner's final approval of this proposal; review is not that approval.

The [editable assistant design](../design/application-assistant.drawio) owns
proposed geometry, visible controls, states and transitions. The
[realization plan](../design/application-assistant.md) explains mechanisms and
remaining engineering checks, without claiming implementation or runtime acceptance.

## Scope and proposed initial defaults

Windows, trusted single-user local deployment, Codex first. Use the existing
provider runner, subscription login, model discovery, Activity and cancellation;
do not create a new inference backend or provider-specific chat methods. Other
providers remain available execution integrations, not assumed chat-accepted.

The initial assistant can inspect the current owner's saved workflows and public/
local Skill metadata and create or revise its own workflow drafts. It cannot run,
publish or delete workflows, modify source workflows or assignments, authorize
GitHub writes, generate custom component code or manipulate account connections.
Private Skill access remains subject to its separately accepted authorization;
this feature never bypasses it or claims unfinished private-source support.

Proposed defaults for final approval: one provider/model/effort binding per
conversation; other choices create a new conversation. Conversations and draft
receipts persist across app restarts. History is retained locally; no automatic
expiry or external transcript publication. Reinstall/migration and a deletion
UI are outside the initial slice; they must not be claimed. New conversation
does not erase previous history. Opening a draft uses a new application tab to
preserve the current editor and its unsaved work, only after the user's action.

## Conversation and message identity

The application owns a durable `conversation_id` and authenticated owner binding.
It records provider/model/effort, runner binding, native thread identity when
observed, workspace checkpoint, messages, attempts and authoritative draft receipts.
Provider credentials and MCP bearer values never belong to this record.

Each user message has a stable `client_message_id` and distinct `attempt_id`.
The first starts an existing provider run; later messages resume its native
session through the existing interface where admitted. A conversation is not a
running container. Idle chat needs no live container or renewable tool grant.
The implementation may retain the native MCP client while idle, but must not
leave usable provider access after a turn ends.

At most one turn is active per conversation. Persist message identity and its
dispatch reservation before submitting native work. Duplicate submission of the
same message/content returns its existing attempt; reuse with different content
is refused. Another message while active is refused without dispatch. Conversation
creation and model selection do not call a model.

Resume does not get a fresh semantic identity merely because an HTTP response was
lost. Resolve submitted attempts through retained request/attempt records before
retrying. An unresolved dispatch is visible as unknown; never blindly re-prompt.

The runner must durably admit follow-up messages idempotently by
`(run_id, activity_attempt_id)` and a canonical digest of task and semantic
resume bindings, with an attempt lookup operation. The existing synchronous
resume endpoint does not yet supply this guarantee. Reserve before dispatch;
duplicates return the existing pending/terminal attempt and changed content under
the same key refuses. Check this before claiming/replacing a new MCP registration;
duplicate requests must not revoke or replace an active attempt's tool access.
The app's own message reservation alone cannot close a lost-resume-response gap.

## Normal chat, Activity and Stop

Show messages, ongoing assistant content, tool progress, final result and the
selected model. Consume the existing attempt-scoped Activity interface while
work happens, rather than waiting for a terminal answer or parsing process logs.
Retained history distinguishes user/assistant/tool observations, partial output,
errors and cancelled attempts. Do not render a final answer twice when both
Activity and a terminal runner record describe it.

Stop targets only this conversation's active attempt and requests cancellation
through the existing provider interface. Show stopping until native status and
owned-resource observations settle; request acceptance is not confirmed teardown.
Closing or switching the chat does not itself cancel a turn. Reopening reconnects
to the same recorded attempt and history, not a new model request.

A normal chat must permit a new message after a stopped or failed turn when
safe native continuation is established. Do not implement this by merely changing
the providers' accepted status strings. Before further dispatch, establish:

- the earlier attempt cannot still execute native work;
- its owned command work and cleanup are settled, or continuation is refused;
- a native session exists and belongs to the same provider/account binding;
- the retained workspace and its recorded checkpoint are consistent;
- outstanding tool effects, especially draft saves, have been reconciled;
- the new attempt gets fresh MCP access and a distinct message/attempt identity.

The new message is not an automatic retry of the interrupted message. Failure
before session creation may require a new native session; do not pretend one
was resumed. Session loss, incompatible upgrades or unsafe recovery preserve
history and show a stable explanation, with an explicit Start linked conversation
action. No silent session substitution or old-message replay is permitted.

On app restart, revoke old MCP grants, reload persisted conversation state and
reconcile active attempts with the runner before enabling Send. App restart is
not necessarily runner restart. Runner restart and provider authentication changes
retain existing fail-closed rules unless separately verified continuation permits
them. Transparent mid-turn recovery is not a promise of this feature. Idle
reopening must preserve history even if the native binding is no longer resumable.

## Laomedo MCP boundary

Provide an actual MCP server with a narrow workflow-authoring toolset. The app
owns the native MCP client/session and admits its selected tools through the
existing manifest/forwarding path, without a graph. Controllers receive only
the per-attempt scoped forwarding connection, not application credentials or
arbitrary upstream configuration. This extends the graph-connected
[MCP contract](mcp-tools.md) to app-owned native sessions; its custody, size limits,
app-loop ownership, expiry, revocation and no-uncertain-replay rules still apply.

Bind the authenticated owner and conversation on the host. The model cannot
choose a user, conversation, server URL, credential source or arbitrary filesystem
path in tool arguments. No tool exposes login, execution, publish, delete or
unrestricted component/code editing. Source workflow names, prompts, descriptions
and Skill content are untrusted data, never authorization.

The host native-client credential binds owner/conversation and is distinct from
the provider's per-attempt forwarding capability. Keep the former only in private
host client configuration and invalidate it on profile lock/sign-out; revoke the
latter for affected attempts and fence dispatch/late response release separately.

Proposed wire signatures, with bounded typed arguments/results:

| MCP tool | Arguments | Result / invariant |
| --- | --- | --- |
| `list_workflows` | `query?`, `cursor?` | Bounded owner-visible workflow summaries and next cursor; no secrets/code |
| `get_workflow` | `workflow_id` | Revision/digest plus projected nodes, ports, non-secret fields and edges; no other owner's data |
| `search_components` | `query`, `cursor?` | Bounded installed-component identities and descriptions |
| `describe_component` | `component_type` | Canonical input/output names/types and writable static field schemas, not arbitrary executable source |
| `list_skills` | `query?`, `cursor?` | Authorized supported Skill identities, exact revisions and descriptions; no implicit private access |
| `save_draft` | `draft_key`, `name`, `spec`, `sources[]`, `draft_id?`, `expected_revision?` | Atomic persisted draft, revision and authoritative receipt, or stable refusal |

`spec` is a typed declarative graph: nodes identify an installed component type,
local node key and allowed field values; edges identify exact source/output and
target/input names. `sources` binds any copied workflow to its exact observed
revision. Model-generated Python, inline executable templates and secret fields
are rejected. Canonical executable templates are supplied by the trusted installed
catalog, not copied back from model output. Structured fields are permitted only
where the approved static schema defines them; no string-coercion workaround.

Copy source settings only through host-owned explicit projections. Do not leak
secret fields through prompts, errors, summaries, tool results or receipts, and
do not duplicate upstream domain credentials into drafts. Unavailable dynamic
fields are reported as unsupported/unresolved; never run component update hooks
to make the draft appear complete.

## Draft persistence, validation and receipts

Validate identities, allowed fields, required values and compatible ports against
installed metadata without evaluating component code, constructing executable
graphs, resolving network inputs or invoking provider discovery. Refuse unavailable
catalog metadata rather than treating missing validation as success. Structural
validity is not proof of executable success. A requested intentionally incomplete
draft may be saved only with explicit incomplete diagnostics, never labelled valid.

Persist the complete draft and its receipt atomically through the workflow owner.
New draft creation must not expose partially assembled graphs. Assistant updating
requires an atomic expected-revision comparison and is limited to this conversation's
own drafts. If the editor or any other writer changed the row since that revision,
refuse the assistant edit. A read-compare-PATCH race or process-local lock alone
is insufficient. Use the flow owner's transactional locking; this does not add
expected-revision parameters to the editor's existing PATCH contract. Source
workflows remain unchanged.

`draft_key` is unique within the conversation. Repeating the same key and same
canonical operation returns the original receipt; a different operation with
that key fails. A new edit uses a new key. Saving never executes or publishes.
Cancelled or timed-out save outcomes are reconciled from the durable receipt
before another save is proposed. Do not depend on replaying the upstream call.

The application obtains draft links from successful persisted tool receipts,
not model prose. Each receipt names conversation/message/attempt, operation key,
draft identity/revision and save outcome. A committed save remains visible even
if the model turn subsequently fails. Invalid/stale saves produce no success
card. A prior saved draft is not silently represented as the result of a failed edit.

## Access, workspace and operational scope

App routes use the current authenticated local profile/owner, not a caller-supplied
owner string. Recheck access at response release and before dispatch. Profile
lock/sign-out invalidates chat access and tool authority; prevent cross-profile
late responses and further dispatch, while preserving private retained evidence.
Do not import credentials from an unrelated interactive assistant session.

Use a dedicated app-owned assistant source workspace and runner configuration,
with no user repository or unrelated host mounts and no GitHub/publication authority.
Native command/file tools remain governed by existing provider isolation; the MCP
allowlist alone does not prevent those tools from running inside the workspace.
The existing isolation guarantees must be verified for this composition. Do not
claim prompt injection harmless merely because the application tools are narrow.

Application and tool tokens remain private host configuration. Metadata/results
are bounded and projected; retained native history can still contain model-visible
content and remains local private evidence. No new general approval authority,
multi-user service, automatic infrastructure retry or numeric model-turn budget
is introduced. Any live acceptance harness has its own explicit scope.

## Acceptance gates

1. A real initial-provider chat creates a draft using actual components/Skills,
   streams Activity and opens the persisted draft only after the user's action.
2. Follow-up edits keep conversation/native identity where supported; source flows,
   tags, assignments and active workflow runs are unchanged. Save runs no graph.
3. Stop then another message works after verified settlement. Failure before/after
   session creation, cleanup uncertainty and restart are separately exercised.
4. Duplicate/lost responses dispatch once; concurrent messages, stale edits and
   conflicting save keys refuse without overwrite or duplicate drafts.
5. Committed-before-cancel saves reconcile to exact receipts; invalid/unknown outcomes
   never create fabricated saved-draft cards or automatic uncertain-call replay.
6. Reopen/restart preserves history and reconciles active attempts; unsafe native
   continuation is explicit and never silently becomes a fresh session.
7. Owner/profile isolation, lock/sign-out fences, private tokens, source-workspace
   isolation and bounded result projections pass concern-owned checks and real
   initial-provider acceptance where needed. No broad private-source claim.
8. Independently review code/spec fit and actual rendered UI at exact revisions;
   fixtures do not replace real agent/MCP/editor acceptance. Proposal review and
   Draw.io inspection alone establish neither implementation nor execution readiness.
