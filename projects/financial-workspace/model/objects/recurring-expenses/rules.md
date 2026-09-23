---
title: Recurring expenses rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Recurring expenses rules

- A service month is identified by service and covered month, not payment date.
- Contract, invoice, service, due, and payment dates remain distinct.
- Price or cadence changes create effective terms rather than rewriting history.
- Missing settlement evidence remains unresolved and does not cancel the expected obligation.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.
