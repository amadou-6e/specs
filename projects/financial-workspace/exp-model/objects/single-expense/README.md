# Single expense

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
single-expense/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> One nonrecurring expense event, including a planned event before payment.

Identity: single_expense_id.

Includes: Description or reviewed basis and realization state. Optional: Merchant, order reference, expected date/amount, travel details, budget and forecast links.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

These are type definitions; no illustrative instance is claimed as an observed record.

A Single expense may contain Single expense items and be supported by receipts. A reimbursement-kind Single income may link to the whole expense or its documented items; the reimbursement does not create another expense.
