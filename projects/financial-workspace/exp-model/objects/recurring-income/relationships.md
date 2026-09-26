# Recurring income relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| recurring-income-receipts | recurring-income | receipt | 0..* | 0..1 |
| recurring-income-entries | recurring-income | cashflow-entry | 0..* | 0..* |
