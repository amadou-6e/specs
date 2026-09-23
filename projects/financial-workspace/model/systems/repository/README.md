---
title: Financial repository model
status: draft
kind: system-model
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related:
  - model/mappings/cross-system
  - model/objects/transactions
  - model/objects/evidence
  - model/objects/reconciliation
  - processes/cash-flow
  - migrations/0001-existing-system
---

# Repository model

This entry defines the private repository as owner of versioned financial representations, executable reconstruction logic, reviewed decisions, and reproducibility evidence. Drive owns original files, Gmail owns original messages and attachments, Notion owns native pages and views, and the financial object models owns financial meaning.

## Ownership and consumers

The repository owns committed bytes and history, repository-relative paths, normalized records derived from external evidence, source catalogs and hashes, schemas, process instructions, exception and reconciliation records, and run artifacts. Cached provider bytes do not replace provider identity or originals.

Cash-flow acquisition consumes the catalog and cache. Procurement, recurring-expense, ledger, and reconciliation workflows consume saved data, decisions, exceptions, work products, and packages. Reviewers consume manifests, checks, reports, and Git history. Cross-system mappings belong in [cross-system](../../mappings/cross-system/README.md), financial semantics in [financial object domains](../../objects/README.md), and procedural sequencing in [cash-flow processes](../../../processes/cash-flow/README.md).

## Guarantees

- Repository paths are references within a stated Git revision, not provider identities.
- A source retains its provider ID and expected SHA-256; filename, path, size, or date alone cannot prove identity.
- `cache/` is replaceable and ignored. Cached bytes require a matching pin and cannot be the sole evidence reference.
- A unique run directory does not prove success; its manifest and validation determine status.
- Posted movements, purchases, service months, liabilities, snapshots, and projections remain distinct.
- Missing, ambiguous, excluded, and resolved records retain an exception trail.
- Credentials, tokens, browser profiles, and captured login URLs are prohibited.

## Implementation and maturity

Evidence was inspected on branch `feat/rclone-cashflow-fetch` at commit `89486b8`, with a materially dirty working tree. Implemented behavior includes a 30-object Drive catalog, local and cached SHA-256 verification, read-only rclone acquisition with post-download metadata checks, failure logging, and an isolated replay runner with declared input and output hashes. A saved report records 30 successful online byte checks on 2026-09-15.

This is a transitional hybrid. Legacy ledgers, statement extracts, reconciliations, reports, Notion snapshots, scripts, and newer run directories coexist. `data/cashflow/canonical/` has no posted transaction set; there is no closed-month PDF-to-analysis replay contract or Cash Flow Notion writer. Existing run formats do not enforce one complete manifest contract, so status remains `draft`.

## Basis

This inventory records evidence used for the repository model. Implementation paths refer to `financial-workspace` on `feat/rclone-cashflow-fetch` at `89486b8`, plus its dirty working tree, inspected 2026-09-23.

| Evidence | Supports |
| --- | --- |
| `README.md` and `docs/cashflow/` overview, methodology, and coverage | Topology, migration status, replay intent, coverage limits |
| `src/cashflow/sources.py` and its tests | Catalog identity, hashes, conservative dates |
| `src/cashflow/fetch.py` and its tests | Path containment, acquisition, cache replacement, failures |
| `src/cashflow/replay.py` | Input isolation and output comparison |
| `config/cashflow/sources.yaml` and `drive_inventory.json` | Thirty IDs, locators, hashes, sizes, dated metadata |
| Saved verification, procurement, and recurring run directories | Dated byte checks and variant run structures |
| `data/cashflow/` guidance | Intended canonical and run boundaries |
| `docs/cashflow/processes/` and `AGENTS.md` | Consumers and exception handling |
| `notion/snapshots/2026-09-08/` | Historical baseline |
| Spec cash-flow process and existing-system migration | Intended guarantees and acceptance criteria |

No live external system was inspected. Remote facts are limited to dated saved inventories and verification reports; provider-specific entries own their interpretation.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
