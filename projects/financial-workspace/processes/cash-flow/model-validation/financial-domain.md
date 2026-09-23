---
title: Financial domain validation
status: draft
kind: validation
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/objects/financial-domain/contract]
---

# Validation

This page maps guarantees to checks and gaps for `main` at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`, inspected 2026-09-23 in a pre-existing dirty worktree.

| Guarantee | Check/evidence | Result and limit |
| --- | --- | --- |
| Spec structure | From `specs/`: `python tools/validate_specs.py` | Fails on pre-existing repository-model broken link to sources.md; financial-domain structure produced no error |
| Procurement validation/idempotency | `python -m unittest tests.test_validate_procurement_import` | Pass: included in 10 focused tests; current projection only |
| Source ID/hash fail closed | `python -m unittest tests.cashflow.test_sources tests.cashflow.test_fetch` | Pass: included in 10 focused tests; cataloged sources only |
| Unique purchase IDs | Parse 2026 source ledger | Pass: 161 rows, 161 unique IDs |
| Uncertainty retained | Parse crosschecks | Pass: SSKM 64 direct, 17 amount/date, 30 unmatched, 17 ambiguous, 5 split, 1 manual mismatch among 134 EUR-with-amount; wallet 58 match, 83 no-match, 20 amount-unknown across 161 |
| Candidate IDs/currency | Inspect wallet script/artifact | Pass for 436 PayPal/Revolut transactions; Revolut row IDs synthetic |
| Provenance/hashes | Inspect source catalog/code/tests | Pass for cataloged files; some coverage filename-derived/unverified; no live inspection |

## Gaps

Canonical schemas/merge tests exist only for part of the model. Scripts use floats/tolerances and no general Allocation or FX record. There are no canonical lifecycle, recurring-service, journey, matter, claim, tax-year, account, or snapshot fixtures. Heuristic reconciliation lacks a general persisted reviewer decision. Statement coverage needs content-level gap/overlap checks. Current Drive/Gmail/Notion parity was not inspected.

The entry remains `draft`; unsupported families and heuristic reconciliation are proposed or review-required.
