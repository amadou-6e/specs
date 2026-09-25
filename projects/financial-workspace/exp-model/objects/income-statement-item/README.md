# Income statement item

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
income-statement-item/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
One line in an Income statement: an earnings component, deduction, reimbursement,
subtotal, total or informational entry. Preserve original labels and provider codes.

Income statement [1 : 0..*] Income statement item. Each item belongs to exactly
one statement. Zero items permits a statement whose detailed breakdown is not yet
available; it does not assert that the source document is empty.

- [Schema](schema.yaml)
- [Relationships](relationships.md)
- [Evidence forms](representations.md)

Gross/net figures on the parent are observed summary values. Items retain the
breakdown and any printed totals. Do not add printed totals to their components.
These lines enrich income evidence; they never create additional cashflow rows.

When this line is a reviewed reimbursement component, it may be allocated to a Single expense or specific Single expense items. Keep payroll settlement as its original transaction and avoid counting parent and item allocations twice.
