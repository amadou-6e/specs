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

Canonical draft requirements: [Codex](codex.md), [Claude](claude.md),
[OpenCode](opencode.md), [isolation](isolation.md),
[authentication and credential lifecycle](authentication.md), the newer
[subsystem interfaces](interfaces.md), and per-exchange
[payload sketches](schemas/README.md). The newer discussion changes
some assumptions in the older isolation draft; its conflict note must be
resolved before implementation acceptance.
The tested local [runner API boundary](runner-api.md) owns bearer authentication,
endpoint behavior, and named-container teardown for the single-user prototype.
Shared serialized records belong to [architecture](../../../architecture/shared-contracts.md).
The [Langflow node interface](langflow-node.md) owns the proposed reusable custom
component, fresh/resume operations, typed outputs and client lifecycle limitations.
[Agent handoffs](handoffs.md) owns explicit transitions, bounded scheduling and the
current incomplete artifact/provenance/live-acceptance boundaries.
[Validation](../validation.md) qualifies maturity; pilot observations do not silently
replace proposed read-only, identity or provider parity guarantees.

Contract container: README.md (1), indexed pages (1 each), `schemas/` (1),
additional owned interface/configuration pages (0..*). The `schemas/` container
has its own index and one file per direct exchange touching this subsystem.
New pages must have one observable behavior owner.
