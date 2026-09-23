---
title: Travel rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Travel rules

- Travel date or interval is distinct from booking and payment dates.
- Titles include verified origin, destination, and travel date where available.
- Routes and dates are never inferred solely from merchant or amount.
- Work travel classification requires supporting employer or itinerary evidence.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Tickets, itinerary attachments, booking confirmations, and accommodation confirmations may support Travel objects. Planning spreadsheets are context only unless corroborated; merchant names and amounts cannot establish routes or travel dates. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
