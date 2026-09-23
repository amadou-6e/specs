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
