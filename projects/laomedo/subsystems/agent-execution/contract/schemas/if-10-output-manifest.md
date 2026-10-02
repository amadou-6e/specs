---
title: IF-10 output manifest payload
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# IF-10: output manifest

Agent execution sends known outputs to
[results and artifacts](../../../results-artifacts/contract/interfaces.md).
See the [interface contract](../interfaces.md#if-10--report-produced-outputs).

```text
OutputManifest {
  run_id: string, stage_id: string, invocation_id: string,
  outputs: [{ artifact_id: string, kind: string, location_ref: Ref,
              content_hash?: string,
              state: "local" | "saved" | "published" | "unknown" }],
  target_pr?: { repository: Ref, number: integer, url: string,
                state: "created" | "updated" },
  manifest_state: "complete" | "partial"
}
```

`target_pr` requires a confirmed GitHub PR, not merely a local diff. Locations
need not be under the run directory. Artifact placement and retention remain
open; a partial manifest must not be interpreted as an empty output set.
