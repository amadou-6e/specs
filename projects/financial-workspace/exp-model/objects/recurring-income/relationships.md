# Recurring income relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| employer-recurring-income | employer | recurring-income | 0..* | 1 |
| recurring-income-statements | recurring-income | income-statement | 0..* | 0..1 |
| recurring-income-entries | recurring-income | cashflow-entry | 0..* | 0..* |
