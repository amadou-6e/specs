# Inspection - Interactions

[inspection.drawio](inspection.drawio) is the sole authority. This table is its searchable
interaction index.

| ID | Control | Result |
|---|---|---|
| `IN-01` | Editor back link | Returns to Editor |
| `IN-02` | Re-run inspection | Starts one durable inspection job while retaining the report |
| `IN-03` | Back to editor | Returns to Editor for remediation |
| `IN-04` | Proceed to publish | Opens Publish / Schedule when overall gate is pass or warn |
| `IN-05` | Medium tab | Selects Medium checks |
| `IN-06` | Hashnode tab | Selects Hashnode checks |
| `IN-07` | Dev.to tab | Selects Dev.to checks |
| `IN-08` | Check row | Selects or deselects evidence |
| `IN-09` | View full dump | Opens raw evidence in a new tab |
| `IN-10` | Tablet drawer close | Closes the evidence drawer; backdrop click is equivalent |

Loading, polling, refreshed data, and report/artifact failures use `SYSTEM` labels.
