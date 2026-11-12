---
title: Shared local agent protocol
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-29
applies_to: [laomedo]
supersedes: null
related: [codex.md, claude.md, opencode.md, isolation.md, output-contract.md]
---

# Shared local agent protocol

Codex, Claude and OpenCode use one host communication path: ACP v1 over the
owned Docker session's standard input/output. The host uses the published
Python ACP SDK for framing, request dispatch and session operations. Provider
CLIs and launch policy can differ. Laomedo must not maintain parallel native
Codex request queues, Claude stream-JSON readers or OpenCode HTTP/SSE execution
clients beside that path. This changes the agent wire, not the authenticated
[runner HTTP API](runner-api.md) used by the graph.

Implementation is on draft [Laomedo PR #250](https://github.com/amadou-6e/laomedo/pull/250).
Runner checks below are bounded evidence, not graph acceptance or merge approval.

## Protocol and policy requirements

| ID | Requirement |
| --- | --- |
| ACP-01 | Use standard initialize, session/new, session/load, session/set_config_option, session/prompt and session/cancel operations. Resume must load the saved native identity; failure must never create a new session or repeat the task automatically. |
| ACP-02 | Discover model and effort choices from the installed runtime. Validate the requested pair before a prompt and confirm the agent's observed configuration. A display label or requested value alone does not prove the effective selection. |
| ACP-03 | Advertise no host filesystem or terminal capabilities. Deny permission requests. The only optional host request extension is pure output-precheck validation; it must not execute commands or mutate files. |
| ACP-04 | Keep launch policy, credential selection, immutable skill materialization, run authorization and output correction in their existing owners. General container ownership, stream limits and container termination belong to py-docker; ACP session cancellation belongs to Laomedo's shared client. ACP does not authorize tool execution. |
| ACP-05 | Keep native session/message/tool/turn identities when actually reported. Label host attempt identities as host identities. A normalized ACP title is display text, not a native tool name or proof that a selected skill executed. |
| ACP-06 | Bound startup, prompts, cancellation grace, captured bytes and metadata export. No verification-only turn limit belongs in ordinary runners or managed services. |
| ACP-07 | Validate incoming notifications before SDK parsing can log private payload fragments. Malformed frames, capture failures and mismatched sessions must invalidate success. Do not globally suppress logging or silently discard a failed capture while reporting completion. |
| ACP-08 | Remove exact launch capabilities and known credential fields before any raw or normalized evidence write. Adapter diagnostics, account/auth/config events and request-response credentials must not enter user-visible errors or activity. |

### Native record extensions

Codex uses the pinned codex-acp adapter with a small maintained extension. Its
initialize reply must advertise `_meta.laomedo` exactly as
`{"version":1,"rawEvents":true,"hostPolicy":true}`. The host must reject an
absent or incompatible capability with descriptive `initialize_rejected` before
creating a session. Matching an upstream adapter version is insufficient.

The extension forwards allowlisted original native notifications on
`_laomedo/codexEvent` and drains those notifications before a prompt response.
Native capture failure terminates native execution. No account, authentication,
configuration or arbitrary native request tunnel is exposed.
The raw archive contains these allowlisted notifications, not every stdout byte;
ACP responses and adapter stderr are excluded. Stderr is drained within stream
limits and discarded, so the retired private stderr log is intentionally absent.
Named extensions provide bounded model metadata, fixed-enum preflight, one pre-prompt executor
registration/status and the pure output precheck. Typed skill items and normal
or split policy come only from validated host metadata, never prompt parsing.
Normal mode inherits the reviewed permission profile with approval set to never;
ACP agent modes must not override it or enable agent self-approval.
The model-writable project root must be explicitly untrusted in native session
configuration. A project `.codex/config.toml`, including a model-written file,
must not become a source of runner permissions, approval, hooks or provider
routing on Fresh, correction or Resume. Native sandbox protection of that path
is an additional boundary, not a substitute for keeping native project trust off.
When only the adapter's ACP configuration supplies model/effort fields, label
their provenance `host_requested_adapter_asserted`. This checks configuration
consistency; it is not an independent native report of effective selection.
Do not describe an adapter echo as native confirmation.

Claude uses claude-agent-acp with original SDK message receipts enabled. A native
terminal receipt, matching session and positive descendant cleanup remain
required. Its canonical ACP options also define the saved-run policy fingerprint;
a retired CLI command must not be retained solely for that fingerprint.

OpenCode uses its native `opencode acp` command. Where ACP omits complete native
usage or child history, the host may make a bounded, consistent read-only backup
of the dedicated runner's native database and run the native CLI export against
a private disposable copy. First take the bounded consistent snapshot in host
memory and verify that pinned account, account-state, control-account and
credential tables contain no rows. Unknown credential schemas or populated
secret-bearing tables refuse export. Rebuild the checked snapshot with SQLite
VACUUM INTO before writing the disk copy, purging deleted-page contents. Native
session token counters are usage metadata, not authentication tokens. The job
receives no authentication files, has no network and mounts no writable live
profile. Credential-store checks and their limits are described below.
Retain original exports, session/parent
bindings, per-attempt message baselines and receipt times. Discover only child
identities actually linked by a native task result and independently verify each
child's parent. An unknown old-child baseline, incomplete tool, interrupted export
batch or uncertain export-container cleanup must never become known zero usage
or complete inclusive totals. Do not add ACP counters to native export counters.
Child metadata available only after export must not be described as live streaming.
The credential check covers known pinned credential stores and a field-name
heuristic, including key, API-key, bearer and cookie names. It is not a proof that
arbitrary JSON/blob task content contains no secrets. Native task history stays
private to its local owner and is not approved for remote export. Do not copy
a personal OpenCode database or describe the guard as a generic secret scanner.

The default database capture ceiling is 128 MiB. The local user may set
`LAOMEDO_OPENCODE_HISTORY_MAX_DATABASE_BYTES` in host runner startup configuration,
up to 512 MiB. If that ceiling is exceeded, preserve existing history, report
incomplete capture and do not replay the task. Larger stores require preserving
an archive and configuring a separate dedicated store for new work; do not delete
active history or imply an archive control exists in the graph UI. Guard refusal
and budget refusal do not imply unconfirmed container cleanup.

The in-memory backup and compaction can peak at roughly twice the configured
database ceiling, plus interpreter overhead; 512 MiB can therefore require about
1 GiB of host memory. This setting bounds input size, not total process memory.

## Failure, cancellation and saved runs

The shared prompt loop monitors host authorization and executor health. An active
authorization failure requests cancellation and preserves its stable auth code.
An independently lost executor retains `executor_lost` and an uncertain work
outcome. ACP cancellation acknowledgement alone is insufficient: Codex needs the
matching raw native interrupted completion, and all providers need confirmed
descendant cleanup. A cleanup failure takes precedence over a successful answer.
Freeze post-run files only after confirmed descendant cleanup, and recheck pinned
skills and protected mounts at that boundary. Directory creation during native
shutdown must not invalidate a snapshot made earlier. Include empty directories
in the frozen tree and verify that actual Fresh-to-Resume remains possible.

Maintain exact precheck call bindings and verified call IDs. Automatic output
correction continues the same session and must not repeat the original task.
Mediated effects, observed tool effects, outstanding commands or uncertain tool
identities block automatic correction as required by [Output Contract](output-contract.md).

Old saved runs retain their original image, CLI, policy and execution-mode
bindings. A pre-ACP run may be rejected with existing `resume_binding_mismatch`
when those bindings change. Keep its history readable; never silently rewrite
the binding or fall back to Fresh. Native history compatibility alone does not
establish migration of an old Laomedo run. Automatic binding migration is outside
this increment.

Public errors use the [shared error presenter](node-errors.md). Include
`turn_timeout`, `cancel_native_unconfirmed`, supported ACP request-timeout codes,
`executor_lost`, `auth_revoked_during_turn` and `permission_preflight_failed` in
producer coverage. Explain uncertainty and actual recovery without blind retry
advice, nonexistent controls or a separate operator on a user's local machine.

## Acceptance and current evidence

Verify the final revision through the actual Agent graph, including Fresh,
same-session Resume, native skill use, cancellation during a real tool, failures
and recovery. Browser acceptance and owner inspection remain mandatory. Unit
fixtures and direct runner checks are supporting evidence only.

At the Codex cutover checkpoint `9bddf7e`, real production-runner checks observed
Fresh and Resume on one native thread, accepted output prechecks, original native
records, local OTLP receipt and confirmed cleanup. Real Claude and OpenCode
checks also observed Fresh/Resume and cancellation; a subsequent real check
loaded the shipped pinned skill-summary through each native skill tool. These
observations do not establish all provider or graph stories at the final head.

Remaining acceptance includes final installed-artifact/graph checks, stock-adapter
refusal, split production paths, app-owned OAuth/custom provider and mediated
GitHub validation, unselected-skill isolation and child activity. Native child
agent validation requires the requested user authorization; do not substitute
synthetic child evidence. Final full-diff reviewer approval and user graph
validation have not been obtained. No release or merge readiness is claimed.

Claude initialization was observed to advertise bundled skills that were not
selected. The current tool allowlist denies their invocation, but discovery
isolation has not been achieved and must not be presented as an accepted capability.

Sources: [ACP stdio transport](https://agentclientprotocol.com/protocol/v1/transports),
[Python SDK](https://github.com/agentclientprotocol/python-sdk),
[Codex adapter](https://github.com/agentclientprotocol/codex-acp),
[Claude adapter](https://github.com/agentclientprotocol/claude-agent-acp),
[OpenCode ACP](https://opencode.ai/docs/acp/) and
[native CLI](https://opencode.ai/docs/cli/).

## Provider extension contracts (#275)

The [direct provider boundaries](../design/provider-roles.md) own the selected
method, value and lifecycle definitions. The earlier runtime and projector ABC
proposal is withdrawn. Native runtimes and interpretation helpers remain
provider-internal; shared Docker mechanics are concrete infrastructure.

ACP is communication, not an Agent process, command executor, credential source,
model catalogue or Activity interpreter. Provider implementations compose the
shared `AcpSession`; no redundant protocol ABC is required.

| Shared consumer boundary | Selected contract |
| --- | --- |
| Agent interaction, Activity and readiness | The existing `BaseAgent` run operations, `read_activity` and `readiness`. Native cancellation acknowledgement and confirmed cleanup remain distinct. |
| Model discovery | `BaseModelCatalog.list_models(refresh=False)`, `snapshot` and `wait_until_idle`. Discovery never prompts a model or substitutes a selection. |
| Native command integration | `BaseCommandExecutor.execute` and `shutdown`. HTTP/MCP handlers adapt this contract; command exit status does not establish resource cleanup. |
| Native credential admission | `BaseCredentialProvider.prepare`, `validate`, `borrow` and `release`. Public identity metadata contains no secret material. |
| Built-in provider registration | `AgentProviderRegistry` and `AgentProviderDescriptor`: trusted identities and actual capabilities. Graph input cannot choose imports, executables, credentials or unregistered providers. |

`BaseCredentialProvider.borrow()` returns host-only `CredentialMaterial`.
Inline-token providers project their selected host token; volume/profile
providers keep secrets with their native owner and return a prepared public
binding. Secret fields are excluded from representations and serialization.
Borrowing transfers neither refresh nor revocation authority; releasing a
borrowed profile never revokes host login. Requested validity/deadline
constraints that cannot be enforced are refused before refresh.

`snapshot()` returns a detached last observation, possibly stale, without
refreshing or selecting a model. `wait_until_idle(timeout=...)` observes discovery
and cleanup completion, not success or execution admission. Native cache TTLs
and refresh ownership remain provider-owned. Readiness, process health and
isolation are separate observations; unsupported checks never report success.

`BaseInterruptibleCommandExecutor` adds `request_cancel` for Claude/OpenCode
transient workers: stop admission, signal owned work and retain unknown native
acknowledgement until observed. `shutdown` separately confirms cleanup.
`BaseSplitCommandExecutor` adds native persistent-executor health and
controller/executor isolation checks. Providers without that topology do not
emulate it. Declared capabilities remain subject to interface/signature checks.

Provider-native pricing stays internal. Claude/OpenCode without verified native
prices retain unknown costs; Codex rates are never a fallback for another
provider. Maintain public payloads, persisted schemas, session IDs, stable
errors, authorization and fail-closed cleanup. Renaming internal objects does
not rename wire values or add personal saved-source migration support.

Acceptance separately covers Fresh, Resume, status, cancellation, model refresh,
Activity and failure/recovery for each provider. Structural and fixture checks
support but do not establish real-provider acceptance. No new model-backed probe
is authorized; the owner's final real-workflow validation remains a merge gate.
