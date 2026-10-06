---
title: Durable pre-dispatch results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

| Crash phase | Durable run before restart | Attempt/callback count | After sweep |
| --- | --- | --- | --- |
| Before write | none | 0/0 | none |
| After commit before ack | present, caller unacknowledged | 0/0 | crashed |
| After ack before dispatch | present | 0/0 | crashed |
| After attempt before callback | present | 1/0 | crashed |
| After callback before completion | present | 1/1 | crashed |
| Normal | present | 1/1 | completed |

Every persisted row included recoverable run ID, trace ID, graph revision, component-code revision and resolved-config reference. The two middle windows demonstrate uncertainty: a committed attempt does not prove a callback ran, and a callback can run without a completed outcome. The store does not auto-replay either. The pre-dispatch persistence mechanism passed this synthetic test. Actual Langflow integration, early real-run identity and cancellation remain untested and belong to the subsequent implementation boundary and #22. Do not promote this into a production guarantee.
