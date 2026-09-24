# Recurring payment agreement relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| defines | recurring-payment-agreement | recurring-payment-occurrence | 0..* | 1 |
| agreement-terms | recurring-payment-agreement | agreement-term | 0..* | 1 |
