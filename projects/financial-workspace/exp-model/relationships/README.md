# Relationships

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
relationships/
├── 1 README.md
├── 1 graph.yaml
├── 1 rules.md
├── 1 tree-views.md
├── 1 records.yaml
└── 1 unified-income-expense-candidate.drawio
```
<!-- END GENERATED: contained-elements -->
[Graph](graph.yaml) owns edge definitions. [Rules](rules.md) define allocations, evidence and lifecycle. [Relationship tree views](tree-views.md) are navigation projections of selected paths through the graph, not separate edge definitions.

The one-page [ERD](layered-erd.drawio) is an editable, manually routed projection of the canonical graph. Validate it with `python tools/validate_specs.py` from the specs repository. The obsolete generator was removed because it would recreate superseded Employer nodes and layouts.

## Candidate relationship graph

[Unified income and expense candidate](unified-income-expense-candidate.drawio) is a reversible visual proposal, not the canonical graph, object schema, or publication contract. Its proposed object vocabulary is **Recurring Agreement** (`direction: income | expense`), **Agreement Term**, **Income**, **Expense**, **Income Item**, **Expense Item**, **Receipt**, and **Receipt Item**. The ERD contains exactly one Recurring Agreement node and one Agreement Term node. A Recurring Agreement has `direction: income | expense`; `income` permits the Income link and `expense` permits the Expense link; one agreement instance does not generate both directions.

An Income or Expense may have zero or one Recurring Agreement and has zero or more matching Items. Receipt Item is a printed document line that may match either item type. The dashed orange reimbursement links run from Income toward Expense or Expense Item and are intentionally directional. Review this proposal before migrating object identities or replacing the canonical ERD.
