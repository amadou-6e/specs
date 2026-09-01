# Overview - State Diagram

The `OVERVIEW - INTERACTION LIFECYCLE` and `OVERVIEW - REMOTE HEALTH AND REFRESH
LIFECYCLE` regions on the `Overview - Articles` page of
[overview.drawio](overview.drawio) are the sole authoritative state diagrams. User
transitions use `OV-*`; automatic API, debounce, refresh, and polling transitions use
the distinct `OV-S*` namespace.

This file is a searchable index of the states represented there. It must not introduce
states or transitions that are absent from the Draw.io. Mobile sidebar behavior is out
of scope.

## Stable states

| State | Required presentation |
|---|---|
| Loading | Five card-shaped skeletons; filters remain visible but do not show stale counts |
| Browse | Loaded article list with no selected article and no details panel |
| Filtered Browse | Loaded filtered list with criteria and count visible |
| First-run Empty | No stored articles; New article action is available |
| Filtered Empty | Articles may exist, but none match; Clear filters is available |
| Load Error | Collection-level failure with a retry path; no false empty state |
| Selected Open | Selected card and populated 300 px details panel |
| Selected Collapsed | Selected card and 12 px side strip; panel content hidden |
| Page Loading | Existing cards remain visible; pagination region shows progress |
| Page Failed | Existing cards remain visible; pagination region shows error and Retry |
| Job Queued | Selected action accepted; queued status visible in panel |
| Job Running | Selected action progress visible; duplicate submission prevented |
| Job Failed | Failure visible in panel with retry when supported |
| Connected Blogs Resolved | Connected Hashnode and Medium records are the source of truth for synchronization |
| Schedule Repaired | Each connected blog has an enabled internal 60-second schedule |
| Sync Queued | Overview reload or a due schedule has queued one idempotent sync job per platform |
| Sync Running | The durable worker is retrieving and reconciling remote articles |
| Collection Refreshed | Successful remote upserts are followed by a local collection refresh |
| Sync Failed | Existing cards remain visible; durable retry or the next recurrence may recover |
| Verification Stale | Saved credentials exist; remote proof is stale and one leased verification may run |
| Reauthentication Required | Platform needs attention and new remote jobs are paused |
| Temporarily Blocked | Platform needs attention until its challenge retry time |
| Rate Limited | Platform needs attention until the provider retry time |
| Unavailable | Platform needs attention until transport retry succeeds |

Navigation destinations are exits from Overview, not additional rendered Overview
states. Preview tabs remain inside the current state; only `Visit` is external.
Synchronization is automatic system behavior and does not introduce a manual Overview
button. The header counts usable connections and separately reports connections that
need attention. Saved cookies alone never count as authoritative remote proof.
