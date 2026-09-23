# Account relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| provides | financial-institution | account | 0..* | 1 |
| issues-for | account | transaction-statement | 0..* | 1 |
| records | account | transaction | 0..* | 1 |
