---
title: Reconciliation rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Reconciliation rules

- States are candidate, confirmed, rejected, or superseded.
- Amount, currency, merchant, and date proximity create candidates only.
- Many-to-many monetary relationships require explicit allocations.
- Allocations balance within a declared tolerance; remainders and ambiguity remain explicit.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Example evidence boundary

Drive does not directly store Reconciliation links or Allocations. Examples must come from immutable repository-run artifacts and retain links to the original Drive, Gmail, statement, or Notion evidence used by the run.
