# Single income relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| settles-single-income | transaction | single-income | 0..* | 0..* |
| supports-single-income | receipt | single-income | 0..* | 0..* |
| single-income-budgets | budget | single-income | 0..* | 0..* |
| single-income-forecasts | forecast | single-income | 0..* | 0..* |
| statement-item-supports-single-income | income-statement-item | single-income | 0..* | 0..* |
| reimburses-single-expense | single-income | single-expense | 0..* | 0..* |
| reimburses-single-expense-item | single-income | single-expense-item | 0..* | 0..* |
