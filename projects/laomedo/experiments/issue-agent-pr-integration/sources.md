---
title: EXP-19 phase-zero sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-19 issue](https://github.com/amadou-6e/laomedo/issues/49): full intended chain and explicit real-run prerequisites. This phase is narrower.
- [Work Graph contract](../../subsystems/work-graph/contract/work-graph.md): source snapshots, readiness and run binding remain distinct from dispatch authorization.
- [Issue integration interface](../../subsystems/issue-integration/contract/interfaces.md): selected issue context does not silently select a discovered PR.
- [EXP-04 evidence](../durable-pre-dispatch/README.md) and [EXP-05 merged evidence](https://github.com/amadou-6e/specs/pull/199): durable run identity and synthetic raw-event retention.
- [Laomedo fixture and implementation](https://github.com/amadou-6e/laomedo/tree/a36523845a1e718fb79fb40d42002a03c0cb4861): frozen base before phase-zero code. The executed revision and observation hash belong in the dated attempt.
