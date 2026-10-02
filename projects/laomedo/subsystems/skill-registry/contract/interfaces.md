---
title: Skill registry interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Skill registry interfaces

The registry owns immutable skill bundle identities, hashes, drafts and
promotion separation. The proposed [prompt and skill library](../../prompt-skill-library/README.md)
owns curation and backend choice, not the exact bytes. See the
[interface map](../../README.md).

## IF-03 — revision lookup

- **Provider / consumer:** Skill registry →
  [prompt and skill library](../../prompt-skill-library/contract/interfaces.md).
- **Lookup input:** skill identity and `latest` or exact revision selector.
  `latest` is resolved once for a launch; the returned exact revision and
  tree/file hashes remain part of the run selection.
- **Lookup output:** immutable `SkillSnapshotRef` from
  [shared contracts](../../../architecture/shared-contracts.md), with
  availability and provenance. An unknown or invalid revision is an error,
  not an empty bundle.

## IF-14 — proposed skill edit

The [prompt and skill library](../../prompt-skill-library/contract/interfaces.md)
may submit a user/agent edit with base revision, edit-policy reference,
edit request or patch, and edit-run provenance when applicable. The registry
validates it as a distinct draft/proposed
revision. Promotion and GitHub publication are separate reviewed actions;
neither mutates a revision used by an active run. Existing
[draft rules](drafts.md) remain the owner of eligibility and validation.

## IF-04 — validated materialization for agent execution

For [agent execution](../../agent-execution/contract/interfaces.md), resolve
an exact `SkillSnapshotRef` to its declared dependency closure and validated
file bytes/hashes. The consumer records the effective workspace where they
were offered. A mismatch, missing dependency or escaping path fails before
dispatch. The registry must not infer that offering a skill proves the agent
read or used it; observed use belongs to [run traces](../../run-traces/contract/interfaces.md).

The registry does not own prompt revisions, saved Langflow graphs, workspace
selection or a GitHub publishing policy. Those boundaries need their own
contracts and must not be introduced by renaming the existing registry.
