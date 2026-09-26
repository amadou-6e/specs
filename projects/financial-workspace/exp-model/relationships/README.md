# Relationships

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
relationships/
├── 1 README.md
├── 1 graph.yaml
├── 1 rules.md
├── 1 tree-views.md
└── 1 records.yaml
```
<!-- END GENERATED: contained-elements -->
[Graph](graph.yaml) owns edge definitions. [Rules](rules.md) define allocations, evidence and lifecycle. [Relationship tree views](tree-views.md) are navigation projections of selected paths through the graph, not separate edge definitions.

The one-page [ERD](layered-erd.drawio) is an editable, manually routed projection of the canonical graph. Validate it with `python tools/validate_specs.py` from the specs repository. The obsolete generator was removed because it would recreate superseded Employer nodes and layouts.
