# Receipt

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
receipt/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> Document supporting a financial event, including an income statement as a Receipt instance.

Identity: receipt_id.

Includes: Document kind, source representation. Optional: Issuer, order/document reference, issue date, Receipt items, total, currency.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

An income statement is a Receipt with document_kind income-statement. Its detailed lines remain Income statement items. Other Receipt lines are Receipt items, which may be matched to Single expense items. Existing income_statement_id values map to receipt_id during migration; do not create duplicate receipts.

These are type definitions; no illustrative instance is claimed as an observed record.
