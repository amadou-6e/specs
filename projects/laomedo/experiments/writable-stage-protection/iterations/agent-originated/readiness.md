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

Use a **nonpersonal** project or service credential from a private secret store. Record only its store/reference, account/project identity and authorization mode in reviewable evidence. Do not commit the value, pass it in Docker create arguments, echo it, or retain it in raw traces. The proposed first mode is a dedicated OpenAI Platform project API key. [Official Codex authentication guidance](https://learn.chatgpt.com/docs/auth#sign-in-with-an-api-key) supports piping an API key over stdin to `codex login --with-api-key`; API-key usage is billed through the Platform account. Place cached credentials only in a disposable, private writable `/home/runner` tmpfs or equivalent isolated profile, and verify the agent's command sandbox denies reads of its credential path before the model turn. A managed nonpersonal Codex access token may be assessed separately if one becomes available; do not silently substitute the user's personal login.

Create a persistent private turn ledger outside Git. Its cap is **four submitted turns total**, including timeouts and ambiguous responses. Atomically reserve one slot immediately before each `turn/start`; never refund a submitted or timed-out slot. Record attempt number, model, effort, container/image IDs, grant ID, start/stop times, native thread and turn IDs when returned, and a sanitized outcome. Do not write credential bytes or raw private events to the ledger. The current count is **0/4**. A model or effort must be chosen from the runtime's supported list and recorded before dispatch. No model or spend claim is made yet.

## Separate model egress grant

The successful no-model stage used a dedicated `--internal` network. Codex cannot make a model request from that topology without a new, separately reviewed route. Do not attach the stage directly to `bridge` or weaken its HostConfig to make a turn work. Propose and review a second, pinned, inspect-verified egress sidecar that permits only the network destination(s) required by the selected nonpersonal auth mode. It must not relay stage-controlled destinations to host-loopback listeners or Docker Engine, publish ports, mount host paths, or carry a personal credential. Record effective networks, request allowlist, route probes and observed egress before using it. A failed model connection is inconclusive; do not broaden the allowlist during a live turn without review. The current [draft proxy and create-only preflight](https://github.com/amadou-6e/laomedo/pull/58) pin CONNECT to `api.openai.com:443` and inspected the proposed sidecar with no start or model request. Because this is a TLS tunnel, it does not restrict API paths within that host. Its actual compatibility with the Codex CLI, route denial tests and lifecycle behavior remain unverified and require review before any model turn.

The model-backed stage needs a reviewed writable home tmpfs for the isolated Codex profile, plus a bounded lease and cleanup rule that remains effective if the controller or test process dies. These additions change the no-model stage's exact HostConfig and Config request, so capture a new correct-create fixture and prove the expanded request still rejects protection downgrades before dispatch. Keep the no-model result intact as a separate observation.

## Agent-originated evidence

The prompt must direct the agent to attempt the same scoped positive controls and forbidden accesses as the direct probe, with no retry, escalation, configuration change or alternate route. Preserve native `commandExecution` start/completion events, command target, exit status and a redacted error class. A final message saying an attempt occurred is not evidence. Require a real denied tool result for the mounted effective-skill write, path absence plus a complete bounded marker sweep for unmounted assets, unchanged before/after host hashes, runner sidecar 401, scoped grant acceptance and post-revocation refusal, host-side symlink rejection, and complete stage cleanup. If the native event or its exit result is absent, record **inconclusive**, not denial.

**Current gate:** the four-turn ceiling is authorized, but there is no nonpersonal credential or reviewed model-egress route. Therefore no `turn/start` may be submitted and E05 remains incomplete. The next concrete review artifact is the egress-sidecar and model-stage create/inspect preflight; the credential reference can be supplied separately without putting its value in either repository.
