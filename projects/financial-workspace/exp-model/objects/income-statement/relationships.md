# Income statement relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| issues | employer | income-statement | 0..* | 1 |
| substantiates-income | income-statement | transaction | 0..* | 0..* |
