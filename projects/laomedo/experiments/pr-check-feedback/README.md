---
title: Same-graph PR-check feedback
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Same-graph PR-check feedback

EXP-123 tests a custom wait/router integration inside one pinned Langflow graph.
The synthetic S1 result passed; production behavior remains unaccepted.
Tracked by [Laomedo #123](https://github.com/amadou-6e/laomedo/issues/123) and
[specs #298](https://github.com/amadou-6e/specs/issues/298).

README.md, protocol.md, sources.md and iterations/README.md: 1 each.
Ordered attempts: 0..*; each has overview, execution, results and evidence
manifest: 1 each. Replication: 0..1 per attempt only when actually performed.

Read [protocol](protocol.md), [sources](sources.md) and [S1](iterations/s1/README.md).
The [target gate contract](../../subsystems/langflow-integration/contract/interfaces.md#pr-head-check-gate-target)
owns behavior; this entry owns evidence and its limits.
