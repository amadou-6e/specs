---
title: Notion financial workspace model
status: draft
kind: system-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system, model/objects/reconciliation, model/systems/repository, migrations/0001-existing-system, processes/cash-flow]
---

# Notion model

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
notion/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
<!-- END GENERATED: contained-elements -->

## Consumers and guarantees

Procurement and recurring-expense publication, cash-flow migration, dashboards, import tooling, operators, and auditors consume this model.

- Native objects are identified by object type and provider ID. Titles, paths, view membership, amounts, and dates are matching evidence.
- Database, data-source, view, and row/page IDs remain distinct. A row page ID and external Source ID are separate aliases.
- Notion is authoritative for native identity and current presentation, not original evidence, reconciliation, or economic meaning.
- Dated exports and scoped baselines state retrieval time and coverage; they are not live syncs.
- Publication requires a fresh baseline, immutable approved package, unambiguous identity, compatible schema, classified actions, and a receipt.
- Views, formulas, helpers, and charts cannot create canonical financial facts.

## Maturity and limitations

Status is **draft**. The concrete [Cash Flow schema](schema.md) and [presentation topology](presentation/procurement.md) preserve the existing page, source, property, view, chart, filter, and helper configuration. Local evidence includes a complete 2026-09-08 legacy Procurement snapshot (260 rows in 12 databases), a 2026-09-09 unified Procurement migration receipt, target IDs verified on 2026-09-14, and a partial 2025-12 test run whose publication was not run. Procurement creation exists through Google Apps Script; documented cash-flow and recurring-expense uploaders remain proposed. No live Notion system was queried, so remote facts are historical observations.

Repository evidence was reviewed on branch main at commit dcc72d596aac78bc90b5e45e6e89ba94be6baeef in a heavily modified working tree.

## Basis

This inventory records local evidence used for the Notion model. No external system was queried on 2026-09-23.

| Evidence | Date | Supports | Limitation |
| --- | --- | --- | --- |
| financial-workspace/config/cashflow/notion_sources.json | 2026-09-14 | Workspace and destination IDs | Read-only reference |
| migrations/0001-existing-system.md | 2026-09-14 | Preservation, baseline, parity, rollback | Proposed contract |
| notion/snapshots/2026-09-08 README and manifest | 2026-09-08 | Legacy coverage, counts, hashes | Predates unified source |
| notion/migrations/2026-09-09-unified-migration.json | 2026-09-09 | Migration receipt | Not replayed here |
| notion/examples/unified_procurement.json | 2026-09-09 | Cash Flow/Procurement page IDs, helper properties, chart tabs, scaffold behavior, counts, and migration references | Current parity unknown |
| notion/examples/kanban_configuration.json | 2026-09-09 | Workflow/table view IDs, category tabs, chart layouts, filters, placement, and empty-column behavior | Current parity unknown |
| scripts/prepare_notion_purchase_import.py | reviewed workspace | Serialization and Gmail IDs | Preparation only |
| procurement/recurring notion-upload procedures | reviewed workspace | Preconditions and stop rules | Recurring writer proposed |
| docs/cashflow/notion-publishing.md | reviewed workspace | Intended cash-flow publication | Writer absent |
| representative 2025-12 package/audit | 2026-09-15 | Classification, hashes, no publication | Partial test scope |

Repository observation: branch main, commit dcc72d596aac78bc90b5e45e6e89ba94be6baeef, with extensive pre-existing modifications.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
- [Procurement presentation](presentation/procurement.md)
