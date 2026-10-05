---
title: E05 agent-originated probe readiness gates
status: draft
kind: experiment-readiness
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Readiness gates

The model-backed probe must preserve the [reviewed E05 boundary](../../protocol.md). The agent must run in a newly created, pinned Docker stage with a writable disposable checkout and effective skill mounted read-only. Protected canonical skill, runner store, host and personal-credential stand-ins remain outside every stage mount. Do not reuse the personal ChatGPT login, `laomedo-122-docker-auth` volume, or a copied personal `auth.json`.

## Credential and turn ledger

The selected billing mode is **ChatGPT subscription access**, not OpenAI Platform API-key usage. [Official Codex authentication guidance](https://learn.chatgpt.com/docs/auth#sign-in-with-chatgpt) distinguishes these modes: `codex login` opens browser sign-in for ChatGPT access; on a headless runner, [device-code sign-in](https://learn.chatgpt.com/docs/auth#login-on-headless-devices) is the preferred alternative when enabled. Codex caches that login and refreshes it during use, so a persistent, access-restricted runner profile can survive individual disposable stages without repeated sign-in. Do not use `codex login --with-api-key` or silently fall back to Platform billing.

The reviewed [E05 protocol](../../protocol.md) still requires a **nonpersonal** test login and prohibits mounting a personal profile into the stage. No such ChatGPT subscription login is available yet. A dedicated account or managed-workspace identity would need to be authorized and signed in once to a private persistent profile outside Git; the test must verify the resulting plan access without exposing token bytes. If the intended test is instead to use the user's existing personal ChatGPT subscription, revise and re-review the protocol's nonpersonal condition before dispatch. Do not copy the live personal `auth.json` as a workaround. Keep the login cache outside the disposable checkout and verify that agent-issued commands cannot read it. Record only the account/profile reference, login mode and status, never access or refresh tokens.

Create a persistent private turn ledger outside Git. Its cap is **four submitted turns total**, including timeouts and ambiguous responses. Atomically reserve one slot immediately before each `turn/start`; never refund a submitted or timed-out slot. Record attempt number, model, effort, container/image IDs, grant ID, start/stop times, native thread and turn IDs when returned, and a sanitized outcome. Do not write credential bytes or raw private events to the ledger. The current count is **0/4**. A model or effort must be chosen from the runtime's supported list and recorded before dispatch. No model or spend claim is made yet.

## Separate model egress grant

The successful no-model stage used a dedicated `--internal` network. Codex cannot make a model request from that topology without a new, separately reviewed route. Do not attach the stage directly to `bridge` or weaken its HostConfig to make a turn work. First identify the actual destinations used by the pinned Codex CLI **under ChatGPT sign-in**, without publishing tokens or widening the live stage. Then propose and review a pinned, inspect-verified route restricted to those destinations. It must not relay stage-controlled destinations to host-loopback listeners or Docker Engine, publish ports, mount host paths, or carry a personal credential. Record effective networks, request allowlist, route probes and observed egress before using it. A failed model connection is inconclusive; do not broaden the allowlist during a live turn without review. The earlier `api.openai.com:443` proxy draft targeted the API-key route and was removed from the implementation PR before any stage start or model turn; it is not evidence that subscription-backed Codex can use that route.

The model-backed stage needs a reviewed writable disposable home for runtime state, while the refreshable subscription login remains in a separate persistent, access-restricted controller profile. The exact controller-to-stage authentication boundary is unproved; do not mount a credential file into a workspace the agent can read. A bounded lease and cleanup rule must remain effective if the controller or test process dies. These additions change the no-model stage's exact HostConfig and Config request, so capture a new correct-create fixture and prove the expanded request still rejects protection downgrades before dispatch. Keep the no-model result intact as a separate observation.

## Agent-originated evidence

The prompt must direct the agent to attempt the same scoped positive controls and forbidden accesses as the direct probe, with no retry, escalation, configuration change or alternate route. Preserve native `commandExecution` start/completion events, command target, exit status and a redacted error class. A final message saying an attempt occurred is not evidence. Require a real denied tool result for the mounted effective-skill write, path absence plus a complete bounded marker sweep for unmounted assets, unchanged before/after host hashes, runner sidecar 401, scoped grant acceptance and post-revocation refusal, host-side symlink rejection, and complete stage cleanup. If the native event or its exit result is absent, record **inconclusive**, not denial.

**Current gate:** the four-turn ceiling is authorized, but there is no nonpersonal ChatGPT subscription login or reviewed subscription-backed model route. Therefore no `turn/start` may be submitted and E05 remains incomplete. The next concrete review artifact must settle which ChatGPT account/profile is authorized under the protocol, then capture a credential-free route inventory and a model-stage create/inspect preflight. No token value belongs in either repository.
