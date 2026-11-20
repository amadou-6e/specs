---
title: Human-approved assistant graph actions
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-11-17
applies_to: [laomedo]
supersedes: null
related: []
---

# Human-approved assistant graph actions

Selected extension: specs #430 and Laomedo #291. This adds approval-gated editing
and execution to the persistent assistant; publication is explicitly deferred by
the owner. Native provider permission modes remain separate (#288). The existing
six read/draft tools keep their narrower behavior until this extension is installed.

## Concrete tools and app routes

- `propose_graph_edit(operation_key, workflow_id, expected_revision, changes, summary)`
  records a bounded patch; applies it only with existing human-granted category consent, otherwise waits for an app decision. Changes name exact existing node IDs
  and writable static settings, trusted installed nodes to add, nodes to remove,
  and exact named connections to add/remove. No executable templates or secrets.
- `propose_graph_run(operation_key, workflow_id, expected_revision, input_value,
  input_type, output_type, summary)` records the exact run request; dispatches only after human approval or under existing human-granted Run consent.
- `get_graph_action(action_id)` reports that conversation's authoritative action
  state and safe result identity, without private graph bytes or raw run outputs.
- Authenticated `POST /conversations/{id}/actions/{action}/decision` with
  `{decision: approve|always_approve|reject, digest}` is a human app operation. It is not an MCP
  tool. Natural-language approval and model tool arguments cannot invoke it.
- Conversation detail includes bounded action summaries/cards across turn end,
  reload and app restart. A proposed tool call returns the authoritative current
  state: pending without category consent, or the admitted outcome under existing
  consent. The native agent never holds a tool call open waiting for the human.
  Approval does not automatically resume the agent or submit another model turn.
  The next explicit user message can read action outcomes through the MCP tool.

## Approval and preview

Bind action to owner, original app session, conversation/message/attempt,
operation key, action kind, workflow identity and full observed revision,
canonical request digest, creation and expiry times. The server constructs the
preview from the actual saved graph and validated patch, not the model's summary.
The same operation key and identical semantics return the same action; changed
semantics under that key refuse. Pending proposals expire after 15 minutes.

The card foregrounds Rename workflow, Edit workflow or Run workflow, the target
name, and a short plain-text description supplied by the agent (maximum 240
characters, part of the request digest). Rename shows the actual old and new name,
not the agent's summary. The server derives Rename only for name-only changes;
settings, nodes, connections and mixed patches are Edit. The agent must not repeat
approval boilerplate, proposal IDs or revision hashes in its chat reply.

Owner decision (2026-11-17): Edit cards retain only the agent's short description,
without server-verified operation counts or an additional effects summary. That
description is digest-bound, not independent verification of the patch; category,
revision and policy checks remain server-enforced.

Buttons are Approve, Always approve renames/edits/runs, and Reject. The Always
scope is stated alongside them: any graph in this conversation. Use muted, regular-weight change text and a small operation heading. A top-right
external-link icon opens the graph in a new tab, with an accessible name and
tooltip. No technical Details section, revision/proposal/run IDs or expiry text
is rendered in the card. Backend receipts retain those identities. Settled cards
collapse to operation, change description and a short outcome: Renamed, Edited,
Completed, Rejected, Expired, Failed, Not started or Outcome unknown. The outcome
is below the description and aligned left, never grouped beneath the graph icon.
All categories share one muted, regular-weight sentence and no separate title or
standalone workflow-name row. Rename says Rename/Renamed workflow "old" to "new".
Edit says Edit/Edited workflow "name": brief change description. Run text is a
sentence using the actual server-built input: Run workflow "name"
with input "value" while pending, Running workflow while executing, and Ran
workflow only after success. An empty input is shown explicitly as "". Do not
repeat the model's input summary or infer success from its wording. Do not add a
separate Saved graph updated sentence. Relevant failure/recovery meaning remains
in the outcome tooltip; uncertain effects are never labeled a definite failure. Model text is
rendered as data, never HTML. A run card states that existing components may
consume model quota and perform their configured external actions. Preview inputs
are non-secret only; credentials must remain configured through existing settings.

Approve applies only the displayed digest. Always approve also grants the actual
server-derived category across any owned graph in this conversation and original
app session. Rename, Edit and Run grants are independent; no cross-conversation or
cross-login consent. The grant is created only when that current action is admitted
successfully, never on stale/expired/rejected/failed admission. It does not bypass
revision, ownership, editability, component policy or execution permission checks.
Subsequent proposals under that category recheck authority and consent inside the
same serialized decision transaction, then apply/claim once; without consent they
remain pending. The model cannot create/revoke consent or choose its category.
Conversation UI lists current grants with Ask every time per category. Human-only
POST /conversations/{id}/permissions/{category}/revoke serializes with action
decisions; it prevents subsequent admission, not already-admitted effects. Native
logout/revocation invalidates that session's grants. Reject/expiry causes no effect. A changed
workflow, revoked session, wrong owner/conversation or unavailable target refuses
before any write/dispatch; a fresh proposal is required. Never silently rebase.
Pending proposals from a revoked originating session cannot be adopted by a new
login. Read responses indicate whether this app session can decide; cards from
another session show fresh-proposal guidance without approval controls. Native
auto-login may rotate the session cookie when reopening a page or editor tab;
then a fresh proposal is required. Access is checked inside the decision
transaction and before execution.

## Safe graph editing

Use the existing workflow owner's transaction/row guards, full revision check
and editability rules. Preserve original IDs, positions, viewport, hidden fields,
secret references and component code for untouched/existing nodes. Apply only
explicitly named changes. Never reconstruct an existing graph from the lossy
non-secret MCP projection. Validate static values/port compatibility against the
trusted installed component catalog without running update hooks or component
code. New nodes use installed templates; secret/code/host-routing fields remain
unwritable. Removing a node also removes its incident edges and the preview says so.
Refuse locked/published/filesystem-managed flows under existing edit rules.

The edit and successful action receipt commit atomically. The assistant refuses a changed base revision, and duplicate approval clicks
cannot repeat an edit. Ordinary editor PATCH does not require an expected revision:
an already-open editor can later overwrite the approved change. Both the pending
and success card's graph-link tooltip must warn that open editors need reloading
before saving, to avoid overwriting saved changes. No automatic reload or unsaved-work loss is
allowed. Approval changes the saved version only; this is not bidirectional
editor conflict prevention. Opening is an explicit separate-tab action.

## Execution and uncertainty

Use Langflow's existing workflow execution owner and its normal caller permissions,
component policy, provider policy and identity checks. No new graph executor,
broad app token, model-callable execute tool or provider modification is added.
Recheck the target revision under its row guard, claim the action durably, detach
an exact in-memory graph snapshot, and execute that snapshot with the approved
inputs and a stable action-owned run/session ID. Do not reload a changed graph
or reuse a cached template from another revision. Existing configured credentials
and external services remain live dependencies; approval is not a snapshot of them.

Run inputs are limited to 12000 characters. Pinned SimplifiedAPIRequest accepts
input_type chat/text/any and output_type chat/text/any/debug; the proposed tool
exposes that exact list, defaults to chat/any, and includes every input in its
digest. The server derives session_id from the action ID; the model cannot
supply session_id, tweaks, output_component or tracing user_id. The run executes
as the approving app user, resolving that user's configured credentials and global
variables. Use context={} for the existing cold execution path; this is not a
claim that the revision-checked warm cache is stale.

A last-moment authority/input refusal before entry into the execution owner is
recorded as not_dispatched, with no graph execution claimed. Once execution is
entered, exceptions are reconciled against the actual exact-owned job; unknown
effects remain unknown rather than being mislabeled a definite no-dispatch.

Run states are pending -> executing -> succeeded/failed/unknown/not_dispatched, or rejected,
expired/stale before dispatch. Persist executing before any execution call. Repeat
approval returns the existing state and never dispatches again. There is no claim
of exactly-once completion across a process crash: interrupted executing actions
are reconciled against the existing job service using their run ID and exact
owner: completed/failed jobs resolve their outcome; absent/nonterminal/ambiguous
jobs become unknown and are never automatically rerun. App shutdown requests
task cancellation but does not claim graph effects were cleanly cancelled. Retain stable run ID
and direct the user to inspect actual history before proposing another run.
Unknown must not be labelled failed-with-no-effects. Raw execution exceptions and
outputs are not returned to the model; safe status and run identity are retained.
Graph execution is independent of the chat's Stop: closing chat or stopping the
assistant does not cancel an approved graph run. Profile revocation prevents new
approval/dispatch; it does not claim cancellation of already-admitted graph effects.

## Completion checks

Controls cover model inability to decide, wrong-owner/session/revocation/expiry,
digest conflict, stale revision, safe preview and secret/code preservation,
atomic edit/receipt, duplicate approval and no dispatch before approval, exact
snapshot/input execution, policy enforcement and restart uncertainty without replay.
UI checks cover both approval cards, exact preview, reject, stale/unknown outcomes,
reload and keyboard accessibility. Real app/editor acceptance must show a graph
unchanged before approval, edited once after approval and preserved on rejection;
a real small graph must run only after approval, with its actual run outcome.
Acceptance includes an editor already open on the edited graph and the explicit
reload warning, rather than claiming the editor cannot overwrite it.
Fixtures and proposal renders alone are not real integration acceptance. Independent
code/spec/actual-render review and final-head checks are required before merge.


## Compact approvals and remembered consent checks

Verify server-derived Rename/Edit/Run, digest-bound model description, actual old/new
rename values, compact controls, muted change text, external-link icon and collapsed outcomes. Human Always approve
must cover any graph in this conversation only, independently per category and
originating app session. Test revocation, cross-conversation/session refusal,
category escalation refusal, stale revision and repeated same-key admission. Real
native MCP and browser checks must demonstrate the first explicit grant, a later
covered proposal, an uncovered category and revocation without automatic replay.


## Conversation transcript controls

The conversation header offers Markdown export of all retained user and assistant
text, including older message pages and normalized answer text. Tool payloads and
hidden native records are excluded. Export is a snapshot; active, unavailable or
partially retained answers are identified rather than claimed complete. One accessible copy action below each response copies all retained
agent activity since that user request: assistant messages, tool/command names
and their displayed inputs/outputs in retained activity order, followed by graph
action outcomes and saved drafts. It excludes that user message, native prompt wrappers and other
requests. Streaming/incomplete copies are marked snapshots. Copy success/failure
is shown locally. Export must abandon results if the owner, profile or conversation
changes during collection. Neither action submits a prompt or changes consent.
Reduce stacked bottom padding so the last answer stays close to the composer.


## Delete conversation

A trash icon beside header Export opens a confirmation naming the conversation.
Cancel leaves it intact; Delete removes the owned conversation from Laomedo
history, including its
messages/activity snapshots, draft/action receipts and remembered permissions.
Saved workflows and independent workflow run history remain. Native provider
thread/session records are outside this deletion; no provider-side erasure is
claimed. The confirmation says "Delete from Laomedo history". Deletion is refused
while an assistant response is active/unsettled or a graph action is executing;
stop/wait for settlement first. The server enforces owner, current app-session
authority and concurrency under the same transaction/row lock as Send and graph
approval. Pending proposals disappear with the conversation and cannot execute.
Linked successor conversations remain, with the deleted predecessor link cleared.
After success, clear that chat's local draft/pending state, remove it from history
and show a new conversation. Failure keeps the chat visible with retry guidance;
no automatic retry. A changed owner/selection must not receive late UI updates.
