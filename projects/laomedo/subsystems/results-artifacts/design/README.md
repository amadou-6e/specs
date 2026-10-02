---
title: Results and artifacts design
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and artifacts design

Candidate assembly joins immutable run context, correlated event/trace refs,
and agent-produced output refs by run and invocation identity. The run record
may store references to a workspace, GitHub branch, PR, report or another
persistent location. The destination is recorded rather than assumed.

The final artifact-placement rules require a later experiment covering output
types, destination defaults, user overrides, retention and unsaved outputs.
No storage engine or automatic relocation mechanism is chosen here.
Observable behavior belongs to [interfaces](../contract/interfaces.md).
Design container: README.md (1), focused mechanism pages (0..*).

The [decision-readiness ledger](decision-readiness.md) tracks remaining
artifact-retention, external-effect and crash-result questions; it is draft
triage rather than an additional result contract.
