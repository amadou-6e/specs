# Receipt item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| receipt-items | receipt | receipt-item | 0..* | 1 |
| receipt-item-expense-items | receipt-item | single-expense-item | 0..* | 0..* |
