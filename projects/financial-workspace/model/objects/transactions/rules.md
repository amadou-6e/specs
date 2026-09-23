---
title: Transactions rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Transactions rules

- Inflows are positive and outflows negative at account level.
- Posting, value, authorization, payment, and observation dates remain distinct.
- Transfers between owned accounts are neither income nor expense.
- Expected charges and invoices do not become transactions until provider evidence shows movement.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Bank, card, wallet, and payment-provider statements or exports may directly support posted Transaction fields. Invoices, orders, and expected charges are not Transaction evidence until a payment provider records movement. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
