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

[Unified income and expense candidate](unified-income-expense-candidate.drawio) is a reversible visual proposal. It is not the canonical graph, object schema, or publication contract. It shows optional recurring agreements feeding Income and Expense events; Income Item and Expense Item belong to those events, while Receipt Item holds printed document lines (including income-statement lines). Both recurring agreement branches have optional Agreement Term records and feed individual events; both event branches have items, transaction and receipt evidence, and Cashflow Entry links. The two Agreement Term cards display the same proposed object type in separate columns. Dashed orange reimbursement links run from Income toward Expense or Expense Item and are intentionally directional. Review this proposal before migrating object identities or replacing the canonical ERD.
