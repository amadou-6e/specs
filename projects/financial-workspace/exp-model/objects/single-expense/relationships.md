# Single expense relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| settles-single-expense | transaction | single-expense | 0..* | 0..* |
| contains-item | single-expense | single-expense-item | 0..* | 1 |
| substantiates-purchase | receipt | single-expense | 0..* | 0..* |
| reimburses-single-expense | single-income | single-expense | 0..* | 0..* |
