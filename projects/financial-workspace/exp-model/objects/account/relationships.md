# Account relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| provides | financial-institution | account | 0..* | 1 |
| issues-for | account | transaction-statement | 0..* | 1 |
| records | account | transaction | 0..* | 1 |
| account-balance-items | account | account-balance-item | 0..* | 1 |
| account-liabilities | account | liability | 0..* | 0..1 |
