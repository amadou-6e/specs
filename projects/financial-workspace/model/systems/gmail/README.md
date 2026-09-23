---
title: Gmail financial evidence model
status: draft
kind: system-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/evidence, model/objects/reconciliation, model/mappings/cross-system, model/systems/repository, processes/cash-flow]
---

# Gmail financial evidence model

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
gmail/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
<!-- END GENERATED: contained-elements -->

## Consumers and guarantees

Procurement, recurring-expense, travel, claims, tax, cash-flow, and monthly-close work consume Gmail evidence. Operators use native IDs to reopen originals, derived item identities to prevent duplicate projections, and coverage records to judge completeness.

- Message identity is mailbox scope plus Gmail message ID. Thread ID groups messages but never identifies one.
- Attachment identity retains mailbox, parent message ID, and native attachment ID. Filename, subject, URL, date, amount, and hash are attributes.
- Messages and attachments relate many-to-many to domain entities through cross-system links.
- Email proves only its content: an order confirmation does not prove settlement, and a refund notice does not prove a posted credit.
- Candidate inventories prove only enumerated IDs. Complete-period coverage requires exact query, account, time bounds, retrieval time, pagination terminal state, returned IDs, exclusions, and failures.
- Extracted facts retain field provenance; unavailable content and unhashed bytes remain gaps.

## Maturity, limits, and exclusions

Status is **draft**. A legacy extract and candidate-scoped December 2025 run retained five message IDs and links, five derived item identities, and six attachment IDs. They did not prove complete-month discovery, retain thread IDs, export MIME bytes, or hash the attachments. Gmail acquisition is manual; no shared schema, exporter, pagination replay, or deletion/change detection exists.

No live Gmail system was queried. Evidence was examined on branch `main` at commit `dcc72d596aac78bc90b5e45e6e89ba94be6baeef` in an extensively changed tree. This entry does not define financial entities, reconciliation, publication, or treat URLs, search results, threads, and caches as originals.


## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
