---
title: Financial entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/financial-domain/relationships, model/objects/financial-domain/states-and-time]
---

# Entity catalog

This view answers which concepts exist, their stable identity, and current coverage.

| Entity | Identity | Meaning and coverage |
| --- | --- | --- |
| Account | `account_id` | Bank/wallet/card/loan/cash/investment; cataloged providers, no full schema |
| Transaction | provider/account `transaction_id` | Observed movement; parser-specific SSKM/PayPal/Revolut data |
| Purchase item | `purchase_id` | Acquired item/service; 161 unique email-derived 2026 IDs |
| Order | scoped order ID | Groups 1..* items; references exist, no normalized collection |
| Recurring service / Service month | `service_id`; service+month | Contract/scheduled month; proposed |
| Journey | `journey_id` | Travel interval; purchases exist, canonical fixture absent |
| Matter / Claim | distinct IDs | Stateful case and request; proposed |
| Tax year | jurisdiction+year | Evidence, filing, assessment, settlement; proposed |
| Evidence | provider+immutable ID | Messages/documents/statements; Drive IDs/hashes implemented |
| Reconciliation link | `link_id` | Reviewed expected-to-observed relation; specialized artifacts only |
| Allocation | `allocation_id` | Amount-bearing join; specialized split statuses only |
| Monthly snapshot | scope+cutoff | Point-in-time financial position; proposed |

Evidence at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`: procurement schema/validator, 2026 ledger/crosschecks, cash-flow source catalog, scripts, and tests.
