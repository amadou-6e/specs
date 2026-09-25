# Income statement item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| income-statement-items | income-statement | income-statement-item | 0..* | 1 |
| reimburses-single-expense | income-statement-item | single-expense | 0..* | 0..* |
| reimburses-single-expense-item | income-statement-item | single-expense-item | 0..* | 0..* |
