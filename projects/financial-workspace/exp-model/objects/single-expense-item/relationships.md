# Single expense item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| contains-item | single-expense | single-expense-item | 0..* | 1 |
| receipt-item-expense-items | receipt-item | single-expense-item | 0..* | 0..* |
| reimburses-single-expense-item | single-income | single-expense-item | 0..* | 0..* |
