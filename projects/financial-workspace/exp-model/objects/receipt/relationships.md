# Receipt relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| substantiates-income | receipt | transaction | 0..* | 0..* |
| substantiates-purchase | receipt | single-expense | 0..* | 0..* |
| supports-occurrence | receipt | payment-occurrence | 0..* | 0..* |
| supported-by-receipt | cashflow-entry | receipt | 0..* | 0..* |
| receipt-income-statement-items | receipt | income-statement-item | 0..* | 1 |
| recurring-income-receipts | recurring-income | receipt | 0..* | 0..1 |
| supports-single-income | receipt | single-income | 0..* | 0..* |
| receipt-items | receipt | receipt-item | 0..* | 1 |
