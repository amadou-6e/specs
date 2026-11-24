---
title: Provider authoring direction
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-11-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Provider authoring direction

The earlier runner/journal/resource-plan ABC proposal is withdrawn by the owner.
Its abstract classes and inspection-only tests are removed from implementation.
Existing live provider execution remains, with no new provider assembly API
claimed. Read [the five boundaries and container acceptance requirements](provider-roles.md).

An author must eventually find required and optional implementations and their
connections at one clear entry point. Exporting many ABC names alone does not
meet that requirement. Only contracts consumed by shared Laomedo code should
be public extension points. `BaseAgent` interaction, `read_activity`, `readiness` and
`BaseModelCatalog.list_models` are the selected contracts linked above. A single
authoring entry point and the composition and construction of new providers remain
open; do not invent constructors or mark provider execution verified.

The first implementation step shares concrete Docker mechanisms and preserves
current provider lifetimes, error mappings and recovery behavior. Providers
supply native container specifications and protocol behavior, not separate
Docker lifecycle implementations. Acceptance requires real-image execution,
cancellation, resume and recovery evidence in addition to unit checks.
