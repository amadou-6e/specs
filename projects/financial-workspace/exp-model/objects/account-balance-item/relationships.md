# Account balance item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-balance-items | account | account-balance-item | 0..* | 1 |
| statement-balance-items | transaction-statement | account-balance-item | 0..* | 0..* |
