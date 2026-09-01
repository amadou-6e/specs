# Inspection - State Diagram Index

The `INSPECTION · AUTHORITATIVE LIFECYCLE` region on the Report page of
[inspection.drawio](inspection.drawio) is the sole authority. This file is a searchable
projection.

| State | Draw.io behavior |
|---|---|
| Load report | Requests the latest inspection |
| Report | Shows platform gates and checks |
| Evidence selected | Populates the artifact panel or tablet drawer |
| Re-running | Preserves the current report while a durable job is polled |
| Publish / Schedule | Allowed only for pass or warn overall gates |
| Editor | Handles missing reports, back navigation, and remediation |
| Recoverable error | Report and artifact failures recover independently |

A failed overall gate disables `IN-04` but preserves diagnostics and editor exits.
