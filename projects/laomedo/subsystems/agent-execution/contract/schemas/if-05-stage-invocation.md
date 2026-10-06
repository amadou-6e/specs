---
title: IF-05 stage invocation payload
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# IF-05: stage invocation

[Langflow integration](../../../langflow-integration/contract/interfaces.md) sends
a frozen stage request to agent execution. See the
[interface contract](../interfaces.md#if-05--invoke-a-configured-agent-stage).
`AgentRunSpec` and snapshot refs follow the [shared records](../../../../architecture/shared-contracts.md);
this shape adds workflow-stage correlation.

```text
StageInvocation {
  run_id: string, graph_revision_ref: Ref, stage_id: string,
  invocation_id: string, loop_index: integer,
  dispatch_reservation_ref: Ref,
  runner_request_id?: string, runner_request_hash?: string,
  agent: { provider: string, model: { requested: string, effective?: string },
           effort: { requested?: string, effective?: string } },
  prompt: { content_ref: Ref, hash: string }, skills: SkillSnapshotRef[],
  input_ref: InputSnapshotRef,
  user_file_refs: [{ file_ref: Ref, filename: string,
                     media_type: string, content_hash: string }],
  upstream_artifact_refs: Ref[],
  session: { mode: "fresh" | "resume", native_session_ref?: Ref,
             expected_post_run_workspace_ref?: Ref,
             session_source?: { stage_id: string } },
  workspace: { mode: "local_mount" | "isolated_checkout", source_ref: Ref,
               optional_shared_home_ref?: Ref },
  permission_grant_ref: Ref, limits: { timeout_seconds: integer,
                                      turn_limit?: integer, spend_limit?: number }
}
```

`loop_index` distinguishes loop invocations, not crash-recovery attempts.
`dispatch_reservation_ref` identifies the durable pre-dispatch run/stage/
invocation reservation; if it cannot be committed, execution refuses dispatch.
For the first fresh Codex slice, `runner_request_id` is the already reserved
`invocation_id` UUID. Recovery adds `runner_request_hash`, a digest of the
exact native request body frozen before POST and checked again on read-only
lookup. The caller must not generate a new request ID on a timeout retry or
resubmit automatically. The separate runner identity is bound on acknowledgement under
the [Langflow integration contract](../../../langflow-integration/contract/runner-correlation.md).
`input_ref` carries the text/structured handoff, not an implicit collection of
files. Every user-added file has its own checked `user_file_refs` entry; an
upstream artifact is kept distinct and needs byte materialization by a later
owner. A missing or mismatched file hash fails before dispatch.

The first slice uses `fresh` and `isolated_checkout` only. For later `resume`,
the native session and expected post-run workspace must resolve before
dispatch. A `session_source` from another stage is a symbolic dependency, not
a native ID available at graph-definition time; its stage must precede this
one in the graph. Cross-stage workspace binding and local-mount exclusion are
unresolved gates. This sketch does **not** define re-submission after backend
death: that run is terminal, not reattached. Effective-model timing, grant
format and workspace isolation policy remain open.
