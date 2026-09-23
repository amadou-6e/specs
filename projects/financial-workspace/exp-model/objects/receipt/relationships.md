# Receipt relationships

Derived from [canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| substantiates-purchase | receipt | procurement | 0..* | 0..* |
| supports-occurrence | receipt | recurring-payment-occurrence | 0..* | 0..* |
| supported-by-receipt | cashflow-entry | receipt | 0..* | 0..* |
