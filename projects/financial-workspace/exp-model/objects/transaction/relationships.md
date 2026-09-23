# Transaction relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| records | account | transaction | 0..* | 1 |
| contains | transaction-statement | transaction | 0..* | 0..* |
| substantiates-income | income-statement | transaction | 0..* | 0..* |
| settles-occurrence | transaction | recurring-payment-occurrence | 0..* | 0..* |
| settles-procurement | transaction | procurement | 0..* | 0..* |
| projects | cashflow-entry | transaction | 1 | 0..* |
| refunds | transaction | transaction | 0..* | 0..* |
