# Recurring-payment occurrence relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| defines | recurring-payment-agreement | recurring-payment-occurrence | 0..* | 1 |
| settles-occurrence | transaction | recurring-payment-occurrence | 0..* | 0..* |
| supports-occurrence | receipt | recurring-payment-occurrence | 0..* | 0..* |
