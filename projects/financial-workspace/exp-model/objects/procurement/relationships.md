# Procurement relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| settles-procurement | transaction | procurement | 0..* | 0..* |
| contains-item | procurement | procurement-item | 0..* | 1 |
| substantiates-purchase | receipt | procurement | 0..* | 0..* |
