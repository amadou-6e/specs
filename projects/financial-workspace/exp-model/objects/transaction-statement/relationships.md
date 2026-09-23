# Transaction statement relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| issues-for | account | transaction-statement | 0..* | 1 |
| contains | transaction-statement | transaction | 0..* | 0..* |
