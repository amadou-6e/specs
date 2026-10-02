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
  status: "completed" | "failed" | "interrupted" | "partial",
  native_session_ref?: Ref, output_ref?: Ref, artifact_refs: Ref[],
  post_run_workspace_ref?: Ref,
  error?: { code: string, class: "input" | "permission" | "session_conflict"
                  | "provider" | "container" | "interrupted", message: string,
            recoverable: boolean }
}
```

An error carries the affected invocation identity; partial outputs remain
referenced. The error is required when `status` is `failed`, but may be absent
for an interruption or incomplete result. Recovery attempts remain within the
same invocation and session. The exact provider-to-error mapping remains open.
