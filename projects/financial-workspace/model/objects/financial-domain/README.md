---
title: Financial domain model
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system, model/systems/repository, processes/cash-flow]
---

# Financial domain

This entry owns the system-independent meaning of accounts, transactions, purchases, orders, recurring services, service months, journeys, matters, claims, tax years, evidence, reconciliation links, allocations, and monthly snapshots. These concepts form one boundary because their economic meaning remains stable across repository, Drive, Gmail, and Notion projections. Native identities belong to system entries, serialization to the repository entry, crosswalks to cross-system, and workflow to processes.

## Consumers

Procurement imports, ledger rebuilds, cash-flow replay, bank/wallet reconciliation, recurring-expense, travel, claim, tax and monthly-close workflows, integrations, reports, agents, and reviewers consume this model.

## Guarantees

- Expected purchases, liabilities, and claims are not transactions until provider evidence shows an account movement.
- Native IDs are provider-scoped; titles, paths, amounts, and dates are matching evidence, not identity.
- Money retains currency; cross-currency work requires an explicit rate basis.
- Many-to-many monetary relationships use links and allocations; ambiguity remains unresolved.
- Event dates, service periods, reporting periods, and snapshot cutoffs stay distinct.
- Evidence retains provenance and available hashes; missing evidence is explicit.

## Maturity and limitations

Status is **draft**. Implemented evidence covers the 2026 email-derived purchase ledger, procurement validator, statement source hashes, provider parsers, and SSKM/PayPal/Revolut crosschecks. Broader entity schemas, lifecycle events, allocations, FX, and snapshot valuation remain adopted contracts without complete fixtures. No live system was inspected; repository evidence was reviewed on `main` at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef` in an already dirty worktree.


## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules/README.md)

## Related descriptions

The [schema](schema.md), [relationships](structure.md), and [states and time](rules/states-and-time.md) provide the domain definitions.
