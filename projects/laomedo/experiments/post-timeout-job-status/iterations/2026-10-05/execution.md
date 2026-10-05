---
title: Post-timeout status execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The prospective protocol was committed at Laomedo `c5f2f68`, and its probe
at `5a44f98`, before the first live call. One v2 invocation returned `408`
with a job ID; four planned GETs returned HTTP 500. The first observation
was committed at `95e991b`. Since it omitted `detail.code`, no cause for
500 was inferred from that run.

Amendment `1c6790a` was committed before changed capture code `3f1e947`
and a second one-call run. The second observation was written directly by
the probe and committed at `3543a66`. Its four GETs captured `JOB_FAILED`.
Each call used a new disposable container and named volume; both were
removed. No timed-out invocation was retried. No model, GitHub or personal
credential was used. Host/container clock offsets and uncertainties are in
each observation; they support multi-second ordering, not sub-second claims.

At `3543a66`, four dedicated tests and 123 main Laomedo tests passed; Python
compile and Git whitespace checks passed. The dedicated tests reject missing
late-effect evidence, fabricated cancellation/safety, and a fabricated
pre-timeout effect. No IF-06/07 product trace was captured.
