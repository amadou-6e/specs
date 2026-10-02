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
the newer [subsystem interfaces](interfaces.md), and the per-exchange
[payload sketches](schemas/README.md). The newer discussion changes
some assumptions in the older isolation draft; its conflict note must be
resolved before implementation acceptance.
The [decision-readiness triage](../design/decision-readiness.md) identifies
first-slice supersessions and unresolved choices; it does not turn either draft
into an accepted implementation contract.
Shared serialized records belong to [architecture](../../../architecture/shared-contracts.md).
[Validation](../validation.md) qualifies maturity; pilot observations do not silently
replace proposed read-only, identity or provider parity guarantees.

Contract container: README.md (1), indexed pages (1 each), `schemas/` (1),
additional owned interface/configuration pages (0..*). The `schemas/` container
has its own index and one file per direct exchange touching this subsystem.
New pages must have one observable behavior owner.
