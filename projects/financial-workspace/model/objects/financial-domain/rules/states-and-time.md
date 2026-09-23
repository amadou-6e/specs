---
title: Financial entity states and time
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/financial-domain/catalog, model/objects/financial-domain/relationships]
---

# States and time model

This view answers when facts happened, what is known, and how operational state changes.

```text
commercial: order -> dispatch -> delivery/return -> refund
service: service period start -> end
banking: pending -> posting -> value/settlement
travel: booking -> departure -> arrival
claim: submission -> decision -> payment
tax: tax year -> filing -> assessment -> payment/refund
reporting: policy period -> snapshot cutoff
```

Dates on different lines never substitute for each other. Reporting month names its source date/policy; statement coverage states its evidence basis; a snapshot is cutoff state; projections carry scenario and assumption date.

Epistemic states `planned`, `expected`, `inferred`, `observed`, `reconciled`, and `projected` are separate from lifecycle. Example lifecycles are Purchase `planned -> ordered -> confirmed -> settled -> returned/refunded`, Matter `draft -> submitted -> acknowledged -> approved/partially-approved/rejected -> paid -> closed`, and Reconciliation `candidate -> confirmed/rejected`, with confirmed links later `superseded`.

Transitions retain event/effective time, actor/source, and evidence. Corrections append events. Procurement labels Pending/Approved/Confirmed and crosscheck match labels are projection-specific and require explicit mapping; neither alone proves settlement.
