---
title: Matters rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Matters rules

- A matter can exist without a transaction.
- Claimed, approved, paid, rejected, and outstanding amounts remain distinct.
- Lifecycle changes append events rather than replacing history.
- Refunds and reimbursements are expense offsets unless another reviewed policy applies.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Claims, demand letters, return requests, reimbursement submissions, insurer correspondence, and case communications may support Matters, Claims, and Matter events. A claim state remains separate from later payment Transactions. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
