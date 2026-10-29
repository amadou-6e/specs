---
title: Agent execution contracts
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution contract index

Canonical draft requirements: [Codex](codex.md), [Claude](claude.md),
[OpenCode](opencode.md), [isolation](isolation.md),
[shared local agent protocol](agent-protocol.md),
[authentication and credential lifecycle](authentication.md),
[GitHub account connection](github-account-connection.md), the newer
[subsystem interfaces](interfaces.md), and per-exchange
[payload sketches](schemas/README.md). The newer discussion changes
some assumptions in the older isolation draft; its conflict note must be
resolved before implementation acceptance.
The tested local [runner API boundary](runner-api.md) owns bearer authentication,
endpoint behavior, and named-container teardown for the single-user prototype.
The proposed [early-run cancellation handoff](early-run-cancellation.md) owns
idempotent asynchronous identity, pre-dispatch cancel and positive stop evidence.
Shared serialized records belong to [architecture](../../../architecture/shared-contracts.md).
The proposed [Output Contract](output-contract.md) owns downstream submission
validation and the separate agent-side precheck/correction boundary from the
release interview. It is not an implemented provider submission tool.
The [Langflow node interface](langflow-node.md) owns the proposed reusable custom
component, fresh/resume operations, typed outputs and client lifecycle limitations.
[Agent handoffs](handoffs.md) owns explicit transitions, bounded scheduling and the
current incomplete artifact/provenance/live-acceptance boundaries.
[Mediated GitHub access](github-write-mediation.md) owns the user-selected
`git`/`gh` capability-parity and revocable-run-grant target, including proposed
Q16 effect identity and uncertain-write handling. GitHub account connection
owns the selected browser-default and explicit-token modes; their concrete
transport, custody and runtime validation are still open.
[Validation](../validation.md) qualifies maturity; pilot observations do not silently
replace proposed read-only, identity or provider parity guarantees.

Contract container: README.md (1), indexed pages (1 each), `schemas/` (1),
additional owned interface/configuration pages (0..*). The `schemas/` container
has its own index and one file per direct exchange touching this subsystem.
New pages must have one observable behavior owner.

[Descriptive node errors](node-errors.md) owns user-facing explanations and safe technical diagnostics; original API error codes remain unchanged.

[Local runner API recovery](local-runner-recovery.md) owns app-level connection-error recovery, independent of graph elements.
