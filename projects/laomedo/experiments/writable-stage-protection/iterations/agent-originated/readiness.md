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

The model-backed probe must preserve the [reviewed E05 no-model boundary](../../protocol.md) and obtain review of the proposed personal-subscription exception before dispatch. The agent must run in a newly created, pinned Docker stage with a writable disposable checkout and effective skill mounted read-only. Protected canonical skill, runner store, host and synthetic personal-credential stand-ins remain outside every stage mount. The real subscription login requires its own reviewed boundary; do not copy the active IDE/CLI `auth.json` or silently reuse the `laomedo-122-docker-auth` volume.

## Credential and turn ledger

The selected billing mode is **ChatGPT subscription access**, not OpenAI Platform API-key usage. [Official Codex authentication guidance](https://learn.chatgpt.com/docs/auth#sign-in-with-chatgpt) distinguishes these modes: `codex login` opens browser sign-in for ChatGPT access; on a headless runner, [device-code sign-in](https://learn.chatgpt.com/docs/auth#login-on-headless-devices) is the preferred alternative when enabled. Codex caches that login and refreshes it during use, so a persistent, access-restricted runner profile can survive individual disposable stages without repeated sign-in. Do not use `codex login --with-api-key` or silently fall back to Platform billing.

The user selected their **existing ChatGPT subscription account** for this local test. The [proposed protocol exception](../../protocol.md#proposed-subscription-backed-step-5-exception-pending-review) replaces the prior nonpersonal-login condition only for step 5, pending review. Sign in once to a separate persistent, access-restricted runner profile outside Git; do not copy the live personal `auth.json` as a workaround. Keep the login cache outside the disposable checkout. The current local runner mounts an auth volume inside the CLI container, so Docker absence is not a valid claim for that real login: verify a native denial for agent-issued credential reads and review every available tool path. Record only the account/profile reference, login mode and status, never access or refresh tokens. If the reviewer rejects a personal profile in the stage, a trusted-controller/command-stage split is required before dispatch.

Create a persistent private turn ledger outside Git. Its cap is **four submitted turns total**, including timeouts and ambiguous responses. Atomically reserve one slot immediately before each `turn/start`; never refund a submitted or timed-out slot. Record attempt number, model, effort, container/image IDs, grant ID, start/stop times, native thread and turn IDs when returned, and a sanitized outcome. Do not write credential bytes or raw private events to the ledger. The current count is **0/4**. A model or effort must be chosen from the runtime's supported list and recorded before dispatch. No model or spend claim is made yet.

## Separate model egress grant

The successful no-model stage used a dedicated `--internal` network. Codex cannot make a model request from that topology without a new, separately reviewed route. Do not attach the stage directly to `bridge` or weaken its HostConfig to make a turn work. First identify the actual destinations used by the pinned Codex CLI **under ChatGPT sign-in**, without publishing tokens or widening the live stage. Then propose and review a pinned, inspect-verified route restricted to those destinations. It must not relay stage-controlled destinations to host-loopback listeners or Docker Engine, publish ports, mount host paths, or carry a personal credential. Record effective networks, request allowlist, route probes and observed egress before using it. A failed model connection is inconclusive; do not broaden the allowlist during a live turn without review. The earlier `api.openai.com:443` proxy draft targeted the API-key route and was removed from the implementation PR before any stage start or model turn; it is not evidence that subscription-backed Codex can use that route.

The model-backed stage needs a reviewed writable disposable home for runtime state and a separate persistent, access-restricted profile for subscription login. The current CLI-in-container design would mount that profile into a trusted CLI path and rely on the Codex command sandbox to deny agent reads, so it is weaker than the no-model stage's Docker-absence guarantee for the real login. The exact boundary is unproved; do not mount a credential file into the checkout or any path the agent can read. A bounded lease and cleanup rule must remain effective if the controller or test process dies. These additions change the no-model stage's exact HostConfig and Config request, so capture a new correct-create fixture and prove the expanded request still rejects protection downgrades before dispatch. Keep the no-model result intact as a separate observation.

### Current-runner gap against E05

The [current local runner at `571dac8`](https://github.com/amadou-6e/laomedo/blob/571dac8/laomedo/local_runner.py) is a useful starting point for a subscription-backed Codex turn, but it is **not** the E05 stage manifest:

| Current behavior | E05 step-5 pre-dispatch work |
| --- | --- |
| A persistent `laomedo-122-docker-auth` volume is mounted read/write at `/home/runner/.codex` in the CLI container. | Select a separate private profile or explicitly review reuse; inspect the actual mount and prove agent-issued reads are denied through every available tool path. |
| The container joins Docker `bridge`; its root filesystem is not requested read-only. | Build and inspect a new exact request with an internal stage network, reviewed model egress and read-only root, without silently weakening other flags. |
| The runner binds a canonical directory read-only and a store directory writable. | Keep the protected E05 canaries outside the stage and mount only the disposable checkout, effective skill, approved runtime state and reviewed login path. |
| [Preflight](https://github.com/amadou-6e/laomedo/blob/571dac8/laomedo/local_runner.py) checks `command/exec` refusal for one auth-file path, and the [policy](https://github.com/amadou-6e/laomedo/blob/571dac8/laomedo/runner-config.toml) denies that path. | Recheck the denial with the exact E05 image/config and a native agent-issued command event; one direct preflight cannot prove every possible access route. |
| The runner has a persistent turn ledger. | Use a private E05 ledger capped at 4, count every submitted or timed-out turn, and retain the 60-second orphan bound. |

No model turn or credential read was performed for this gap analysis.

## Agent-originated evidence

The prompt must direct the agent to attempt the same scoped positive controls and forbidden accesses as the direct probe, with no retry, escalation, configuration change or alternate route. Preserve native `commandExecution` start/completion events, command target, exit status and a redacted error class. A final message saying an attempt occurred is not evidence. Require a real denied tool result for the mounted effective-skill write, path absence plus a complete bounded marker sweep for unmounted assets, unchanged before/after host hashes, runner sidecar 401, scoped grant acceptance and post-revocation refusal, host-side symlink rejection, and complete stage cleanup. If the native event or its exit result is absent, record **inconclusive**, not denial.

**Current gate:** the four-turn ceiling and use of the user's existing ChatGPT subscription are authorized, but the proposed personal-login exception, profile mount, command boundary and subscription-backed model route are not reviewed. Therefore no `turn/start` may be submitted and E05 remains incomplete. The next concrete review artifact is a no-model credential-boundary preflight, credential-free route inventory and model-stage create/inspect downgrade check. No token value belongs in either repository.
