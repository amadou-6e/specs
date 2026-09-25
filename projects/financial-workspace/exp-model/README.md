# Financial model replacement

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
exp-model/
├── 1 README.md
├── 1 objects/
├── 1 relationships/
├── 1 representations/
├── 1 systems/
├── 1 mappings/
└── 1 migration/
```
<!-- END GENERATED: contained-elements -->
> Concrete financial objects, their relationships, source forms and unified cashflow representation.

This is the contender to replace model/, not an experiment catalogue.

- [objects](objects/README.md)
- [relationships](relationships/README.md)
- [representations](representations/README.md)
- [systems](systems/README.md)
- [mappings](mappings/README.md)
- [migration](migration/README.md)

One entry per booked transaction; receipts enrich rows without creating money movements. An income statement is a Receipt with document_kind income-statement, while a reimbursement is a Single income with income_kind reimbursement. Transaction and Receipt are the two primary sources used to explain cashflow rows; Single income has its own relationship column. Tax, investments and new manual cash capture are out of scope.

## Metadata ownership

Object metadata explicitly links direct representations, supporting evidence forms, schemas, canonical graph edges and cashflow mappings. Schema fields own types and nullability; graph.yaml owns cardinalities; representation metadata owns encoding variants and locators. No copy of an edge or field definition in metadata is authoritative. tools/validate_specs.py checks the references and completeness.
