# Balance item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| account-balance-items | account | balance-item | 0..* | 0..1 |
| liability-balance-items | liability | balance-item | 0..* | 0..1 |
| statement-balance-items | transaction-statement | balance-item | 0..* | 0..* |
