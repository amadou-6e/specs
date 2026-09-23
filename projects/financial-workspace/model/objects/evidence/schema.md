---
title: Evidence entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Evidence schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Evidence source | `evidence_id` | provider, immutable source ID, type, observation time, hash when bytes exist |
| Evidence assertion | `assertion_id` | evidence, subject, field or claim, source location, confidence |
| Coverage record | `coverage_id` | source scope, interval/query, completeness, gaps |
| Derived artifact | `artifact_id` | sources, transformation, version, output hash |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
