---
title: Timeout trace integration execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The protocol was committed at Laomedo `2a2a1ad` and the initial probe at
`6931275` before the first live call. That call produced `408`, four
`JOB_FAILED` reads and one late synthetic effect; the first observation was
committed at `19f823d`. Because the observation omitted the source row's
monotonic value, its effect hash cannot be independently recomputed.

Amendment `95c1121` preceded the changed capture code `a885197` and exactly
one separate one-call replication. The direct observation and five falsifying
checks were committed at `076030c`. The probe verified the effective
3-second server limit, used a single POST and four planned GETs, calibrated
host/container clocks, then reopened the SQLite store without redispatch.
Each run used a disposable localhost-only container and named volume, removed
after capture. No model, GitHub write or personal credential was used.

At `076030c`, the five evidence checks and all 133 main Laomedo Python tests
passed. The checks reject an omitted effect, fabricated complete/cancelled
status, a missing `JOB_FAILED` code and a tampered effect-source row. A host
attempt to run the optional Langflow component tests was inconclusive because
the pinned component runtime and runner-token fixture were unavailable there;
it is not counted as a passing check.
