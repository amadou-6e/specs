# Single expense item relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| contains-item | single-expense | single-expense-item | 0..* | 1 |
| documents-expense-item | receipt | single-expense-item | 0..* | 0..* |
| reimburses-single-expense-item | income-statement-item | single-expense-item | 0..* | 0..* |
