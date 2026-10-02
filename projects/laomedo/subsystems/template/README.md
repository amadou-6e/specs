---
title: Snapshot-bound execution example
status: template
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Snapshot-bound execution example

Illustrative subsystem, not a separate accepted or implemented owner. Consumer: a flow
adapter asking to resume a run. Owner: execution service. In actual Laomedo work this
behavior belongs in agent-execution unless it gains an independent interface.

| Element | Cardinality | Purpose |
| --- | --- | --- |
| README.md | 1 | Scope, consumers and maturity |
| contract/README.md | 1 | Observable resume behavior |
| design/README.md | 1 | Registry and restoration mechanism |
| validation.md | 1 | Test mapping and gaps |
| contract/*.md, design/*.md | 0..* | Further owned detail |

Copy directly to a peer, replace identity, all example facts/links and template statuses,
retain required pages and index the entry. Read [contract](contract/README.md),
[design](design/README.md) and [validation](validation.md).
