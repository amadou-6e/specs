---
title: Agent execution validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution validation

The initial authoring migration executed no new implementation test. Later
experiment evidence is added below with its own pinned version, task and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Snapshot-bound restart/resume | 2026-10-01 pilot, Codex 0.159.2 | Same native thread and snapshot observed; API only |
| Missing snapshot / cancellation / cap | Same four-turn pilot | HTTP 400 before reservation; 39 partial events; ledger 4/4 |
| Isolation / read-only / remote mode | #120, #122, Docker sources | Earlier failures retained; general grant and remote storage unproven |
| Claude parity | #121 | CLI blocker before model call; acceptance unknown |
| New IF-05/IF-06 stage invocation and same-session conflict | No new check | Target interface only; not executed |
| First-slice mid-turn container crash terminates invocation with partial/unknown evidence | No new check | Proposed rule; EXP-05 kills a fate-shared process, not a container while its backend survives |
| Fate-shared run/backend process crash retains only committed evidence | [EXP-05 synthetic crash probe](../../experiments/agent-evidence-crash/iterations/2026-10-03/results.md) | Six process kills plus a normal control preserved committed IDs/raw receipts, ended the run as crashed, and marked streams unknown or partial; no actual backend, container or provider was killed |
| Three-attempt same-session crash recovery | No new check | Deferred target pending controlled real-agent mid-turn crash/session-restart experiment, including repeated/lost external effects |
| Run-scoped approvals | No new check | Broker, expiry and unattended default remain open |
| IF-05 user files and durable pre-dispatch reservation | No new check | Separate hash-checked refs and refuse-dispatch rule specified; no product test |
| IF-08 raw receipt to projection correlation | [EXP-05 synthetic crash probe](../../experiments/agent-evidence-crash/iterations/2026-10-03/results.md) | Post-flush restart projected one committed receipt with matching sequence; replay/dedup policy and real provider events untested |
| IF-08 replay / IF-10 manifest supersession | No new check | Producer-stable dedup key remains open; manifest supersession not tested |
| OpenCode authenticated prototype | [2026-10-02 verification](../../experiments/opencode-agent/iterations/2026-10-02/results.md) | Native multi-skill fresh/resume, live runner API cancellation with `cancelled` status, and saved-flow execution without tweaks observed before the latest API-auth and worker-network fix. The later fix passed synthetic host checks, not a new live turn; fresh UI Stop and exhaustive boundary remain unverified |
| Reusable Langflow custom node | Eight synthetic component/graph checks, 34 host checks, installed catalog/flow round trip | UI Stop propagation deferred to Laomedo #22; browser visual placement not separately inspected |
| Installed native-node fresh/resume | [Four-turn attempt](../../experiments/native-codex-node/iterations/2026-10-01/results.md) | Catalog, flow round trip, tool results, bound restart/resume and host isolation observed; cancellation inconclusive, sample fresh task failed |
| Explicit node cancel / successful fresh task | [Authorized retry](../../experiments/native-codex-node/iterations/2026-10-01-retry/results.md) | Runner cancelled via transport teardown, 33 partial events; fresh native command confirms no marker; aggregate ledger 6/6 |
| Two-agent handoff / bounded controller / selected artifacts | [Two-turn chain](../../experiments/agent-handoffs/iterations/2026-10-01/results.md), ac204ab | Real Codex chain completed 2/2; 54 host + 15 pinned checks pass; real loop/cross-provider acceptance unobserved |

Current native-node detail: [implementation/acceptance record](../../implementation/native-langflow-node.md).

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
