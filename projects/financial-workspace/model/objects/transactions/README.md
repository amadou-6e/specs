# Transactions

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines observed movements of money and reviewed transfer relationships independently of purchase, invoice, or statement containers.

## Domain boundary

**Includes:**

- Posted or observed money movements
- Signed amount and currency
- Posting, value, authorization, and payment dates
- Counterparty and provider transaction reference
- Reviewed transfer pairs

**Excludes:**

- Orders and purchase items
- Invoices and expected charges
- Account identity
- Period balances and financial-position snapshots
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
transactions/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
<!-- END GENERATED: contained-elements -->

## Maturity

Status is **draft**. Implemented coverage varies by process; unsupported fields remain unknown rather than inferred.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
