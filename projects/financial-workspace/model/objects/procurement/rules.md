---
title: Procurement rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Procurement rules

- Purchase item identity remains distinct from order, email, and payment identity.
- Order references are merchant scoped.
- Order, dispatch, delivery, return, and refund dates remain distinct.
- Do not manufacture item allocations when evidence cannot explain an order total.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.
