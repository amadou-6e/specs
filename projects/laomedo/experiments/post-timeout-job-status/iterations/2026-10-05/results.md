---
title: Post-timeout status results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The amended diagnostic run returned `408 EXECUTION_TIMEOUT` with a job ID
after 3.031 seconds. Read-only job-status polls at 0, 1, 4 and 7 seconds
after that response all returned `500 JOB_FAILED`; the first was **before**
the runner effect. The synthetic endpoint recorded exactly one request, one
effect and one response write. The effect was about 3 seconds **after** the
408. Langflow's error response had no durable `error_detail` payload.

The first run at `95e991b` showed the same four HTTP 500s and one late
effect but did not retain the error code; it is not independent evidence for
`JOB_FAILED`. The committed [manifest](evidence/manifest.md) keeps both
observations separate.

This is **not a safe-timeout pass**. At the pinned Langflow revision, a
terminal failed job status did not account for the later external effect.
Neither `JOB_FAILED` nor `408` proves cancellation. The native job API is
not Laomedo's IF-06/07 partial trace. Real-agent cancellation, explicit
effect reconciliation and trace persistence remain untested; Q11 stays open
as a first-slice integration gate. [Laomedo #66](https://github.com/amadou-6e/laomedo/issues/66)
owns effect-aware partial trace integration; [#22](https://github.com/amadou-6e/laomedo/issues/22)
owns early real-runner identity and supported cancellation. These runs do not
establish a frequency or behavior for other Langflow versions.
