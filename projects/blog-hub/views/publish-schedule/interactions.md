# Publish / Schedule - Interactions

[publish-schedule.drawio](publish-schedule.drawio) is the sole authority. This table is
its searchable interaction index.

| ID | Control | Result |
|---|---|---|
| `PS-01` | Back | Returns to Inspection |
| `PS-02` | Edit | Opens Editor |
| `PS-03` | Medium selection | Includes or excludes Medium |
| `PS-04` | Medium mode | Selects Now or Scheduled |
| `PS-05` | Hashnode selection | Includes or excludes Hashnode |
| `PS-06` | Hashnode mode | Selects Now or Scheduled |
| `PS-07` | Schedule date/time | Sets a time at least ten minutes ahead |
| `PS-08` | Fix destination | Returns to Inspection for remediation |
| `PS-09` | Confirm and publish | Starts one explicit publish request |
| `PS-10` | Review and retry | Returns failed results to editable configuration |
| `PS-11` | View published destination | Opens the Medium result externally |
| `PS-12` | Fix failed destination | Returns to Inspection |
| `PS-13` | Back to overview | Opens Overview |
| `PS-14` | View article | Opens the first successful remote article externally |

Validation, job polling, and outcome refresh use `SYSTEM` labels. Network failure never
automatically retries a publish request.
