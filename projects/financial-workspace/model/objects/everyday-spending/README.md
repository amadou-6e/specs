# Everyday spending

<!-- BEGIN GENERATED: object-domain-summary -->
> Defines routine consumption where item-level procurement lifecycle tracking is unnecessary.

## Domain boundary

**Includes:**

- Spending occurrences
- Commercial date, merchant, amount, currency, and category
- Optional receipt lines supported by evidence
- Evidence and classification state

**Excludes:**

- Orders requiring item lifecycle tracking
- Inferred receipt lines
- Provider transaction records
- Raw receipts and statement files
<!-- END GENERATED: object-domain-summary -->

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
everyday-spending/
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
