---
title: Playground host join bounded result
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Bounded result

The [Laomedo Phase G result at `74a2c13`](https://github.com/amadou-6e/laomedo/blob/74a2c13f37d8bb3463aff990aca76c06e7504d33/experiments/exp22/PHASE-G-LIVE-RESULTS.md)
reports one visible Playground Send, one persisted host reservation and one
real Codex runner start. The native turn failed before executing the task's
credential-read or long shell command. Its **redacted** error summary contains
nine `responseStreamDisconnected` retry events and one final `other` event,
with no HTTP status. The cause is unknown. The browser's Stop control was not
visible after the early failure, so no Stop click, bridge cancel or runner
cancel was observed. This is an **inconclusive cancellation result**, not a
negative sandbox or Stop result.

| Criterion | Observation | Assessment |
| --- | --- | --- |
| Real Playground-to-Codex route | One browser Send, host bridge start and real native runner start; one turn reserved at 7/12 | Observed for this failed turn |
| Durable cross-store identity | After bridge shutdown and disposable Langflow recreation, a fresh child process reopened the same host binding; one Langflow trace matched saved-flow UUID and reported graph ID in a linked span; native request/digest, run ID and private raw-event reference matched | Observed for one failed turn; reported graph ID is corroboration, not execution attestation |
| Visible Stop and native interruption | No shell command, Stop click, cancel route, `interrupted` event or terminal `cancelled` status | Not tested by this attempt; #22/Q11 remains open |
| Credential boundary | The content-free agent read did not execute. Neither local token appeared in sanitized result, pins, teardown or route logs | Token-publication check passed; stage credential unreadability not retested |
| Cleanup | Native terminal `failed`, owned container absent, disposable Langflow and both host servers stopped | Observed; no retry of the ambiguous attempt |

The absent sentinel is not cancellation evidence because its creating command
never started. The result does not establish a provider outage, stale login,
executing-graph attestation, semantic task success, hosted isolation or #93's
joint-outage and real push-credential revocation. Previous bounded Phase E and
F Stop observations remain separate positive cases. This new real route
establishes only the identity join at the failed-turn scope; it does not
combine that join with a successful visible Stop. The target contract stays
partially observed.
