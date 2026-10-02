---
title: IF-06 invocation outcome payload
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# IF-06: invocation outcome

Agent execution reports one invocation to
[Langflow integration](../../../langflow-integration/contract/interfaces.md).
See the [interface contract](../interfaces.md#if-06--report-invocation-outcome).

```text
InvocationOutcome {
  run_id: string, stage_id: string, invocation_id: string,
  status: "completed" | "failed" | "interrupted",
  evidence_state: "complete" | "partial" | "unknown",
  native_session_ref?: Ref, output_ref?: Ref, artifact_refs: Ref[],
  post_run_workspace_ref?: Ref,
  error?: { code: string, class: "input" | "permission" | "session_conflict"
                  | "workspace_conflict" | "provider" | "container", message: string,
            recoverable: boolean }
}
```

`status` is the terminal outcome; `evidence_state` says how complete the
captured trace/output is. They are not competing statuses. An error carries
the affected invocation identity and is required for `failed`; a user Stop
can be `interrupted` with no error. A mid-turn container crash is `failed`
with class `container` and partial/unknown evidence in the first slice; it
does not automatically retry. A fate-shared backend crash ends the **run**
as `crashed`, rather than being reported as an agent error. Partial outputs
remain referenced. `workspace_conflict` is reserved for later local-mount
execution; first-slice isolated checkouts do not implement shared-mount locks.
The exact provider-to-error mapping remains open.
