# Agreement term

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
agreement-term/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
One dated set of price and cadence terms for a Recurring-payment agreement.

The relationship is optional for the agreement: zero or more Agreement term records.
Each Agreement term belongs to exactly one agreement. Absence does not invalidate
the agreement or prevent its Recurring-payment occurrences from being recorded.

Identity: term_id.

- [Schema](schema.yaml)
- [Relationships](relationships.md)
- [Evidence forms](representations.md)

Effective dates, amount, currency and cadence come from reviewed agreement evidence.
They describe expected payments, not actual cashflow.
