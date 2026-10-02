---
title: IF-04 skill materialization payload
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# IF-04: skill materialization

Agent execution requests exact skill bytes from [skill registry](../../../skill-registry/contract/interfaces.md).
The [interface contract](../interfaces.md#if-04--obtain-exact-skill-bytes) owns the
dispatch rule; this page sketches the exchanged data.

```text
SkillMaterializationRequest {
  invocation_id: string, snapshot: SkillSnapshotRef, target_workspace_ref: Ref
}
SkillMaterializationResult {
  invocation_id: string, snapshot: SkillSnapshotRef,
  files: [{ relative_path: string, content_ref: Ref, hash: string }],
  dependency_snapshots: SkillSnapshotRef[],
  effective_workspace_ref: EffectiveWorkspaceRef
}
```

The result is returned only after path, dependency and hash validation. A
missing or mismatched snapshot is a coded failure, never an empty successful
bundle. Transport of file bytes and the exact failure code set remain open.
