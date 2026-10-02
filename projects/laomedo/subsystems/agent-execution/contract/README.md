---
title: Agent execution contracts
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution contract index

Canonical draft requirements: [Codex](codex.md), [Claude](claude.md),
[OpenCode](opencode.md), [isolation](isolation.md).
The tested local [runner API boundary](runner-api.md) owns bearer authentication,
endpoint behavior, and named-container teardown for the single-user prototype.
Shared serialized records belong to [architecture](../../../architecture/shared-contracts.md).
The [Langflow node interface](langflow-node.md) owns the proposed reusable custom
component, fresh/resume operations, typed outputs and client lifecycle limitations.
[Validation](../validation.md) qualifies maturity; pilot observations do not silently
replace proposed read-only, identity or provider parity guarantees.

Contract container: README.md (1), indexed pages (1 each), additional owned interface/
configuration pages (0..*). New pages must have one observable behavior owner.
