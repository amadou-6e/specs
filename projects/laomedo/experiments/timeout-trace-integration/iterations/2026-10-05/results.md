---
title: Timeout trace integration results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The amended v2 call returned `408 EXECUTION_TIMEOUT` with a job ID after
3.015 seconds. Four read-only status polls returned `500 JOB_FAILED`, two
before and two after the synthetic effect. Clock calibration supports that
multi-second ordering. The runner journal contains one entry, one effect
and one response write, not evidence of a real agent.

Laomedo saved run/trace/stage/invocation identity and one dispatch attempt
before the native call. Its append-only trace retained eight receipts:
reservation, dispatch, timeout, two job-status deliveries, effect, and two
more job-status deliveries. The effect receipt's `sha256:` source reference
matches the committed sanitized runner row. Before and after reopening the
SQLite store, the trace was identical: workflow `timed_out`, invocation
`failed`, native job `failed`, effect `observed`, evidence `partial`, action
uniqueness `uncertain`, and no redispatch on startup sweep. `JOB_FAILED` was
never interpreted as proof of no effect or confirmed cancellation.

This demonstrates the **synthetic Laomedo-to-Langflow trace boundary only**.
It does not establish real-agent cancellation or that remote actions stop on
timeout. The [proposed contract](../../../../subsystems/langflow-integration/contract/timeout-reconciliation.md)
and first-slice Q11 still require the real-runner checks in
[Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22).
