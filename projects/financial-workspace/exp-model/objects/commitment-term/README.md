# Commitment term

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
commitment-term/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
One dated set of price and cadence terms for a Recurring commitment.

The relationship is optional for the commitment: zero or more Commitment term records.
Each Commitment term belongs to exactly one commitment. Absence does not invalidate
the commitment or prevent its Payment occurrences from being recorded.

Identity: term_id.

- [Schema](schema.yaml)
- [Relationships](relationships.md)
- [Evidence forms](representations.md)

Effective dates, amount, currency and cadence come from reviewed commitment evidence.
They describe expected payments, not actual cashflow.
