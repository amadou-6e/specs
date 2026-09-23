---
title: Financial position rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Financial position rules

- A snapshot describes a cutoff state and is not a cash-flow period.
- Every valuation records currency, basis, source, and observation time.
- Expected amounts state their certainty and do not become observed balances implicitly.
- Corrections supersede snapshots without erasing the prior reviewed artifact.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Dated balance documents, account overviews, valuation statements, and loan balance statements may support positions. An aggregated Monthly snapshot requires declared scope and evidence for every included balance. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
