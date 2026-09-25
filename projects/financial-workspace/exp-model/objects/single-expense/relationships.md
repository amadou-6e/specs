# Single expense relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| settles-single-expense | transaction | single-expense | 0..* | 0..* |
| contains-item | single-expense | single-expense-item | 0..* | 1 |
| substantiates-purchase | receipt | single-expense | 0..* | 0..* |
| single-expense-budgets | budget | single-expense | 0..* | 0..* |
| single-expense-forecasts | forecast | single-expense | 0..* | 0..* |
| reimburses-single-expense | income-statement-item | single-expense | 0..* | 0..* |
