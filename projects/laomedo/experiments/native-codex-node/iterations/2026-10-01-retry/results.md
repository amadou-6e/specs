---
title: Two-turn retry results
status: complete
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Gate | Outcome | Observation |
| --- | --- | --- |
| Explicit cancellation through imported node | Pass within tested mechanism | Cancel HTTP 200, interrupted run HTTP 500, runner cancelled, 33 retained events, no active Codex containers afterward |
| Successful independent fresh task | Pass | Native command result and final answer FRESH-MARKER-ABSENT; independent host workspace |
| Missing snapshot and exhausted cap | Pass | Errors before another model turn; ledger 6/6 unchanged |
| Automatic UI Stop / native interrupt acknowledgement | Not claimed | Cancel uses runner flag and transport teardown; #22 remains separate |

Cancelled run: ba0b596e-179e-4993-9d5b-5f395a23a70d.
Successful fresh run: 924e738a-db92-40cf-a14b-dd0ca8779ef3,
native thread 01a0f8eb-7441-7460-9def-3be5ad469978.

Together with the original fresh/restart-resume/catalog evidence, the bounded
#21 acceptance work is complete and ready for review. This is not issue closure,
spec approval, PR merge, production readiness or proof of every command's final
exit status. #22 and #24 remain declared limits; original attempts 3 and 4 stay
negative/inconclusive, not retroactively converted to passes.

