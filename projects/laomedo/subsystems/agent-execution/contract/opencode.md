---
title: OpenCode local provider adapter
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-25
applies_to: [laomedo]
supersedes: null
related: []
---

# OpenCode local provider adapter

Scope: issue [Laomedo #27](https://github.com/amadou-6e/laomedo/issues/27).
This is a draft local adapter contract. The bounded authenticated Docker pilot is
recorded in the [latest results](../../../experiments/opencode-agent/iterations/2026-10-02/results.md).
Reuse the [node lifecycle](langflow-node.md), [isolation owner](isolation.md),
and immutable [skill references](../../skill-registry/contract/langflow-node.md).

## Provider and ports

The OpenCode Agent has Task, Provider/Model, Variant, Skill References (1..16),
Operation, Prior Run and local Runner URL ports. Answer is Message; Run Reference
is JSON in pinned Langflow 1.12.3. Output methods share one dispatch per build.
The shared component category must be installed together and on the Python module
search path because the OpenCode client reuses the Codex client class.

Model is an explicit provider/model identifier advertised by the private OpenCode
server. Only `default` effort is supported in this slice; any other setting fails
before dispatch. Default means no explicit native variant, not verified low effort.
Fresh creates a private snapshot/session. Resume requires completed status, exact
native session ID, unchanged snapshot, same provider/runtime/model/effort and pinned
skills. Provider is `opencode`; never accept a Codex run reference as OpenCode.

The adapter checks server health version `1.18.33` and connected-model inventory
before recording a submitted attempt. Ordinary runners have no verification-only
turn ceiling. Their diagnostic sequence is separate from historical experiment
ledgers, which remain unchanged. Explicit verification bounds belong to an isolated
harness, never normal startup or persistent services. An attempt is recorded before
the message POST, including a timeout or unsuccessful request.
Private native response records remain outside Git. Unknown usage remains unknown.
Terminal assistant metadata and no outstanding native tool are required for success.
Observed native tool IDs/results are retained; a completed `skill` tool selecting an
offered skill establishes native load evidence, not subsequent compliance with it.

## Authentication and isolation gate

The active Console login is selected from the user's OpenCode database using a
read-only connection. The local handoff stores only the selected Go credential and
routing context in access-restricted runner state outside Git. The Console access
token is copied only when the official provider configuration requires its exact
substitution; no refresh token or complete personal database is copied. The
private validity record binds the selected key by digest and records its expiry.
The runner rejects an expired or near-expiry Console token before reserving a turn.
Refresh remains the official client's responsibility.

The pinned OpenCode controller and disposable command workers are separate Docker
containers. The controller receives the selected `auth.json` as a read-only file
mount; the worker receives neither the credential nor the controller profile or
Docker socket. The controller's session directory can contain an empty Docker
mount placeholder but no second plaintext auth copy. The broker admits one
command at a time. It still binds to `0.0.0.0` for Docker Desktop bridge routing,
protected by a random per-run bearer capability. Disposable command workers use
Docker `--network none`, so they have no configured network path to the host
runner API. The controller retains bridge networking for its model API and
command broker. The runner API independently requires a persisted private bearer
capability on every endpoint, including status and cancel. The Langflow OpenCode
component reads the capability from a mounted read-only file, never from flow
JSON. Broker LAN exposure and all credential access routes have not been
exhaustively audited.

The runner without isolated transport fails closed with
`opencode_isolated_transport_required`; an injected transport preflight reports
`transport_configured`, not proof of isolation. Fresh and resume both verify that
the workspace skill directories exactly match recorded pinned revisions before
building the controller view. A changed or extra skill fails the turn. A cancel
requested before message dispatch is checked before reserving and again before
sending the message. Native abort remains the mechanism after dispatch; a
concurrent request can still race a final pre-dispatch check, so perfectly atomic
cancel/submit exclusion is not claimed.

The saved Langflow flow points at the local runner on port 8768. This is a bounded
single-user local prototype only. Production auth lifecycle remains specs #129;
hosted or multi-user use requires a broader network and credential-boundary audit.

## Historical continuation findings on 2026-10-02

The terminal login was found in the active Console account stored in SQLite,
separate from legacy `auth.json`. Two previous message submissions failed with
HTTP 401 before tool results because the handoff incorrectly treated redacted
`debug config` output as a credential. Those attempts remain in the 2/2 ledger.

The corrected resolver reads only active account access-token/expiry/server and
organization fields using a read-only database connection. Request account config
at its official `https://opencode.ai` origin, preserve the `/console` prefix, use
JSON request headers, and reject redirects. Accept only a concrete Go credential
or the exact Console-token environment substitution; reject redacted values,
canaries, arbitrary templates, expired tokens and organization mismatches.
Copy only the selected credential and routing context into private runner state.
Never copy refresh tokens or the complete personal database. Refresh remains the
official client's responsibility. The corrected handoff succeeded with no model turn.

The explicit controller/tool transport uses a pinned OpenCode controller image and
separate disposable Docker command workers with the existing grants. Disable
controller tools except allowlisted native skills and the per-run authenticated
MCP broker. Workers receive no controller profile/environment/auth mount or Docker
socket. Direct command probes showed workspace writes succeed, canonical/store
writes fail and controller-auth paths cannot be read. A worker's own `/proc`
environment was readable; the credential canary was absent. This is separation
evidence, not a claim that `/proc` is globally unreadable or that agent-originated
denial, network isolation or child termination has been established.

At that earlier takeover verification, 48 host tests and 14 pinned Langflow checks passed
(three OpenCode, eleven Codex). Live fresh/resume, actual skill calls and native
cancellation remain pending a new turn allocation. Original isolation findings
above describe the earlier draft, not a completed authenticated pilot.

## Additional live attempts and routing correction

Four further authorized turns were submitted through imported Langflow: attempts
3, 4 and 5 returned HTTP 401; attempt 6 returned HTTP 400, "Model does not support
this protocol." No native tool results or completed snapshots were observed, so
resume was not submitted. The cumulative OpenCode ledger is 6/6, failures retained.
This is failed acceptance, not a completed authenticated pilot.

Catalog models retained `/zen/go/v1` despite the provider endpoint override.
Carry explicit official model definitions and allowlisted SDKs so the Console
inference route and each model's protocol override catalog defaults. Luna needs
`@ai-sdk/openai`, not the provider-level OpenAI-compatible protocol. Final runtime
preflight confirmed `/inference/go/openai/v1` and `@ai-sdk/openai`; no remaining
model allocation exists to verify that final correction. Sanitized evidence is in
the implementation's `examples/opencode-agent/live-evidence.json`. Port 8768 avoids
the handoff runner. Host tests remain 48 passed; live acceptance gaps remain.

## Cancellation and evidence limits (target retained)

Status is durable and reports restarted running records as interrupted. Cancel uses
the active session's native abort endpoint. A true response records acknowledgement;
child-command termination remains unverified. The adapter retains partial raw records.
Neither provider session creation nor an abort acknowledgement proves OS containment.
Credential-free synthetic tests cover snapshot/session resume, fresh independence,
native skill/tool normalization, unknown usage and fail-closed effort/transport paths.
At that stage, real skill discovery, authentication reuse, Docker image pin, network
behavior and native cancellation termination were acceptance gaps. See the latest
results for the tested local routes and the remaining limits.

## Latest bounded observations

[2026-10-02 results](../../../experiments/opencode-agent/iterations/2026-10-02/results.md)
supersede the earlier failed-acceptance status above. Four further authorized turns
produced successful direct CLI, real imported-flow native multi-skill fresh and
same-session restart/resume, and native abort with observed worker termination.
The cancellation-status race was fixed and covered by a deterministic synthetic
test. A later authorized live runner API retest returned `cancelled`, with native
abort acknowledged, the owned worker absent and no delayed write. The cumulative
ledger is 11/14 with three turns unused. The existing saved Langflow flow's
Runner URL was updated to port 8768 under explicit user approval and verified
by readback. Successful model-backed flow calls before that edit used a per-run
override to 8768. This remains a draft local prototype contract, not a hosted
guarantee.

Saved-flow attempts 12 and 13 then used that stored URL without request tweaks.
Attempt 13 completed with both native skill loads, a successful worker command,
queryable status and independent marker readback. The tested worker private
paths were absent, the controller skill view contained only the two pins, and
the selected provider key was absent from saved/exported flow data, tracked
repository files and inspected run results. Attempt 12's fixture typo and the
attempt 13 checker correction are retained in the linked results. Ledger is
13/14 with one unused authorized turn at that point. The later review fixes and
attempt 14 are recorded in the [results](../../../experiments/opencode-agent/iterations/2026-10-02/results.md).
The final ledger is 14/14. The local prototype meets the tested #27 path;
exhaustive disclosure-route and network claims remain outside this evidence.

Subsequent review fixes added runner API authentication and disabled networking
for disposable command workers. Synthetic host tests passed against the revised
stack without another model turn. A no-model container canary showed no host
route under Docker `--network none`, and three pinned Langflow component tests
passed. The prior saved-flow run and private-path checks do not verify this
exact new deployment; fresh saved-flow deployment validation remains outstanding. The earlier observed
controller skill view contained only the two pins for the tested fresh run; resume
pin enforcement is established by synthetic tests, not a live mutation attempt.

## Sources checked (reference owner)

- [OpenCode server API](https://opencode.ai/docs/server/): session/message/abort and provider inventory.
- [Native skills](https://opencode.ai/docs/skills/): project `.agents/skills` discovery and skill tool.
- [Go](https://opencode.ai/docs/go/): provider credential mode.
- [Configuration](https://opencode.ai/docs/config/): personal/project and inline configuration precedence.
- [Pinned account implementation](https://github.com/anomalyco/opencode/blob/v1.18.33/packages/opencode/src/account/account.ts): active account configuration route and Console token semantics.
- [Pinned config implementation](https://github.com/anomalyco/opencode/blob/v1.18.33/packages/opencode/src/config/config.ts): active organization config and Console-token substitution.

Sources inspected 2026-10-02. Local command evidence: `opencode.cmd --version`,
`opencode.cmd run --help`, `opencode.cmd auth list`, process executable metadata.
At the initial source check, no model turn had been submitted. Later private
authenticated runs are documented in the linked experiment; subscription
availability and credential profile are not inferred from public documentation.


## Graph activity and usage

The OpenCode node uses the shared graph Agent Activity view, reached through the
node's Activity action with that node already selected. Viewing or exporting
activity does not execute an agent. The graph execution selector contains runs of
the current graph only.

Each Gantt row represents an observed agent conversation, with native parent
identity determining nesting. Captured turns are separate selectable segments
on that row. Idle, startup and cleanup gaps have no green envelope bar. The full
invocation receipt range remains the time axis. Native titles are labels, not
proof that an agent initiated a child. A host-created child and an agent-delegated
child must remain distinguishable in verification evidence.

All activity, conversation and turn selections scope messages, tool records,
OpenTelemetry records, token totals and cost estimates consistently. Unattributed
records remain available in All activity. Missing attribution, truncated detail,
or unverified invocation boundaries must not become known zero usage through
narrower selection. While a selected run or turn is running and has no usage
observations or capture warning, its total cards display zero, including a
provisional zero estimate. Reported values replace those initial values; missing
or unpriced observations remain Unknown. Completed missing usage remains Unknown.

Input includes native cache categories; output includes reasoning. Inclusive
aggregation must not charge repeated native updates or snapshot reconciliation
twice. USD values are API-equivalent estimates using recorded model catalog rates,
not subscription charges or invoices. Unpriced models remain unknown. Token and
cost charts appear side by side when space permits.

Native SSE receipts and reconciled message snapshots retain their provenance.
Adapter-generated OpenTelemetry spans are explicitly adapter-observed, not
claimed native SDK instrumentation. Partial stream evidence does not determine
task success. Capture notes use the shared [descriptive error presenter](node-errors.md),
with safe codes and identifiers available separately from the explanation.

Conversation appears last in an open section, has a bounded scrollable body,
right-aligned user messages, left-aligned agent replies and compact tool rows.
Tool outputs and native metadata start collapsed; message-source icons expose
source metadata without an extra disclosure row. Fuzzy search preserves transcript
order. Conversation exports support Markdown or JSON; OpenTelemetry exports JSON
records. Exports include the selected scope, filter and capture limits. Exported
records are not an OTLP ingestion envelope.

## Trusted host agent configuration

The isolated boundary preserves its normal skill and command-worker tools and
primary instructions. A trusted host may extend the native agent configuration
before the read-only configuration mount is created. Graph/request inputs cannot
supply this callback or replace the host policy. A read-only named subagent in a
local verification profile is not evidence that unrestricted native tools or
delegation are enabled by default. Provider identity, runtime pins, credentials
and worker isolation remain governed by the existing isolation contract.

## Verification boundaries for this continuation

Real Docker-backed fresh and resume runs, message/tool capture, per-session token
usage, API-equivalent estimates, adapter OpenTelemetry records and a native
parent/child Task delegation have been observed in bounded local verification.
The final preservation of default skill/worker policy has startup and internal
test evidence, not a new paid run of those restored tool paths. Initial zero-card
rendering and live cancellation on the final revision require separate live
acceptance; internal tests and old screenshots do not establish it. Retain these
limits in the implementation PR rather than treating document validation as
runtime proof.
