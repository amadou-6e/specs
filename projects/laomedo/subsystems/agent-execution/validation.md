---
title: Agent execution validation
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution validation

No implementation test was executed in this authoring migration. Evidence is bounded
by its original version, task, grant and date.

| Guarantee | Evidence | Boundary / gap |
| --- | --- | --- |
| Snapshot-bound restart/resume | 2026-10-01 pilot, Codex 0.159.2 | Same native thread and snapshot observed; API only |
| Missing snapshot / cancellation / cap | Same four-turn pilot | HTTP 400 before reservation; 39 partial events; ledger 4/4 |
| Isolation / read-only / remote mode | #120, #122, Docker sources | Earlier failures retained; general grant and remote storage unproven |
| Claude parity | #121 | CLI blocker before model call; acceptance unknown |
| New IF-05/IF-06 stage invocation and same-session conflict | No new check | Target interface only; not executed |
| First-slice mid-turn container crash terminates invocation with partial/unknown evidence | No new check | Proposed first-slice rule; pilot clean restart does not test a killed turn |
| Three-attempt same-session crash recovery | No new check | Deferred target pending controlled real-agent mid-turn crash/session-restart experiment, including repeated/lost external effects |
| Run-scoped approvals | No new check | Broker, expiry and unattended default remain open |
| IF-05 user files and durable pre-dispatch reservation | No new check | Separate hash-checked refs and refuse-dispatch rule specified; no product test |
| IF-08 replay / IF-10 manifest supersession | No new check | Producer-stable dedup key remains open; manifest projection rule not tested |

Canonical evidence: [pilot result](../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md)
and [feasibility ledger](../../research/runner-feasibility/sources/README.md).
Follow reports for exact revisions and private-artifact limits. A bounded observation
does not accept every target guarantee.
