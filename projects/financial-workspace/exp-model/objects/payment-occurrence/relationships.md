# Payment occurrence relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| defines | recurring-commitment | payment-occurrence | 0..* | 1 |
| settles-occurrence | transaction | payment-occurrence | 0..* | 0..* |
| supports-occurrence | receipt | payment-occurrence | 0..* | 0..* |
