# Single income relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| settles-single-income | transaction | single-income | 0..* | 0..* |
| supports-single-income | income-statement | single-income | 0..* | 0..* |
| single-income-budgets | budget | single-income | 0..* | 0..* |
| single-income-forecasts | forecast | single-income | 0..* | 0..* |
