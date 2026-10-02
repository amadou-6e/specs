---
title: OpenCode local provider adapter
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# OpenCode local provider adapter

Scope: issue [Laomedo #27](https://github.com/amadou-6e/laomedo/issues/27).
This is a draft adapter contract, not a completed authenticated Docker pilot.
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
before reserving a submitted-turn ledger entry. A submitted turn is charged before
the message POST, including a timeout or unsuccessful request. Default cap is zero.
Private native response records remain outside Git. Unknown usage remains unknown.
Terminal assistant metadata and no outstanding native tool are required for success.
Observed native tool IDs/results are retained; a completed `skill` tool selecting an
offered skill establishes native load evidence, not subsequent compliance with it.

## Authentication and isolation gate

The installed CLI reports version 1.18.33 and no credentials in its default store.
No running OpenCode process was observed in the read-only metadata check. This does
not refute the user's authenticated Go setup; it leaves its runtime/profile unresolved.
No credential material was read or copied. Official Go documentation describes a
Go API key. Do not assume a ChatGPT token or OAuth refresh semantics.

The Codex Docker image's controller credential protection depends on its command
sandbox. It must not be assumed for OpenCode, whose native shell controller/tool
separation has not been verified. Mounting a Go credential into a same-UID native
OpenCode shell container is not an acceptable equivalent. No such mount is created.
The production transport fails closed with `opencode_isolated_transport_required`.
An explicitly injected transport enables protocol tests only, not proof of isolation.

Before enabling live deployment, locate the actual authenticated profile through
metadata-only inspection, define a pinned Docker/controller/tool boundary under the
existing grants, and verify credential denial through every enabled native tool.
Then authorize a separate aggregate turn/spend cap and run the actual imported flow.
Production auth lifecycle remains specs #129. No server/config/flow is installed or
restarted by this adapter slice.

## Continuation findings on 2026-10-02

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

At takeover verification, 48 host tests and 14 pinned Langflow checks passed
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
Real skill discovery, authentication reuse, Docker image pin, network behavior and
native cancellation termination are still acceptance gaps.

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
13/14 with one unused authorized turn. The local prototype meets the tested
#27 path; exhaustive disclosure-route and network claims remain outside this
evidence.

## Sources checked (reference owner)

- [OpenCode server API](https://opencode.ai/docs/server/): session/message/abort and provider inventory.
- [Native skills](https://opencode.ai/docs/skills/): project `.agents/skills` discovery and skill tool.
- [Go](https://opencode.ai/docs/go/): provider credential mode.
- [Configuration](https://opencode.ai/docs/config/): personal/project and inline configuration precedence.
- [Pinned account implementation](https://github.com/anomalyco/opencode/blob/v1.18.33/packages/opencode/src/account/account.ts): active account configuration route and Console token semantics.
- [Pinned config implementation](https://github.com/anomalyco/opencode/blob/v1.18.33/packages/opencode/src/config/config.ts): active organization config and Console-token substitution.

Sources inspected 2026-10-02. Local command evidence: `opencode.cmd --version`,
`opencode.cmd run --help`, `opencode.cmd auth list`, process executable metadata.
No model turn submitted. Go subscription availability and actual credential profile
are not inferred from public documentation.
