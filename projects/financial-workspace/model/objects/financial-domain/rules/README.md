---
title: Financial domain contract
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/financial-domain]
---

# Contract and invariants

This page defines testable system-independent guarantees. Native and repository representations may add fields but cannot weaken them.

## Identity and required meaning

Every entity has a canonical ID. Native identity is `(provider, native_id)`. Account identity does not depend on display name/path. Transaction identity uses a provider/account transaction ID, or a generated ID that retains its source and derivation. Purchase item identity remains distinct from email, order, and payment; order references are merchant/provider-scoped. Evidence identity is `(provider, immutable_source_id)`; filenames, paths, subjects, and hashes are attributes. Imports reject duplicate package source IDs and skip IDs present in a baseline. Merges preserve aliases and reviewed decisions.

| Entity | Required meaning |
| --- | --- |
| Account | ID, provider/type, ownership scope, currency or multi-currency policy |
| Transaction | ID, account, observed status, signed amount/currency, provider date, provenance |
| Purchase item / Order | Separate IDs; description, merchant, commercial date; an Order has 1..* items |
| Recurring service / Service month | Service ID and lifecycle; month identity is `(service_id, service_month)` |
| Journey | ID and travel date/interval, distinct from booking/payment |
| Matter / Claim | Separate IDs and lifecycles; claimed, approved, and paid amounts remain distinct |
| Tax year | jurisdiction, tax year, lifecycle |
| Evidence | provider ID, type, provenance; hash/coverage when available |
| Reconciliation link | ID, typed endpoints, method, review state, timestamps |
| Allocation | ID, endpoints, amount, currency |
| Monthly snapshot | scope, cutoff, balances/assets/liabilities and currencies |

Unknowns are null or explicit unsupported states, never guessed values. EUR/USD/null and non-negative amounts are current procurement-import constraints, not universal domain rules.

## Money, relationships, and reconciliation

Money uses decimal semantics at source precision and ISO 4217 currency. Account inflows are positive and outflows negative; purchases/claims may store unsigned magnitudes. FX requires original and converted money plus rate, source, and date. Allocations balance to the source amount within a declared rounding tolerance; remainders are explicit. Refunds/reimbursements are distinct linked transactions.

Evidence and transaction relations can be many-to-many and require explicit links; monetary splits require Allocations. Reconciliation states are `candidate`, `confirmed`, `rejected`, or `superseded`; only confirmed links support settlement conclusions. Amount/currency/merchant/date matches are candidates. Transfers between owned accounts are neither income nor expense; refunds and reimbursements are expense offsets absent another documented policy.

## Time, lifecycle, evidence, and rejection

Order, dispatch, service, travel, invoice, posting, value, payment, refund, claim, decision, reimbursement, filing, and assessment dates are distinct. Reporting periods name their policy/source date; statement coverage is an interval and snapshots are cutoff states. Planned, expected, inferred, projected, pending, observed, and reconciled are distinct. Changes retain event/effective time, source/actor, and evidence; corrections append superseding events.

Assertions link evidence or state `missing-evidence`, `inferred`, or `planned`. Derived artifacts retain source and transformation. Hash mismatch fails closed. Missing/unknown fields, invalid dates/enums, duplicate IDs, currency mismatch, imbalance, parser failure, incomplete coverage, or conflicting evidence produce rejection or review, never fabricated facts.

Implemented: procurement validation/idempotency, Drive IDs/hashes, parser transaction IDs, ledger IDs, exact-currency candidate matching and unresolved states. Adopted but incomplete: general schemas, lifecycle history, Allocations, FX, transfer pairing, snapshots, and end-to-end recurring/claim/tax validation.

## Verification

See [checks and historical results](../../../../processes/cash-flow/model-validation/financial-domain.md).
