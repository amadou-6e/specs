# Liability

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
liability/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
The debt obligation, distinct from the Account administering it and from dated balance observations. Loans, credit-card debt and overdrafts are supported kinds.

A Liability can be recorded from its documents before the administering Account is identified. Dated outstanding amounts may be recorded as Liability-owned Balance items even before an Account is mapped. A balance covering several liabilities cannot be assigned in full to each one.

Original principal is an optional contract value, not the current outstanding amount. Liability terms preserve changes to the agreement over time. Unmapped liabilities remain an explicit financial-position coverage gap. Repayments do not automatically establish how much principal was reduced.

- [Schema](schema.yaml)
- [Relationships](relationships.md)
- [Evidence forms](representations.md)
