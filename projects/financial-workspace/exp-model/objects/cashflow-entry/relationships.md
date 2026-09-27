# Cashflow entry relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| contains-entry | cashflow-sheet | cashflow-entry | 0..* | 1 |
| projects | cashflow-entry | transaction | 0..1 | 0..* |
| supported-by-receipt | cashflow-entry | receipt | 0..* | 0..* |
| recurring-income-entries | recurring-income | cashflow-entry | 0..* | 0..* |

| budget-cashflow-entries | budget | cashflow-entry | 0..* | 0..* |
| forecast-cashflow-entries | forecast | cashflow-entry | 0..* | 0..* |
