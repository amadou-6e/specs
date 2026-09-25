# Income statement relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| issues | employer | income-statement | 0..* | 1 |
| substantiates-income | income-statement | transaction | 0..* | 0..* |
| income-statement-items | income-statement | income-statement-item | 0..* | 1 |
| recurring-income-statements | recurring-income | income-statement | 0..* | 0..1 |
| supports-single-income | income-statement | single-income | 0..* | 0..* |
