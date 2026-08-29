# Publish / Schedule - State Diagram Index

The `PUBLISH · AUTHORITATIVE LIFECYCLE` region on the Configure page of
[publish-schedule.drawio](publish-schedule.drawio) is the sole authority. This file is a
searchable projection.

| State | Draw.io behavior |
|---|---|
| Load publish state | Requests destination draft and gate status |
| Configure | Selects destinations, delivery modes, and schedule times |
| Invalid | Keeps row-level corrections visible and disables confirmation |
| Publishing | Sends one request and polls its durable job |
| Outcome | Shows published, scheduled, skipped, and failed destinations |
| Request failed | Preserves configuration for explicit review and retry |
| Inspection | Handles back navigation and destination remediation |

The Outcome page defines both mixed completion and all-failed variants.
