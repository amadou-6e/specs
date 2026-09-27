# Forecast relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-forecasts | account | forecast | 0..* | 0..1 |

| forecast-cashflow-entries | forecast | cashflow-entry | 0..* | 0..* |
