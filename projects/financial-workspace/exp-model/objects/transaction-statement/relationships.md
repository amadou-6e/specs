# Transaction statement relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| issues-for | account | transaction-statement | 0..* | 1 |
| contains | transaction-statement | transaction | 0..* | 0..* |
| statement-balance-items | transaction-statement | account-balance-item | 0..* | 0..* |
