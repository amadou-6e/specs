---
title: Accounts rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Accounts rules

- Account identity never depends on its display name or folder path.
- Provider-native identifiers are scoped to their provider and ownership context.
- Single-currency and multi-currency policies are explicit.
- Closing an account does not delete its transaction or snapshot history.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.
