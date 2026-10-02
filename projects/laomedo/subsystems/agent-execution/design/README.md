---
title: Agent execution design
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution design

Native app-server/SDK processes operate behind a separate runner. Source, effective and post-run snapshots are distinct. Resume restores the last post-run files before native thread reuse. Docker is a bounded prototype mechanism, not proof of production confinement.

Reconstructed from local specs and evidence reports; implementation was not re-executed
or independently verified by this migration. [Validation](../validation.md) pins the
observation boundary. Public behavior belongs to [contract](../contract/README.md).
Design container: README.md (1), focused mechanism pages (0..*). No language partitions
are needed for currently inspected material.

The [decision-readiness triage](decision-readiness.md) separates confirmed
first-slice choices, open product decisions, research handoffs and experiments.
It is not a replacement for the contracts or evidence of implementation.
