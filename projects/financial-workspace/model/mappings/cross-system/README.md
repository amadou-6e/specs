---
title: Cross-system financial workspace model
status: draft
kind: cross-system-model
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related:
  - model/objects/financial-domain
  - model/systems/repository
  - model/systems/google-drive
  - model/systems/gmail
  - model/systems/notion
  - processes/cash-flow
  - migrations/0001-existing-system
---

# Cross-system financial workspace model

This entry owns mappings that let one financial fact move between the repository, Google Drive, Gmail, and Notion without losing identity, provenance, cardinality, or review state. Each linked model remains authoritative for its records and native identifiers.

## Ownership and consumers

This entry owns qualified references, domain-to-native crosswalks, authority precedence, many-to-many reconciliation links, handoff manifests, baselines, approvals, receipts, and verification. Financial meaning belongs to [Financial domain](../../objects/financial-domain/README.md); native objects belong to [Drive](../../systems/google-drive/README.md), [Gmail](../../systems/gmail/README.md), [Notion](../../systems/notion/README.md), and [Repository](../../systems/repository/README.md). Procedures and transitions belong to [processes](../../../processes/README.md) and [migrations](../../../migrations/README.md).

Cash-flow, procurement, recurring-expense, monthly-close, travel, claims, and tax processes consume these mappings. Operators review gaps and publication diffs; connectors fetch sources and upsert projections; audit tooling replays results.

## Guarantees

1. References retain namespace and native ID; paths, titles, amounts, and dates are matching evidence.
2. Projections retain canonical identity and evidence provenance. Publication does not transfer authority.
3. Links allow zero-to-many relationships; monetary many-to-many matches use explicit allocations.
4. Observed, inferred, proposed, approved, published, and rejected facts remain distinct.
5. Missing, changed, inaccessible, or conflicting evidence creates a gap or exception.
6. Publication requires a validated run, current baseline, exact package, package-bound approval, idempotent actions, receipt, and verification.

## Maturity and evidence

Status remains **draft**. Implemented evidence includes namespaced Drive sources in `config/cashflow/sources.yaml`, Notion IDs in `config/cashflow/notion_sources.json`, and a partial procurement run with hashes, baseline, Gmail IDs, gaps, and publication `not_run`. Drive and Notion observations date from 2026-09-13/14 and were not refreshed. Generic handoff schemas and complete-period discovery remain proposed.

Implementation branch `main` at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef` had extensive pre-existing changes, so it is workspace evidence rather than a clean release.


## Reading map

- [Structure](structure.md)
- [Schema](schema/README.md)
- [Rules](rules.md)
