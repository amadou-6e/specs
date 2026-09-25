# Budget relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-budgets | account | budget | 0..* | 0..1 |
| single-expense-budgets | budget | single-expense | 0..* | 0..* |
| single-income-budgets | budget | single-income | 0..* | 0..* |
