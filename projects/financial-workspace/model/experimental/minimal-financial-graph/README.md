# Minimal financial graph

Replacement candidate for the current object-domain catalogue. The target is one Notion cashflow sheet with one entry per booked account transaction, enriched before upload from purchase documents, contracts and income statements.

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
minimal-financial-graph/
├── 1 objects.md
├── 1 representations.md
├── 1 cashflow-sheet.md
├── 1 migration.md
├── 1 validation-cases.md
├── 1 open-questions.md
├── 1 model.yaml
├── 1 relationships.md
├── 1 tree-views.md
└── 1 README.md
```
<!-- END GENERATED: contained-elements -->

## Reading order

1. [Objects](objects.md): meaning, identity and attributes.
2. [Relationships](relationships.md) and [model.yaml](model.yaml): canonical graph, cardinalities and allocation rules.
3. [Representations](representations.md): email, PDF, scans, exports and field provenance.
4. [Cashflow sheet](cashflow-sheet.md): flattened Notion fields and aggregation.
5. [Tree views](tree-views.md): account and cashflow navigation.
6. [Historical checks](validation-cases.md), [migration](migration.md) and [open decisions](open-questions.md).

Scope excludes tax, investments, new manual cash capture and a separate claims model. All available booked account movements are included; minimal transfer/wallet-funding classification is necessary for correct aggregate spending.

This defines intended behavior. Source extraction, matching and Notion publication are not implemented by these documents.
