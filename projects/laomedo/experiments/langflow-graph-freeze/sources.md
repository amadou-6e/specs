---
title: Langflow graph freeze sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- Governing [Langflow readiness E02](../../subsystems/langflow-integration/design/decision-readiness.md), specs main at 6ff899522af54db3f8526c563f73500056ad8c5e.
- [EXP-03 issue](https://github.com/amadou-6e/laomedo/issues/33).
- Pinned image: langflowai/langflow 1.12.3, sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0.
- Inspected installed langflow.api.v1.endpoints.simple_run_flow: reads flow.data, optionally uses a warm graph, otherwise copies graph data and calls Graph.from_payload before job execution. This is source evidence, not by itself a runtime freeze proof.
- [Fixture, probe and raw synthetic observation](https://github.com/amadou-6e/laomedo/tree/feat/33/experiments/exp03). No model or private transcript is involved.
