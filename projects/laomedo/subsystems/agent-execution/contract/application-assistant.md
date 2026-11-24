---
title: Persistent application assistant and Laomedo MCP
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-19
applies_to: [laomedo]
supersedes: null
related: []
---

# Persistent application assistant and Laomedo MCP

## AS-311 — Complete supported flow configuration and observation

Owner-selected implementation: Laomedo #311; specification #443. This extends
the delivered draft/edit/run tools, rather than introducing another execution
engine. Subscription quota work is outside this feature.

The assistant must discover, configure, validate, save, request execution,
observe and repair a supported flow without a human completing its configuration
in the editor. A static demonstration alone does not establish this capability.
The editable A4 workshop's AC311 states own the interaction outcomes below.

### Supported configuration inventory

Discovery identifies the exact component/schema revision and each field's kind,
dependencies, configurability, safe default provenance and blocked reason.
Existing visible primitive static fields remain supported. The initial audited
dynamic families are Laomedo Codex/Claude/OpenCode Agent account/model/effort,
local imported Skill identity/revision, and registered MCP selections where the
registration owner provides authorized metadata. Schema-declared structured
values require explicit field-specific support. Unknown hooks, custom code,
unmediated endpoints/host paths and secret values remain unavailable, visibly
reported during discovery. They must not be silently cleared and called ready.
Private GitHub node configuration retains its separate PR287 dependency.

`resolve_node_configuration` accepts an installed component and candidate values,
plus the expected schema revision when continuing a candidate. It returns safe
normalized values, dependent choices, remaining requirements and an expiring
resolution identity. Resolution is bound to the authenticated owner/conversation,
browser authority, component/schema, values and resource generations; the identity
does not grant permission. Revalidate on save, apply and dispatch. No account
fallback or model-supplied credentials. Audited resolvers call existing resource
owners; they never invoke arbitrary component update/build hooks. Zero-turn model
catalogue discovery may start its normal bounded native discovery, but submits no
model task and never changes the selected connection. Report that operation's
availability honestly; validation itself performs no native discovery.

For existing nodes, incremental edits retain unmentioned values and trusted code
exactly. For new nodes, retain only explicitly supported, schema-valid nonsecret
defaults. Cached connection selections, private references, executable values and
host configuration are not defaults to copy. Missing required bindings remain
not ready. Ordinary authorized read grants cover resource discovery; missing
authority is an explicit refusal, not a new automatic grant.

### Readiness, saving and execution

`validate_workflow` supports a declarative candidate or an exact owned saved
revision and returns structured node/field/edge diagnostics, unresolved resources
and readiness. Structural and configuration checks never build or execute graph
nodes or call their refresh hooks. Resource bindings are checked through their
owners without credential release. Saving an incomplete draft still requires
explicit `allow_incomplete`; it does not constitute runnable readiness.

Extend existing draft/edit requests with resolution references and existing run
proposals with typed runtime node inputs and output selection where the pinned
execution API supports them. All semantics participate in existing action digest,
revision and human consent checks. Never expose a generic tweaks/HTTP/code tool.
Late schema, resource generation or graph changes refuse rather than overwrite.
The exact approved graph revision is the executed snapshot.

### Run evidence and cancellation

`get_workflow_run` selects this conversation's approved action, with optional
node/result pagination. Return authoritative lifecycle, output availability,
bounded typed outputs, partial results and safe structured diagnostics. A
completed job without retained output is not a fabricated answer. Reuse existing
Langflow execution records; retain any missing bridge result under the same owned
database lifecycle, with bounded release and restart reconciliation. Do not
expose raw errors, settings, templates, credentials or arbitrary nested runtime
objects. Recheck current session/owner/resource authority at release.

`cancel_workflow_run` affects only an exact owned previously approved run through
the existing execution owner. It is idempotent and submits no new graph work.
Distinguish requested cancellation, observed settlement and uncertain outcomes;
cancelled is separate from failed. Chat Stop retains its existing scope. Never
automatically replay a run or infer success from assistant prose.

### Acceptance and evidence

Maintain a supported capability inventory mapped to applicable checks. Real
internal-agent MCP acceptance must create a new target graph, resolve dependent
settings, save/reload, validate and run with an independently checked result;
also edit an existing flow and diagnose/repair a controlled failure. Cover a
pinned Skill/registered MCP path and an independently worded holdout. Source
graphs may exist for edit/combine tests; no prebuilt target may masquerade as
agent authoring. Verify no human editor save between agent save and execution.

Concern-owned tests cover stale schema/options, foreign/revoked resources,
conflicts, lost acknowledgements, duplicate operations, result release bounds,
cancellation and restart. Negative cases assert no unauthorized dispatch or
release; they do not require a run. Fixtures cannot establish real provider
acceptance. Record exact revisions, approved live submission budget/accounting,
tool receipts, saved/run identities, independent output oracle and actual editor
render. Production must not depend on experiment drivers. Independent code,
specification and actual UI review remain required before merge. No acceptance
or safety certification is claimed by this draft.

## Native agents and slash commands â€” selected work, Laomedo #293

AS-293 is an incomplete implementation target tracked by specs #435. The owner
selected provider-native agents and slash commands, with built-ins only. This is
not a request to expose Laomedo runner start/resume/cancel controls. Personal CLI
profiles, repository-defined commands, custom agent files and plugins are outside
this selection. Native permission modes remain separately owned by Laomedo #288.

The assistant must discover actual native capabilities through Laomedo MCP and
propose exact invocations for human approval. Merely offering a human-only slash
menu does not complete this requirement. Discovery grants no invocation authority.
Catalog descriptions and argument hints are untrusted display data. Missing,
unsupported, invalid and explicitly empty observations must not be conflated.
Optional discovery failures must not break normal chat or graph-agent execution.

Command catalogs belong to the same owner, conversation, native session and
isolated workspace in which execution occurs. ACP command updates replace the
complete list, including an empty list. Clearing per-turn Activity buffers must
not discard session command metadata. Bounded detached observations have a stable
metadata revision; the revision is not an authorization token.

Invocations must bind the exact command or agent identity, arguments, catalog
revision, owner, conversation and originating human app session. The model cannot
approve its own proposal. Existing graph permissions do not authorize native
commands. No command may bypass account-management restrictions or alter native
permission modes through this interface. Unknown or UI-only commands must not be
silently interpreted as ordinary prompts or reported as successfully executed.

Execution must not re-enter an active native prompt. An admitted operation must
retain an unambiguous dispatch identity, recheck authority and native availability,
and settle the thread/workspace checkpoint before further chat uses that session.
Commands that return a native control result without a model turn must not invent
turn IDs, model usage, native completion events or assistant response text.
A compact operation completing without an agent message shows only its outcome
state. Other model-generating commands keep
the existing native terminal-evidence requirements. Uncertain outcomes are retained
without automatic replay; cancellation, revocation and restart must not duplicate
effects. Results remain visible and copyable in the conversation.

The first selected slice composes Codex only. Its pinned ACP interface advertises
slash commands but has no configured built-in-agent enumeration. Spawned-child
events are not a selectable agent catalog. The owner then selected the additional
Claude/OpenCode slice defined below; native agent invocation remains excluded.
`list_native_agents()` reports unsupported with that explanation, not an empty
list implying no native agents exist.

The concrete MCP surface is `list_native_commands()`, `list_native_agents()`,
`propose_native_command(command, arguments, catalog_revision, operation_key)`
and `get_native_action(action_id)`. All calls are host-bound to the current
conversation. The model supplies no owner, runner address, workspace or native
thread ID. Command discovery requires a native session to have advertised its
catalog; opening a conversation alone does not create a native session or model
turn. Observed descriptions are not execution policy.

The initial execution policy admits `/status`, `/mcp`, `/skills`, `/review` and
`/compact` only when actually advertised. Only `/review` accepts arguments: one
line of at most 4000 characters without control or line-separator characters.
The other admitted commands accept no arguments. Execution rechecks the catalog
observed in the resumed native session itself; an absent catalog or changed
revision refuses the command before dispatch.
Codex `/logout`, Claude `/login` and `/logout`, and OpenCode `/connect` open the existing Settings → Providers screen without disconnecting an account. Codex and Claude `/rename` open the existing Laomedo conversation title form, with Save/Enter to apply and Escape to cancel. These are explicitly labelled app actions, not native command execution; they do not invoke a model or native command.
`/goal` and `/plan` remain deferred by owner decision: `/goal` changes autonomous continuation; `/plan` changes native configuration
that is not retained by the existing per-turn runtime. Branch/commit review
commands require a selected repository and are unavailable in scratch chat. Deferred plan/goal and repository-review commands remain disabled, never silently mapped to another operation. Unknown commands and
custom skills are unavailable in this built-ins-only slice. Review and compact
can consume model quota. Arguments must be shown exactly before approval.

Each proposal renders a compact native command card in its originating response:
`Run /review with arguments "inspect error handling"`, followed by Approve and
Reject. There is no native-command Always grant in this slice. Decisions are
human-only app routes bound to the exact action digest. Approval during an active
chat turn is refused without consuming the proposal; the user can approve after
that turn settles. Approval atomically reserves a command message or produces an
explicit non-replayable uncertain outcome. The command result appears as the
response to that command message; it does not automatically start another model
turn. Approved graph actions and their existing consent remain unchanged.

The approval interaction design and final implementation require independent
review and real provider verification before this slice is accepted.

## Graph editor sidebar â€” selected owner feedback, Laomedo #296

AS-296: The header Assistant link opens full-window `/assistant` in the current
tab, on both the workflow list and graph pages, using the router and its existing
unsaved-editor navigation guard. Navigating away during a graph build stops it
through the existing guard. The rail toggle keeps the graph running. An Assistant icon in the graph left rail toggles
a right-hand chat column using the same conversations and APIs as `/assistant`, including
existing approvals, tools, copy, export and deletion. It creates no workflow or
second inference integration. Opening, closing, resizing and selecting a saved
conversation never submit a prompt. The editor and unsaved canvas remain mounted when toggling the sidebar. The rail
control leaves the selected left section unchanged, including the Agents view.

The divider supports pointer dragging, Arrow Left/Right in 24px steps, Home for
minimum and End for maximum, with an accessible name, orientation and current
value. Drag resizing uses the same arrow strip as click collapse, with no second
rail or column. A drag must not collapse the panel on release. Initial width is 480px, minimum 280px and maximum 720px, clamped to the
available editor. Narrow windows use an overlay with the same visible collapse strip.
Resizing the window reclamps width. Focus returns to the opener on close.

The sidebar uses one top header row: conversation title (including rename),
History, existing export/delete actions and the full-window link. There is no
extra Assistant title row or header close icon. The outer 8px edge strip collapses
the entire assistant panel without discarding its mounted draft. It stays available
in chat, history and locked states. The header History icon opens/closes the
conversation list; choosing a conversation restores the chat view. Expanded history
keeps History and full-window actions reachable. Full-window chat retains its
existing history geometry and controls.
Conversation metadata replaces the provider text labels with monochrome SVG
provider marks alongside the date/state. Faint rules separate the vertically
stacked conversation rows, rather than adding dividers inside their metadata. Do not
add a new icon column before the conversation title; retain accessible provider names.
Earlier conversations load automatically when scrolling near the end, with a
loading indicator and no separate pagination action. Active rows show a spinner;
background work shows a throbber instead of the static switching-conversations tip.
The sidebar initially hides its conversation list to prioritize chat. Expanding
history shows the same owner-scoped conversations as full-window chat. Selection
does not alter the graph URL. Closing retains the mounted chat's draft and active
response; reopening restores them. Navigating away may unmount the sidebar, while
accepted work continues in the existing service. A full-window icon uses router navigation in the current tab to open the
selected saved conversation. The sidebar full-window icon leaves the editor;
unsent sidebar text is discarded and the existing guard applies, including
stopping an active build. Unsent text otherwise remains local to its originating
surface; no cross-tab draft synchronization is promised. Profile changes clear
private rendered state and selection as in full-window chat.

The appended AS-296 page in the editable assistant diagram defines its geometry.
Acceptance requires actual shared conversation history, close/reopen draft
retention, keyboard and pointer resize, preserved canvas and existing approval
behavior in a real application preview. Fixture tests alone are insufficient.

Proposal for [specs #423](https://github.com/amadou-6e/specs/issues/423) and
[Laomedo #282](https://github.com/amadou-6e/laomedo/issues/282). The owner selected
a long-lived normal chat backed directly by an existing provider, with Laomedo
MCP tools. The assistant itself has no Langflow workflow. This is an explicit
exception to the earlier all-agent-interactions-through-Langflow direction.
Langflow still owns workflows that the assistant creates. The owner subsequently
authorized implementation and requested the final UI changes
recorded below. This amendment aligns the specification with those decisions;
independent review does not substitute for owner approval.

The [editable assistant design](../design/application-assistant.drawio) owns
geometry, visible controls, states and transitions. The
[realization plan](../design/application-assistant.md) explains mechanisms and
engineering boundaries. The validation record separates observed implementation
checks from target guarantees and remaining limits.

The selected [approval-gated graph extension](assistant-graph-actions.md) adds
human-approved edits and runs when implemented and accepted. Its explicit
approval boundary supersedes the initial read/draft-only restriction only for
those actions. Publication and native permissions remain excluded.

## Scope and selected initial behavior

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

The provider binding remains fixed for a conversation; another provider requires
a separate conversation. Model and reasoning effort are selected for each turn
from discovered supported options, without replacing the native thread/run. The
composer visibly reuses a supported current/recent pair or the first supported
pair for a new chat; this is a UI selection, not a claim about provider defaults.
Selection and conversation creation never submit inference. Conversations and draft
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
same message/content/configuration returns its existing attempt; reuse with
different content or configuration
is refused. Another message while active is refused without dispatch. Conversation
creation and model selection do not call a model. Each admitted message records
its immutable model/effort selection. Omitting both uses the conversation
defaults; supplying only one refuses. Explicit selection forms part of the
canonical retry digest; retry must preserve its original identity and selection.
Codex resume accepts supported model/effort changes without requiring model
equality, while preserving native thread, account, workspace and safety checks.

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

## Owner-selected chat controls and send feedback

The editable design owns the detailed layout and transitions. The title header
shows the conversation name without repeated provider/model metadata. Double-click
or keyboard title activation opens a wide inline rename field; Enter or Save
commits, Escape or Cancel leaves the title unchanged. Rename does not dispatch
inference. User and assistant bodies use the same 14 px text size.

History is collapsible, with New conversation at its bottom. New chat shows a
workflow illustration and the supported Codex provider card. The compact composer
model menu uses the discovered model list and an annotated effort slider; there
is no Refresh models action or model-card grid.
OpenCode Go model labels omit the `opencode-go/` prefix; exact IDs remain unchanged
in the provider contract and model selection. Changing a selection during an
idle conversation applies to its next turn. Selection is locked during dispatch
and an active turn. Native permission modes are deferred to Laomedo #288.

When the command/skill picker is open, Enter selects its first executable match
without dispatching; after selection, Enter sends the prepared message.
Otherwise Enter sends, Shift+Enter inserts a newline, and Enter during IME composition does
not send. The message box retains focus after Enter and remains editable during
dispatch/response while Send stays fenced. Keyboard and button use the same admission rule: no dispatch
while active, pending, busy, needing attention, or unable to observe current state.
A displayed error from a definite rejected request must not permanently disable
Send after the conversation is observed idle. Unknown dispatch retains its exact-key
pending fence and explicit recovery rather than permitting a duplicate request.
Stop remains available while the active turn can be cancelled.
The composer remains editable during startup, dispatch and active responses so
the user can draft the next message; typing never queues or submits another turn.
Late acknowledgements preserve newer text. If a definite refusal restores the
submitted text, retain any newer draft too. Locked/attention states retain their
existing restrictions. Provider cards have a 320px maximum width independent of
the explanatory sentence, and shrink within narrow sidebars.

A normal send clears the submitted text after durable local reservation and immediately
shows the user bubble with stable retained-message geometry. It must not flash
retry instructions. Before answer text appears, show accessible Thinking with
subtle staggered letter motion, disabled for reduced-motion preference. Hide
Thinking as soon as streamed or retained answer text is visible. Stopping and
reconciliation retain their own meaningful status rather than Thinking.

Only an uncertain failure or a restored, still-unobserved pending submission may
offer explicit same-key Retry after status observation settles. A successful
acknowledgement followed by history-read failure must not turn into a new retry
or automatic resubmission. Definite refusal restores the original draft; owner/
profile changes fence late state updates. The existing sidebar may still label
a running turn responding; Thinking is the main conversation waiting indicator.

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

AS-296 workflow-card graph icons use same-tab router navigation to open the
corresponding graph; they do not require integrated-browser popup support.
If that graph is already open, the icon reloads the document to fetch its saved
state. The editor's existing browser leave confirmation protects unsaved changes
and active builds; cancelling that confirmation keeps the current editor intact.
Graph navigation resets the sidebar's selected conversation; saved conversations
remain in History. A document reload also closes the sidebar and discards unsent
sidebar text, without a separate chat-draft confirmation.

AS-293 upgrade boundary: native tool manifests remain frozen for a native session.
A new conversation receives the expanded MCP surface. Earlier retained sessions
keep their exact tool set when compatible; an image/configuration mismatch requires
an explicit new conversation rather than silently replacing the native session.
History is preserved. Native commands use the same scoped MCP tools as chat;
any proposals they create still require their own human approval.

AS-293 proposals expire after 15 minutes. Receipts distinguish Expired, Commands
changed, Stopped and Interrupted as well as Completed, Failed, Rejected and
Outcome unknown. Expiry or stale discovery never grants execution authority.

AS-293 compaction completion: `/compact` may settle on one ordered native
contextCompaction item start/completion pair with the same observed thread, turn
and item IDs, in addition to ordinary native turn completion. A bounded drain
checks late failure/cancellation before normal cleanup. The receipt distinguishes
compaction terminal evidence from a model-turn result and records whether a turn
terminal was observed. Missing, conflicting or failed evidence remains unknown.
Compaction without an assistant message renders its outcome only.

AS-293 handler admission: an advertised command catalog is insufficient unless
the bound adapter explicitly advertises native command execution support. The
current handshake uses integer `nativeCommands: 1`. A base-only pinned adapter
may run ordinary chat, but native discovery is unavailable and explicit command
requests are refused before any prompt; they must never become ordinary model
text. Unknown or invalid capability fields fail initialization.


## Additional assistant providers - selected target, Laomedo305 / specs439

This extends the Codex-first slice; it is a target until its implementation and
real acceptance are reviewed. It does not retroactively claim that existing
Claude/OpenCode execution integrations already support application chat.

### AP-1: immutable provider and host-owned composition

New conversations may select Codex, Claude or OpenCode. Discovery returns actual
models/options from the selected configured provider, without inference.
Unconfigured or unavailable providers report a concrete setup/readiness reason;
no request silently switches to Codex. The initial selected defaults remain a UI
choice, not an assertion about native model defaults.

A conversation's provider is immutable. Another provider requires another
conversation. Every send/resume, native proposal/decision, Stop, Activity,
reconciliation and sign-out cancellation uses that saved provider. The tool
binding never follows the newest selected UI provider or another owner's runner.
Model responses arriving after the user selects another provider cannot replace
that selection's catalog. Draft text and retained conversations are preserved.

The concrete application calls are `runtime.models(owner, provider)` and
`runtime.runner(owner, provider)`. `AssistantRunner` composes the existing
registered provider. Extra profile/volume paths are trusted host settings, never
browser/model input or public settings output. New provider runners, locks and
private source/runtime roots are separate for each owner/provider. Existing Codex
root/key and operational identity are preserved rather than relocated. Global
OpenCode managed-startup capability is unchanged. Native sessions, credentials
and command metadata must not cross provider/owner boundaries.

### AP-2: exact built-in admission

Reuse the existing native MCP proposal and human decision surface. Native agents,
host custom commands, repository commands, plugins, publication and permission
mode changes remain excluded. Command descriptions/hints grant no authority.
A provider catalog is an observation, not a fabricated list copied from another
provider or inferred from an unadvertised handler branch.

Typing `/` in the composer opens the matching entries from the selected
conversation's complete observed native catalog. Unavailable commands remain
visible and disabled with an explanation; listing is not execution support.
Keyboard arrows navigate executable entries, Enter selects, and Escape dismisses.
Before a native session exists, show documentation previews of the pinned Codex
adapter's eleven built-ins and known Claude/OpenCode native entry points, with
only initial Codex status selectable. Other previews stay disabled pending both
actual advertisement and implemented admission/settlement support.
Previews are not a native catalog or an execution grant; no
selection sends a hidden prompt. A first Codex `/status` can create that session using an
explicit, persisted initial-native-control mode. The runner opens the session,
observes its actual supported catalog and executes native status with that
observed revision; it never submits an ordinary model prompt or fabricates a
pre-session catalog. The initial request is digest-bound and idempotent, retains
normal cancellation/cleanup/checkpoint handling, and permits subsequent messages
to continue that same thread under the [zero-turn lifetime rules](#initial-codex-status-retain-the-live-zero-turn-session).
An unused thread requires its original live controller; its ID is not durable
resumable history. Other commands and providers cannot use this initial
mode. The actual native status result uses the existing status panel and export
path, without an approval proposal or a model turn.
Exact observed slash commands use the authenticated human app route directly;
refused or uncertain native dispatch never falls through to an ordinary model
prompt. Incomplete or unmatched slash text is ordinary chat, with its original
text retained. “Known” means an exact entry in the observed provider catalog or
the AP-2 candidate names: Codex status/mcp/skills/review/compact; Claude compact;
OpenCode init/review/compact (including the unavailable compact candidate).
Those names refuse while unadvertised, and known unsupported commands or invalid
native arguments still refuse before effects. This refusal list grants no native
execution authority. Editing or choosing a new command clears only a definite
command-input rejection; uncertain dispatch and account/model/observation errors
remain fenced. A rejected input must not permanently disable Send. Whitespace
inserted by menu selection must still permit the exact initial-status mode.

Sending an exact native command or skill through the authenticated human chat
route is approval of that request, including its arguments. Do not ask again
after Send. This applies to every provider and supported native operation,
independently of its name, kind or model-use classification; no special-case
approval bypass list. Retain the same owner/session, run/thread, catalog-revision,
idempotency, atomic reservation, cancellation and outcome checks. Model-originated
proposals still require a separate human decision. Approval cards align right,
with a white Approve button; slash messages use plain right-aligned text.
Draft editing remains responsive while model discovery and history load; Send
still waits for a valid model selection and execution admission.

Claude `/usage` displays, copies and exports only its native Limits section:
reported windows, percentages, reset times and bars. Other usage report sections
are omitted from this view; the full original native receipt remains retained.
If no Limits section is reported, show that limits are unavailable without
inventing values or exposing unrelated report sections.

On resume after durable native history exists, reopen the saved native session, observe its current catalog and
validate exact command/arguments, built-in provenance, pinned handler/image and
catalog revision before any native prompt. The revision for newly admitted
providers binds provider, handler version/image and observed entries (Claude:
executable entries, as specified below). Retain the
existing run/thread/app-session and atomic-reservation checks. Refusal must never
fall through to ordinary model text or a fresh native session.
For an initial zero-turn session, use the original live session directly under
the [zero-turn lifetime rules](#initial-codex-status-retain-the-live-zero-turn-session);
expiry, cancellation or loss of that controller requires an explicit new conversation.

| Provider | Initial candidate policy | Required proof |
| --- | --- | --- |
| Claude | Actually advertised `/compact`, no arguments | Root-session raw SDK compaction boundary, or compacting start followed by native success; terminal prompt response; no native failure/cancellation. |
| Claude read-only views | Actually advertised `/usage`, `/context` and `/mcp`, no arguments | Root-session native local-command-output receipt, or an assistant local-command-run receipt with the exact command and empty arguments matched by the local-command name in the result; successful native result with zero output tokens and terminal ACP response; actual nonempty ACP view text. Missing receipts, native failure or reported model output refuse completion. No fabricated model turn or usage. Completed views show the command followed by retained native output, without a redundant completion card; usage includes only Limits. Reports may contain upstream errors and do not establish service health. Copy/export use the same displayed output, without earlier model usage or partial-model-reply warnings; full native receipts remain retained. Live acceptance remains required. |
| OpenCode | Actually advertised `/init` and `/review`, no arguments | Terminal error-free native root/child history, successful task/tool states and verified cleanup; review includes the matching completed native child. |
| OpenCode `/compact` | Unavailable in the initial pinned catalog | A handler branch and ACP end_turn without command evidence cannot establish support. |

These candidates become accepted only with real provider evidence. Commands whose
required proof or isolation is unavailable remain unavailable, with a reason;
implementation must not claim parity with Codex. Other commands require their
own traced policy, arguments and completion semantics before admission.

#### Bundled native skills

The native menu shows **Commands** first and **Skills** after, preserving provider
names, descriptions and argument hints. Search narrows both groups; headings and
the divider disappear when only one group has matches. Usable entries precede
blocked entries within each group, and blocked entries show a concise reason
rather than a generic unavailable label. Only skills observed in the pinned running CLI
are listed; the application does not invent entries from a website or a host CLI
installation. This is distinct from Laomedo's skill registry and MCP `list_skills`.
Personal, project and marketplace skill import remains outside this slice.

Skill discovery records native provenance and binds it to the current image,
session and catalog revision. Claude uses its isolated native SDK initialization
skill list; Codex retains native system scope and exact system-skill path;
OpenCode requires the pinned built-in source. Ambiguous names or missing source
evidence never grant execution. A skill must satisfy a traced provider capability
policy before it becomes selectable. Unsupported skills remain visible with a
specific reason, including provider configuration, subagents, scheduling, missing
external services or unverified requirements. Discovery never widens the existing
controller tools, writable roots, credential access or external-effect permissions.

New Claude assistant controllers select the current registered execution image
while retaining the saved account's exact native profile volume. The separate
login-custody image stays pinned for authentication operations; it does not pin
chat's adapter version. Existing run image/thread checks still refuse incompatible
resume rather than replaying history. Graph image selection is unchanged.

Claude's approval revision binds executable command/skill entries, their native
provenance, the observed skill set and the pinned image. Sort executable entries
canonically. Unavailable display-only entries may appear or reorder on native
resume without invalidating unchanged executable contracts; changes to an
executable entry or its admission requirements still invalidate approval.

Selection fills the composer with the exact native invocation and leaves arguments
editable. Human Send approves that exact request and reuses the conversation-bound
atomic decision/reservation path without another approval card. Assistant-proposed
invocations retain the exact name, arguments and model-use disclosure and require
a human decision; rejection does not dispatch. Both paths revalidate provenance
and catalog before dispatch,
without fallback to ordinary model text or a different session. Codex system skills
are extracted only into a bounded disposable controller filesystem, verified
against the pinned image manifest; no host skills or persistent profile changes.
The credential-free worker contains the same public helper tree read-only at its
native paths so bundled helper scripts remain usable without controller access.

Codex resolves native dollar skill mentions inside ordinary text as well as
structured skill input. Known bundled mentions and native skill links therefore
require the approved skill route; refuse other occurrences before native dispatch
with guidance to use the menu, preserving the text for correction. Dollar-prefixed
ordinary text such as `$20 a month` remains chat. An approved skill's arguments
cannot implicitly invoke a different bundled skill. No silent text rewriting.

A completed model-backed skill requires normal native root-turn completion plus
provider-specific evidence that the requested skill was loaded or expanded.
Completion does not imply any file, configuration or external change without the
corresponding effect receipt. Retain streamed tool activity, native errors and
cancellation semantics. Control receipts and compaction boundaries cannot stand
in for skill completion. Real discovery, approved invocation, unsupported refusal
and retained streaming outcomes are acceptance requirements for each enabled
provider. These remain pending until evidenced; a menu test is not live acceptance.
For Codex, retain an explicitly labelled adapter receipt that the verified native
structured skill input was prepared and its root turn accepted, including the
unique invocation ID, native session/turn IDs, canonical skill/path and image
manifest digest. Require this receipt in order between the matching native turn
start and completion; a generic successful turn or an old receipt is insufficient.
This admission receipt does not claim a native file or external effect.

Claude built-in provenance requires disabled host/project setting sources and
no custom/pinned skill collision. Native root identity and current-attempt
boundaries must exclude replayed or child compaction receipts. Native command
completion has its own receipt: no invented assistant answer, model turn ID,
model usage or success event. Observed compaction context occupancy is distinct
from model-token usage. Failed/cancelled/conflicting or missing evidence cannot
be reported completed. A normal message resumes the same settled native thread.

OpenCode's command templates perform shell interpolation before native tool
permission checks. This slice therefore permits no arguments. The pinned built-in
templates themselves must be checked for controller-side shell expansion.
A generated command subtask is not proof that the model's native Task tool is
available; its actual child permissions/tool exposure must preserve worker-only
execution. Do not enable unrestricted Task, shell or file tools to make a command
work. Require real evidence alongside source/configuration checks.

OpenCode commands run in an isolated controller view, not the user's repository.
Approval must disclose that files/Git state may be unavailable and `/init` may
create AGENTS.md only in the scratch environment. A command completing is not
proof that it changed a file or reviewed a repository: claim those effects only
with their own actual receipts. A swallowed child failure, tool error or unknown
slash no-op followed by end_turn cannot count as successful native execution.
Terminal native commands whose admitted tool or assistant step reports an error
are retained as known failed commands (`opencode_native_command_failed`) with
their actual response. Once cleanup is confirmed they are not presented as
uncertain remote work, and claim no file or repository effect. Incomplete,
unadmitted or unlinked native work remains unconfirmed.

### AP-3: truthful display, cancellation and acceptance

Conversation rendering, copy/export and Activity use the actual provider. Native
command messages remain plain right-aligned text. Codex-specific status parsing
must not be applied to Claude/OpenCode output. Exact observed responses and
outcomes remain visible; unsupported fields remain unavailable.

Stop and session revocation must target the bound provider's actual active
attempt, including native review children. Acknowledgement alone does not prove
cancellation or cleanup. If settlement is uncertain, retain unknown state and
never replay automatically. Provider-specific resume limitations must be stated;
do not silently resume a cancelled run as a new session.

Acceptance for the additional slice:

- Actual configured Claude/OpenCode model discovery and fresh chat, then normal
  resume on the same native thread through the existing Laomedo MCP tools.
- Independent owner/provider roots and concurrent routing; existing Codex state
  remains usable. Delayed catalog results and Stop/revocation never cross them.
- Human-approved supported native command, rejection/revocation, changed catalog
  refusal and exact command grammar; model cannot approve itself.
- Claude compaction completion with genuine root native evidence and no invented
  text/usage, followed by same-thread chat. Exercise Stop against active work.
- OpenCode built-in provenance and no-argument admission; actual child permission
  and terminal receipts for review; no success for missing/error/no-op evidence.
  Disclose unavailable repository context rather than pretending a review occurred.
- Actual rendered provider selection, responses, approvals and outcomes reviewed
  in the shared integrated browser. Fixture tests do not establish live acceptance.
- Reviewed canonical spec, full substantive code diff, required CI and explicit
  remaining limits before merge; parent Codex spec/implementation dependencies
  are merged or separately accounted for, never assumed.


## Saved account chat binding ? selected owner direction, 2026-11-20

The owner requested wiring chat to the saved provider login capability on
`develop`. New chats default to the first connected, ready account in the current
profile's safe saved-account list for the selected provider. If none is ready,
a connected account with an expired access token may default into the existing
guarded discovery and credential-refresh path. Revoked, reauthorization-required
and unavailable accounts never default except OpenCode's `opencode_go_key`
local-custody summary: its unavailable state means upstream authentication is
unverified, while missing custody is revoked. This may default into guarded
discovery; it does not certify authentication or bypass admission.
Connect account and Manage accounts open Settings > Providers in the current
tab, without depending on integrated-browser popup handling. Retain unsent drafts
and provider in profile-scoped tab session storage before navigation, restore once
on return, and clear on profile changes or locking. If storage fails, ask before
discarding the draft. Preserve the editor's unsaved/build document-navigation
guard when opened from the assistant sidebar. The visible account
choice can be changed before chat starts. Defaulting waits for that profile's own
list to load; it never uses stale accounts from a different profile. It does not
create a conversation, dispatch a command or send a model prompt. When no choice
is selected, the composer placeholder says Select an account, or No account
available when that provider has no connected account; it does not show a stale
model/effort or a separate selection paragraph. Model discovery uses that exact
connection. Conversation creation retains its opaque
connection UUID and observed connection generation, independently of model and
effort. The binding cannot change within the conversation. No service account,
host token, different provider or graph preference is an implicit fallback.
Existing conversations never switch their saved account or generation, even if
another account is ready. An explicit choice in a new chat is not overwritten by
list refresh or discovery.

Chat uses the existing saved-account controller, credential admission and
isolation paths for Codex, Claude and OpenCode. Its controller state and scratch
source are separate from graph execution. Account disconnect inventories and
cancels both graph and assistant work, including unresolved resume reservations;
startup recovers both scopes before continuing a pending disconnect. Graph calls
cannot resolve an assistant run. Credential material never enters chat rows,
model arguments or browser responses. Native browser session leases and profile
revocation remain enforced; account selection does not authorize native commands.

Normal signed access-token renewal retains the originating browser's assistant
approval identity through the profile boundary's verified renewal binding.
Persist only token fingerprints and their canonical authority, never bearers.
Retain verified bindings with the session revocation fence across restart: a
renewed token must not become a new authority after logout because an in-memory
alias map was lost. Logout also fences a renewed token not yet used by chat.
Owner mismatches, conflicting bindings and revocation refuse; unrelated logins
cannot inherit pending approvals. Existing pre-fix proposals require a fresh
proposal rather than being rebound to a different browser session.

Acceptance covers a normal renewal and page reload with an approvable proposal,
subsequent renewal after service restart, and logout through an unused renewed
token followed by restart. The latter must remain refused with a still-valid
signed token. Model execution is not needed for the database revocation checks.

Disconnected, removed, changed-generation and unbound conversations keep their
retained history but refuse new native operations. A new account needs a new
conversation. The transition must not abandon earlier operational state: if an
old dedicated chat runner retains active runs, unresolved resume dispatches or
resource receipts, block new assistant dispatch while preserving app, Settings
and graph availability and the old files for explicit reconciliation. This
transition check can retire only after the older operational state has been explicitly reconciled; it does not require personal graph export
compatibility.

Acceptance requires tests for account defaulting, explicit override, foreign-profile and generation
refusal, no fallback, independent graph/chat sources and run lookup, disconnect
inventory/cancellation and assistant-only restart recovery. Real saved-account
chat, initial status, MCP use and same-session continuation remain live acceptance
requirements; fixture checks alone do not establish them. Implementation/review
and live acceptance are pending.


### Initial Codex status: retain the live zero-turn session

The owner selected keeping the actual native controller alive between first
`/status` and the first ordinary message. The pinned Codex does not persist an
unused thread, so closing its controller and later attempting disk resume cannot
meet the same-thread contract. Do not submit a hidden turn, reconstruct a rollout,
replace the thread or replay the message to work around that limitation.

- Status completion and resource cleanup are separate observations. An idle live
  session keeps exact controller/executor ownership and its original native
  event loop. The first ordinary message uses that same live ACP/native session.
  Once a model turn has materialized durable history, normal cleanup and later
  native resume apply.
- No tool authority survives between messages. An inactive transport may remain
  attached to the retained native session, but its owner/conversation/browser
  binding must match and its current message authority must be reestablished
  before any tool call. The frozen manifest cannot expand during reuse.
- Account disconnect, browser logout, conversation deletion, explicit
  cancellation, native failure and app shutdown release the idle native
  ownership. Observe cleanup; do not rewrite a completed status command as a
  failed model turn or claim an uncertain cleanup succeeded.
- An unused session has an explicit host-configured idle lifetime, independent
  of model-turn execution limits. Expiry closes it and makes continuation
  unavailable; it does not silently start a replacement session. Credentials
  must still satisfy the saved account/generation fence at the first model turn.
- The owner selected in-place native credential refresh. Routine OAuth token
  rotation for the same admitted account and generation must update the retained
  controller before inference without replacing its native thread. The host
  remains the OAuth-refresh owner; the executor receives no credential, refresh
  token or credential-store mount. An unconfirmed update or changed account
  binding refuses before prompting and releases exact owned resources; it never
  recreates or replays the session. A token's byte value changing alone is not
  grounds to require a new conversation.
- After restart, reconcile the exact saved resource receipt. An unmaterialized
  session is unavailable if its process was lost; its indexed thread ID alone is
  not resumable history.

Acceptance must demonstrate real status, first message and contextual follow-up
with one native thread, real OAuth token rotation followed by the first model
message on that same thread, real Laomedo MCP use under the new message authority,
inactive tools between requests, and idle ownership cleanup on
disconnect/shutdown. Implementation and reviewer acceptance remain pending.


### History panel and native command results

The conversation list heading is **History**. Titles use muted text, with faint
separators between conversations. Its scrollbar sits at the panel's right edge,
beside the single arrow divider. In the full-page chat, drag that divider to
resize history (180-480px, further bounded to the available width), or click it
to collapse/reopen. Drag release must not collapse the panel. Arrow keys adjust
24px; Home/End use the bounds. Resizing and selection never dispatch a turn and
preserve the draft. The existing editor assistant retains its separate panel
width and resize controls.

Completed native commands show the user's command followed by its actual
retained output, without a separate "Ran /command. Completed" receipt card.
Pending assistant-proposed approvals and non-success/uncertain outcomes remain
visible. Persisted completion receipts remain authoritative for reconciliation
and are not deleted merely because their redundant UI card is suppressed.
