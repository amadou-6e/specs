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

> The user-file multiplicity and first-slice workspace/grant details in this
> sketch remain open; see [Q10 and Q17](../../design/decision-readiness.md#question-ledger).
> The single `input_ref` is not a complete list of user-added files.

[Langflow integration](../../../langflow-integration/contract/interfaces.md) sends
a frozen stage request to agent execution. See the
[interface contract](../interfaces.md#if-05--invoke-a-configured-agent-stage).
`AgentRunSpec` and snapshot refs follow the [shared records](../../../../architecture/shared-contracts.md);
this shape adds workflow-stage correlation.

```text
StageInvocation {
  run_id: string, graph_revision_ref: Ref, stage_id: string,
  invocation_id: string, attempt_number: integer,
  agent: { provider: string, model: { requested: string, effective?: string },
           effort: { requested?: string, effective?: string } },
  prompt: { content_ref: Ref, hash: string }, skills: SkillSnapshotRef[],
  input_ref: InputSnapshotRef, upstream_artifact_refs: Ref[],
  session: { mode: "fresh" | "resume", native_session_ref?: Ref,
             expected_post_run_workspace_ref?: Ref },
  workspace: { mode: "local_mount" | "isolated_checkout", source_ref: Ref,
               optional_shared_home_ref?: Ref },
  permission_grant_ref: Ref, limits: { timeout_seconds: integer,
                                      turn_limit?: integer, spend_limit?: number }
}
```

`attempt_number` distinguishes loop invocations, not crash-recovery attempts.
For `resume`, the native session and expected post-run workspace must resolve
before dispatch. Effective-model timing, grant format and workspace isolation
policy remain open.
