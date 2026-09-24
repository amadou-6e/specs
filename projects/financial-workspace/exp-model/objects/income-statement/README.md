# Income statement

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
income-statement/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
> One payslip or employer payment statement.

Identity: income_statement_id.

Includes: Employer, period, source. Optional: Gross/net amounts, deductions, reimbursement component.

- [Fields](schema.yaml)
- [Relationships](relationships.md)
- [Source forms](representations.md)

These are type definitions; no illustrative instance is claimed as an observed record.

[Income statement item](../income-statement-item/README.md) captures the optional line breakdown: [1 : 0..*]. Parent amounts remain observed summaries.
