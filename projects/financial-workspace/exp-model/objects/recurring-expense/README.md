# Recurring expense

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
recurring-expense/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> Continuing commitment.

Identity: recurring_expense_id.

Includes: Provider, service description, source or reviewed basis. Optional: Cadence, effective dates, versioned price terms.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

These are type definitions; no illustrative instance is claimed as an observed record.

[Commitment term](../commitment-term/README.md) is an optional child: [1 : 0..*]. Versioned terms are separate records, replacing the embedded terms field.
