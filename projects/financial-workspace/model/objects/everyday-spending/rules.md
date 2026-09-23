---
title: Everyday spending rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Everyday spending rules

- Use this domain when item-level lifecycle tracking is unnecessary.
- A receipt line is optional and is not inferred from a statement description.
- Commercial date and posting date remain distinct.
- Reclassification to procurement preserves identity and provenance.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Example evidence boundary

The Drive folder `Financial Workspace/Everyday spending/Receipts/2026/` was observed empty on 2026-09-23. No receipt-backed Spending occurrence was verified, so this domain has no example. This is a dated coverage fact, not proof that no everyday spending exists.
