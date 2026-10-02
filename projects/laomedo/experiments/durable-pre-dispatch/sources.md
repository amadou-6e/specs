---
title: Durable pre-dispatch sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [Langflow readiness Q02/Q03 and E06](../../subsystems/langflow-integration/design/decision-readiness.md), specs 6ff8995.
- [EXP-04 issue](https://github.com/amadou-6e/laomedo/issues/34), which follows [EXP-03](../langflow-graph-freeze/README.md).
- [Laomedo SQLite prototype](https://github.com/amadou-6e/laomedo/blob/feat/34/laomedo/workflow_run_store.py) and [fault probe](https://github.com/amadou-6e/laomedo/blob/feat/34/experiments/exp04/probe.py).
- Existing [#22](https://github.com/amadou-6e/laomedo/issues/22) separately owns early identity and cancellation on the real agent runner API; this synthetic experiment does not close it.
