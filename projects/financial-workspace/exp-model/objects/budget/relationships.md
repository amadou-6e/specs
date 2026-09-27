# Budget relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-budgets | account | budget | 0..* | 0..1 |

| budget-cashflow-entries | budget | cashflow-entry | 0..* | 0..* |
