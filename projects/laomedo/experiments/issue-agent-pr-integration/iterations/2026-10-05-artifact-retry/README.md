---
title: EXP-19 artifact retry attempt
status: draft
kind: experiment-iteration
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Artifact retry attempt

This is a separate [#69](https://github.com/amadou-6e/laomedo/issues/69) follow-up to the [first live attempt](../2026-10-05-local-e2e/README.md), not a rewrite of its failed outcome. The [protocol amendment](../../protocol.md#artifact-retry-after-the-first-live-attempt) keeps the runner ledger cumulative. The user approved four additional submitted turns, including timeouts, so the ceiling is 10 after the first six. Turn 7/10 proved an agent-originated nested write. Turn 8/10 then ran the newly frozen issue-report flow and the trusted host published its verified artifact in [draft PR #71](https://github.com/amadou-6e/laomedo/pull/71). The one-draft-PR grant for Laomedo `test/49` into `develop` is consumed.

[Execution](execution.md), [results](results.md), and [evidence manifest](evidence/manifest.md) separate the canary, Langflow run and published draft PR with their exact identities and limits.
