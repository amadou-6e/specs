# Income statement item relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| income-statement-items | income-statement | income-statement-item | 0..* | 1 |
| statement-item-supports-single-income | income-statement-item | single-income | 0..* | 0..* |
