---
title: Prompt and skill library interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Prompt and skill library interfaces

The catalog supplies versioned selections to run setup; it does not own
Langflow graph sequencing or agent dispatch. See the [interface map](../../README.md).

## IF-02 — resolve prompt and skill selections

- **Provider / consumer:** Prompt and skill library →
  [Langflow integration](../../langflow-integration/contract/interfaces.md).
- **Trigger:** selection or launch of a saved agent/workflow configuration.
- **Input:** requested prompt/skill identities, each with `latest` (default)
  or an explicitly pinned revision. A direct text prompt may be supplied as
  run input without first publishing it as a library item.
- **Output:** exact prompt revision/content reference and exact
  [skill snapshot reference](../../../architecture/shared-contracts.md),
  with provenance of the selector used. The launch path freezes the resolved
  refs for the run, including recovery. A missing or inaccessible revision
  fails visibly; it must not fall back to another version.
- **Open:** prompt revision serialization, native/GitHub synchronization,
  access/visibility and conflict resolution.

## IF-03/IF-14 — immutable skill revision boundary

The library consumes [skill registry](../../skill-registry/contract/interfaces.md)
revision lookup (IF-03). Library entries reference a registry skill identity,
exact revision and hash. A user/agent edit submits a draft proposal to the
registry (IF-14); it does not mutate the revision already referenced by a run.

For GitHub-backed publication, a PR is the default path. Direct editing of a
configured branch is an explicit setting; it does not retroactively change
running configurations. Native-backend publication is a distinct operation.
The exact authorization and merge/sync mechanisms remain open.

The library's prompt revision store is not silently folded into the existing
skill registry. Its ownership and storage mechanism require a separate design
decision before an implementation contract can be frozen.
