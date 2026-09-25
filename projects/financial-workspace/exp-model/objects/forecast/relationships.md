# Forecast relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-forecasts | account | forecast | 0..* | 0..1 |
| single-expense-forecasts | forecast | single-expense | 0..* | 0..* |
| single-income-forecasts | forecast | single-income | 0..* | 0..* |
