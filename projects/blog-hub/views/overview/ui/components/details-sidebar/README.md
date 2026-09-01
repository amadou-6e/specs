# Overview details sidebar

Canonical source: [Overview Draw.io, page `Overview · Articles`](../../../overview.drawio)

| ID | State |
|---|---|
| `OVERVIEW-DETAILS-SIDEBAR-OPEN` | Article details visible beside the overview grid |
| `OVERVIEW-DETAILS-SIDEBAR-SUBMITTING` | Action acceptance pending; duplicate actions disabled |
| `OVERVIEW-DETAILS-SIDEBAR-QUEUED` | Durable job queued and identified |
| `OVERVIEW-DETAILS-SIDEBAR-RUNNING` | Durable job progress visible |
| `OVERVIEW-DETAILS-SIDEBAR-RECOVERING` | Reload-time active-job discovery visible |
| `OVERVIEW-DETAILS-SIDEBAR-RETRYING` | Durable retry pending; duplicate actions disabled |
| `OVERVIEW-DETAILS-SIDEBAR-FAILED` | Failure details and supported Retry visible |
| `OVERVIEW-DETAILS-SIDEBAR-CANCELED` | Backend cancellation visible and terminal |
| `OVERVIEW-DETAILS-SIDEBAR-COMPLETED` | Fresh article data shown after completion |
| `OVERVIEW-DETAILS-SIDEBAR-RECOVERY-UNAVAILABLE` | Discovery error visible with Retry recovery |

The sidebar and durable action-state studies appear beneath the article-card states on
the Overview tab.
Running-application screenshots are stored in `references/`. Draw.io inspection exports
are temporary and are not tracked.
