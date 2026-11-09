---
title: Graph-connected MCP tools
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Graph-connected MCP tools

Owning issues: [specs #418](https://github.com/amadou-6e/specs/issues/418),
[implementation #280](https://github.com/amadou-6e/laomedo/issues/280).
This is a target contract, not evidence of implementation or live acceptance.

## Graph interface

The optional list-valued **MCP Tools** input accepts the native MCP node's
**Toolset** output. Server registration and selection stay on the existing
Langflow node. Skill References remain independent and may be connected alongside
MCP Tools. The editable [Agent node controls](../design/agent-node-controls.drawio)
own the input placement, connection example and failure states. No connection
preserves existing Agent behavior. Whole-flow MCP publication is outside scope.

## Authority and selection

Support the existing trusted single-user local deployment. Do not claim multi-user
ownership. The app owns upstream clients and credentials; isolated controllers see
only an invocation-scoped authenticated forwarding endpoint. Workers remain
network-free. Every transport goes through the exact selected-tool allowlist;
upstream endpoints, credentials, environment and STDIO commands do not travel in
graph/task data or durable Agent records.

Freeze selected original tool identities and input schemas into a bounded manifest.
Keep display aliases separate. Reserve internal `laomedo`; namespaced exact external
grants extend provider allowlists without widening internal permissions. Reject
ambiguous duplicates and unsupported approval requirements. New server tools never
enter an admitted grant; missing or changed selected tools fail closed.

## Identity and lifecycle

The manifest participates in canonical request identity and persisted non-secret
run binding. Transient registration references and runtime bearer tokens do not
define semantic identity. Admission verifies manifest equality even on idempotent
retries; replay must not replace an existing active registration or leak a new one.
Resume re-registers the identical manifest with a fresh capability or refuses the
binding. Status/cancel do not build upstream MCP nodes or open upstream connections.

The app lifespan retains selected tool objects and their original live event loop
after asynchronous start returns; compose with upstream startup/shutdown. Reject
registration without that owner or on another loop. Revoke before upstream app
shutdown, and on admission/launch failure, cancellation, final completion and lease
expiry. Borrowed shared clients remain Langflow-owned. App/loop loss stops access
and fails attempts closed; no direct upstream fallback or automatic reconnection
under a different identity. The runner may outlive the app, but cannot retain
external tool access after app loss.

Default forwarding bind is loopback. Permit an explicitly configured private
Docker-reachable interface; refuse wildcard binds. Do not alter firewall rules or
silently broaden exposure. Existing OpenCode internal broker binding is unchanged.
Authenticate every request with a high-entropy scoped capability, compare in
constant time, enforce bounded leases and revoke immediately. Capabilities appear
only in private host/native configuration, excluded from public serialization.

## Calls and failures

Preserve schema validation, original upstream names, structured MCP content and
`isError`. Never replay a call after dispatch, including inside a borrowed native
client. Timeouts/cancellation can leave effects unknown; report that rather than
retry. Bound schemas, arguments, results, concurrent calls and registrations.
Treat results as untrusted data, never new authority. New Laomedo events retain
identity/duration/outcome only, not arguments/results; provider-native history can
contain model-visible content and must be disclosed separately.

Missing registration, connection loss, changed bindings, invalid credentials,
unsupported native shapes/versions or approval requirements produce stable safe
failure categories. Never expose upstream exception text containing secrets.

## Acceptance

- Native MCP Toolset connects without re-entering server configuration.
- Codex, Claude and OpenCode each discover/invoke tools from HTTP and host-owned
  STDIO servers; test all six combinations using harmless read-only tools.
- Multiple servers coexist with Skill References; selection cannot be bypassed.
- Asynchronous start retains working tools after the graph build returns.
- Resume checks exact manifest; status/cancel open no upstream connections.
- Completion/failure/cancellation/app shutdown revoke access without closing
  unrelated pooled clients; no uncertain invocation is replayed.
- Loopback/private-interface reachability is verified on the actual deployment.
- Exported graphs, task payloads, diagnostics and durable records contain no
  upstream credentials. Native scoped bearer material stays private.

Current evidence: plan reviewed for checkpointed implementation against Laomedo
`7f37cfb63a2fed30330b941498c0b165771c4bb2`; runtime acceptance remains unverified.
Native LFX 1.12.3 tool objects, closure compatibility, single-call behavior and
app-loop lifetime must be verified before provider integration. Actual rendered
UI and the substantive implementation diff still require independent review.
