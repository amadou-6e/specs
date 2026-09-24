# Recurring payment commitment relationships

[Canonical graph](../../relationships/graph.yaml).

| Edge | Source | Target | Targets per source | Sources per target |
| --- | --- | --- | --- | --- |
| defines | recurring-commitment | payment-occurrence | 0..* | 1 |
| commitment-terms | recurring-commitment | commitment-term | 0..* | 1 |
