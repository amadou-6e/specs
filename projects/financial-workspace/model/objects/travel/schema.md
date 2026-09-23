---
title: Travel entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Travel schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Journey | `journey_id` | origin, destination, travel interval, purpose classification |
| Travel segment | `segment_id` | journey, mode, origin, destination, departure/arrival |
| Booking | `booking_id` | journey, provider reference, booking date, traveler |
| Travel stay | `stay_id` | journey, property, check-in/check-out |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
