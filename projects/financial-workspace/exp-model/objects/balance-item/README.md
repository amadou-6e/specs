# Balance item

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
balance-item/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
A dated balance observation for exactly one Account. Optional time and timezone preserve intraday precision when available. Booked, available and outstanding-debt balances have different meanings; do not sum them together.

Transaction statement opening/closing balances can support these items. The same observation may appear in overlapping statements. Parent statement fields remain source summaries, not additional positions.

For monthly reporting select the appropriate dated observation per account, currency and balance type. Do not silently substitute an older balance as if it were observed at month end.

- [Schema](schema.yaml)
- [Relationships](relationships.md)
- [Evidence forms](representations.md)
