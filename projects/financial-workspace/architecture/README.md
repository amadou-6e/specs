---
title: Financial Workspace architecture
status: active
kind: architecture
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related: []
---

# Financial Workspace architecture

Fixed top-structured category: this is the one system-wide architecture for the
Financial Workspace project. Focused documents may be added beside the ones below
(for example a future `architecture/reconciliation-model.md`), but the category does
not gain a copyable `architecture/template/` folder or arbitrary new top-level
partitions — that is what distinguishes it from an expandable folder collection.

## Contained elements

```text
architecture/
├── 1 README.md                 # this file
├── 1 data-model.md             # cross-system financial data model and Drive layout proposal
├── 1 cash-flow-workflow.md     # reproducible cash-flow analysis and Notion publication design
├── 1 migration-contracts.md    # existing-system migration rules (Notion, Drive, tax-year workspaces)
└── 1 drive-folder-example/     # illustrative Drive layout with representative original PDFs
```

## Documents

- [data-model.md](data-model.md) — the cross-system financial data model: Financial
  position / Cash flow / Open matters / Documents, tax as a cross-cutting concern,
  claims lifecycle, and the current vs. proposed Google Drive layout.
- [cash-flow-workflow.md](cash-flow-workflow.md) — the reproducible cash-flow
  analysis pipeline: portable repository layout, Drive source index and fetch
  contract, transaction/decision model, repeatable CLI procedure, and Notion
  publication.
- [migration-contracts.md](migration-contracts.md) — contracts for migrating the
  live Notion databases, recurring-service history, liabilities, Git-tracked
  statement evidence, the local Drive mirror cache, and tax-year workspaces.
- [drive-folder-example/](drive-folder-example/README.md) — a concrete, non-canonical
  example Drive tree populated with representative original PDFs.
