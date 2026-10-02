---
title: Agent execution contracts
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution contract index

Canonical draft requirements: [Codex](codex.md), [Claude](claude.md), [isolation](isolation.md),
and the newer [subsystem interfaces](interfaces.md). The newer discussion changes
some assumptions in the older isolation draft; its conflict note must be
resolved before implementation acceptance.
Shared serialized records belong to [architecture](../../../architecture/shared-contracts.md).
[Validation](../validation.md) qualifies maturity; pilot observations do not silently
replace proposed read-only, identity or provider parity guarantees.

Contract container: README.md (1), indexed pages (1 each), additional owned interface/
configuration pages (0..*). New pages must have one observable behavior owner.
