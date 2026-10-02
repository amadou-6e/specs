---
title: Work Graph subsystem
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph

Work Graph owns immutable repository-work snapshots, dependency evidence and
readiness projection. It binds selected work to agent runs without owning the
agent's session, skill revision or raw trace. Consumers are the planned Work
Graph view and the execution service. The initial read-only implementation is
described in [validation](validation.md); dispatch and UI remain proposed.

Read the [contract](contract/README.md), [design](design/README.md), and
[validation](validation.md).
