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

- `propose_graph_edit(operation_key, workflow_id, expected_revision, changes)`
  records a bounded patch, never applies it. Changes name exact existing node IDs
  and writable static settings, trusted installed nodes to add, nodes to remove,
  and exact named connections to add/remove. No executable templates or secrets.
- `propose_graph_run(operation_key, workflow_id, expected_revision, input_value,
  input_type, output_type)` records the exact run request, never starts it.
- `get_graph_action(action_id)` reports that conversation's authoritative action
  state and safe result identity, without private graph bytes or raw run outputs.
- Authenticated `POST /conversations/{id}/actions/{action}/decision` with
  `{decision: approve|reject, digest}` is a human app operation. It is not an MCP
  tool. Natural-language approval and model tool arguments cannot invoke it.
- Conversation detail includes bounded action summaries/cards across turn end,
  reload and app restart. A proposed tool call returns promptly with pending
  status; the native agent does not hold a tool call open waiting for the human.
  Approval does not automatically resume the agent or submit another model turn.
  The next explicit user message can read action outcomes through the MCP tool.

## Approval and preview

Bind action to owner, original app session, conversation/message/attempt,
operation key, action kind, workflow identity and full observed revision,
canonical request digest, creation and expiry times. The server constructs the
preview from the actual saved graph and validated patch, not the model's summary.
The same operation key and identical semantics return the same action; changed
semantics under that key refuse. Pending proposals expire after 15 minutes.

The card shows Edit graph or Run graph, target name/revision, readable exact
field/node/connection changes or run inputs, and Approve/Reject. Model text is
rendered as data, never HTML. A run card states that existing components may
consume model quota and perform their configured external actions. Preview inputs
are non-secret only; credentials must remain configured through existing settings.

Approve applies only the displayed digest; no approve-all, remembered consent or
permission to approve a later revision. Reject/expiry causes no effect. A changed
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
and success card must warn: Reload open editor tabs before saving; unsaved editor
work may overwrite this saved change. No automatic reload or unsaved-work loss is
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
