---
title: Persistent application assistant realization proposal
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-11-17
applies_to: [laomedo]
supersedes: null
related: []
---

# Persistent application assistant realization proposal

Behavior belongs to [the assistant contract](../contract/application-assistant.md).
Geometry/states/transitions belong to [the editable design](application-assistant.drawio).
The owner authorized the implementation in Laomedo #282 / PR #283 and then
selected the revised controls recorded in the contract and editable design.
Implementation reviewed at `7911f134bf29bf2e11c37ecbe9ae87fe1ba43687` uses the
pinned Langflow/LFX1.12.3 checkout `fec71dca901949c09ed4d63315804337cd2eb13d`.
This amendment records the selected behavior; it does not promote the broader
agent-execution subsystem or claim acceptance for other providers.

## Concrete arrangement

```text
Application chat UI
    -> authenticated conversation routes
        -> existing provider runner HTTP start/resume/status/cancel
            -> provider native session, isolated runtime
                -> existing scoped MCP forwarder
                    -> app-owned native MCP client
                        -> real Laomedo authoring MCP server
                            -> existing workflow and Skill owners

Existing attempt-scoped Activity -> conversation UI
Atomic workflow save + receipt -> verified draft card -> user Open action
```

No assistant workflow, new provider interface, separate inference SDK or replacement
workflow store. The application controller owns conversation orchestration around
existing providers. The assistant's authored drafts are normal workflow definitions
with explicit draft provenance; they are never passed to graph execution by chat.

## Material interfaces

Application HTTP, authenticated in the same app/profile context as ordinary UI:

```text
POST /api/v1/laomedo/assistant/conversations
  {provider, model, effort} -> {conversation_id, state}
POST /api/v1/laomedo/assistant/conversations/{id}/messages
  {client_message_id, text, model?, effort?} -> 202 {message_id, attempt_id, state}
PATCH /api/v1/laomedo/assistant/conversations/{id}
  {title} -> updated owner-scoped conversation; no inference
GET /api/v1/laomedo/assistant/conversations
  ?cursor=... -> bounded conversation summaries
GET /api/v1/laomedo/assistant/conversations/{id}
  ?cursor=... -> bounded messages, active attempt, saved-draft receipts
GET /api/v1/laomedo/assistant/conversations/{id}/activity
  ?attempt=...&after=... -> existing normalized Activity page projection
POST /api/v1/laomedo/assistant/conversations/{id}/stop
  {attempt_id} -> cancellation observation, not teardown assertion
```

The controller, not the browser/model, supplies runner IDs, profile/daemon binding,
native thread, workspace checkpoint, request identity and private credentials.
Callers cannot choose a runner URL/token or an arbitrary local path.

Actual existing runner endpoints are `/v1/runs/async`, `/v1/runs/{id}/resume`,
status `/v1/runs/{id}`, `/v1/runs/{id}/activity`, `/v1/runs/{id}/cancel`, request
lookup and `/v1/models`. First submit uses stable `request_id`; follow-up resume
uses recorded `expected_thread_id`, `expected_post_run_hash`, model/effort and a
new `activity_attempt_id`. A supported new model/effort pair resumes the same
native thread/run; model equality is not a continuation requirement. Account,
workspace checkpoint, request identity and settled-resource checks still apply.
First-attempt identity must be observed/bound using
the actual current runner representation, not an invented resume-only field.
The current resume HTTP call is synchronous: dispatch from an application-owned
background job, return the durable app attempt immediately and poll Activity.
Browser disconnect must not terminate/replay the background dispatch.

Required runner addition: durable idempotent resume admission and lookup keyed by
`(run_id, activity_attempt_id)` plus semantic request digest. Return the existing
attempt for duplicates, refuse changed content and reserve before native dispatch.
Transient MCP references/capabilities are excluded from the semantic digest.
Admission checks precede MCP claim/replacement so a duplicate cannot steal or
revoke the active grant. App message jobs alone cannot guarantee this across a
lost synchronous resume response. Preserve existing direct API behavior for callers
outside this explicitly scoped idempotent path; do not add chat-specific provider methods.

## MCP server and client reuse

Proposed transport: a real FastMCP HTTP tool surface hosted in the existing local
application, with an app-owned native HTTP MCP client. It shares authenticated
domain services with ordinary UI operations; it does not pass general app API
credentials into a provider. A private host credential identifies a server-side
conversation binding; owner/conversation are not model-selectable arguments.
Prefer this in-app surface over a new STDIO process per chat if supported safely
by the pinned package. This hosting choice needs the bounded source check below.

The tool surface implements only the contract's six operations. The native client
returns actual MCP tools, adapted using existing `LangflowMcpTool` and registered
with `McpRegistry` on the app event loop. This is the same protocol/forwarder as
graph tools, with app-owned connection lifetime rather than graph registration.
Do not introduce descriptor/invoke-only Python tools as a second public protocol.

Open native connections lazily after app startup, not by HTTP-calling the app
before its listener exists in lifespan startup. Compose server/client/registry
lifespans: revoke provider grants, settle/reconcile owned work, close clients,
then stop the tool surface. All host endpoints remain explicit local/private;
MCP presence is not blanket authority to the general workflow API.

The parent application's composed lifespan must explicitly enter the MCP server's
`session_manager.run()` exactly once; mounting its Starlette sub-app alone does
not establish that lifetime. Compose this with the existing registry/upstream
lifespans. Set explicit narrow MCP Host/origin allowances for the actual local
deployment; do not use wildcard host trust or disable transport protection.
Use literal loopback for the private native connection. Verify LFX's real connector
and HTTP-transport SSRF settings with that connection; tests which disable SSRF
are not acceptance. Never globally turn protection off. Pinned source exposes
`connector_ssrf_allow_loopback` and `ssrf_allowed_hosts`; any needed configuration
change must be scoped, explicit and reviewed rather than applied silently.
Handlers use asynchronous DB operations or bounded off-loop work so self-HTTP
does not block the app loop. If supported HTTP hosting/client admission cannot
meet these conditions, return a documented proposal revision for a real STDIO
MCP server; do not silently add a private socket protocol or general app API key.

Each attempt registers a fresh scoped forwarding capability with a stable tool
manifest; completion/cancel/expiry revokes it. Idle MCP sessions may be closed
and reopened. Schema/identity changes on upgrade fail the existing exact-manifest
binding, retain history and require an explicit linked new conversation; do not
patch manifests in retained runs silently.

The upstream `lfx.mcp` server is reference/reuse material, not enabled wholesale.
It offers login, arbitrary flow IDs, deletion and execution; `validate_flow`
calls `/build/{id}/flow`, and `create_flow_from_spec` defaults to executing that
validation. Component configuration can run update hooks. Reuse only inspected
pure graph/parser/metadata helpers. Do not expose these broad tools and rely on
the prompt to avoid their effects.

## State ownership and storage

Use the app's existing database/owner context. Proposed concern-owned tables:
conversations, messages/attempt dispatch reservations and draft-operation receipts.
Do not store an unbounded message list in one row. Bind every lookup to the owner;
stable message keys are unique within a conversation. Transactions own active-turn
reservation and idempotent response recovery. Durable jobs/reconciliation handle
the gap between reservation and a remote runner acknowledgment.

Use ordinary Langflow flow records for complete saved drafts. Extend the owning
flow persistence service with an atomic create/update-plus-receipt operation and
assistant expected-revision check under the same row-lock/transaction discipline
as editor writes; no parallel workflow database. Refuse an assistant save when
the editor has changed the row. Changing the editor PATCH API itself is outside
this proposal.
The exact service seam must be verified. Store canonical request digest with each
save key. Applying identical keys returns the prior receipt; changing semantics
under the same key refuses. Model output contains a typed graph description, not
raw executable component JSON.

## Normal message flow

```text
User sends "Combine Research and Implement using Skill X"
  app reserves message M1 in conversation C
  app binds C's authoring MCP tools and registers fresh forwarding access
  existing provider runner starts the first message
  model reads source workflows/component schemas/Skill refs via MCP
  model calls save_draft with exact source revisions and operation key
  workflow owner validates metadata and atomically saves draft D plus receipt
  Activity streams; app exposes D from the receipt even if the turn later fails
  terminal attempt revokes tool access and unlocks Send after settlement
User clicks Open on D -> new app tab; original editor is untouched
User selects model/effort and sends M2 -> same provider/native session,
  immutable turn selection, new attempt and MCP capability
```

## Provider continuation is a gate, not a status-string relaxation

Current Codex/Claude/OpenCode admission generally requires a completed previous
attempt. Codex also has authentication-mode/runner-restart binding restrictions;
workspace snapshots, account/image/config identity and cleanup remain significant.
The consultation's suggestion to accept more terminal statuses is insufficient.

Trace each provider's actual cleanup/finalization paths and native session behavior
before designing the smallest correction to existing resume admission. First
support Codex Stop/failure-follow-up with evidence, preserving current workflows.
Resume is a new prompt after safe settlement, never automatic replay of a crashed
turn. Retain refusal when the session or workspace checkpoint is unavailable or
effects/owned work remain uncertain. Other providers require their own evidence.

Provision an app-owned minimal assistant source tree and private state/Skill store
through existing runner setup. `BaseAgent` binds its source at construction and
does not accept arbitrary per-message source paths. Do not reuse an instance
configured for the user's repository. No publication controller or GitHub grant
is supplied. Confirm allowed workspace shape and isolated worker mounts rather
than assuming an empty directory is admissible under every provider.

## Realization sequence and evidence boundary

1. Inspect metadata-only graph helpers, transactional flow persistence, native MCP
   HTTP hosting/client lifecycle and current runner setup. Resolve mechanisms
   against this contract; do not run model probes merely to explore APIs.
2. Implement runner-side idempotent resume/lookup and continuation safety for the
   initial provider, with meaningful current regression tests. Reuse observed
   attempt/cleanup fields only where their actual guarantees suffice; a boolean
   named finished or cancel-confirmed alone is not proof of all owned work settling.
   Prepare bounded live Stop/failure/session checks separately
   on `exp` when authorized; no production verification-only turn caps.
3. Implement the workflow owner's atomic draft/receipt operation, pure validation
   and six MCP tools. Check stale/concurrent/idempotent/uncertain save behavior.
4. Add conversation persistence, authenticated routes, app-owned dispatch jobs,
   native MCP lifetime, profile fences and Activity projection around existing APIs.
5. Implement the reviewed normal chat UI and consent-based new-tab draft opening.
6. Real initial-provider acceptance: multiple messages, tool-created draft, editor
   inspection, Stop/failure follow-up, lost response, restart/history and privacy.
   Reviewer code/spec/actual-render coverage and final owner validation are separate.

## Review questions and known gaps

### AS-311 authoring and observation extension

Specification #443 and Laomedo #311 extend the existing authoring MCP. A4's
AC311 rows show resolution/readiness diagnostics, observed run outputs and
requested/settled cancellation in the existing chat tool/result language. They
add no parallel editor or automatic model execution. Dynamic choices come from
audited resource owners, not component Python hooks. Exact supported coverage,
resolution lifetime, validation, binding and result-release rules belong to
AS-311 in the contract. No final implementation or visual acceptance is claimed.

The initial source checks and implementation acceptance are summarized in
[validation](../validation.md#application-assistant-implementation-2026-11-17).
The selected chat controls, per-turn configuration, retry identity and keyboard
feedback supersede the original fixed-model/header-metadata proposal. Provider
change still creates a separate conversation. No permission dropdown or tool
for running/publishing/updating original workflows is introduced. Human-approved
workflow actions require a separate selected specification and implementation.
