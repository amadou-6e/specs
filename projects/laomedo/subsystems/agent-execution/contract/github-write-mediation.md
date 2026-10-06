---
title: Mediated GitHub access for agent stages
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-06
applies_to: [laomedo]
supersedes: null
related: []
---

# Mediated GitHub access for agent stages

This page owns the target execution boundary selected in
[decision 0004](../../../decisions/0004-mediated-git-gh.md). It is **not** a
claim about the present local runner. The GitHub identity/permission source,
CLI transport, Q16 effect identity and multi-user custody still need design
and evidence.

## User-visible capability

Within the selected user's GitHub permissions and an explicit run grant, an
agent can use its normal local `git` workflow and the authorized remote
`git`/`gh` capabilities needed by its task. Laomedo mediation must not silently
restrict the surface to only creating PRs. The parity target includes branch
fetch/push, general GitHub API and issue/PR operations, and Actions reads where
the grant permits them. A capability not yet supported must fail visibly
before execution or at the operation boundary; it must not be misreported as
a GitHub permission denial or silently replaced with a narrower operation.
The chosen user/grant still controls repository scope, write access and
approval. Workflow-file writes require their separately approved permission.

## Authority and lifetime

The agent container may receive a run-scoped **capability to ask Laomedo** to
perform a GitHub operation, but not an ambient host `gh` login or reusable
GitHub credential. The mediator checks run, invocation, repository, grant,
operation and expiry against durable records. It journals request identity,
authorization decision, dispatch and known result without storing credential
values in traces. Denial and uncertainty are distinct from confirmed success.
It must stop accepting the run's writes when a grant is revoked, expires, or
the owned stage is orphaned; the selected orphan bound is 60 seconds. A
stopped container alone is not revocation evidence. Another run's grant must
remain unaffected.

## Failure and verification

- A repeated or lost response does not by itself authorize reissuing a
  non-idempotent GitHub write. Q16 must specify effect keys, reconciliation
  and PR ownership before claiming deduplicated create/update behavior.
- If the mediator or credential owner is unavailable, writes fail closed.
  Reads and local-only `git` behavior may continue only when their own grant
  and failure policy permit; never fall back to host `gh` credentials.
- Compare a frozen matrix of representative direct and mediated operations
  using the same disposable permission scope. Include allowed operations,
  denied operations, unsupported syntax/endpoints, response/error fidelity,
  concurrent runs and credential absence from the agent filesystem/process
  environment. Count a parity gap as a gap, not a pass.
- Kill the runner at the selected failure boundaries, then attempt a write
  through the same run capability. Verify denial within 60 seconds and that
  another valid run is unaffected. The existing EXP-93 whole-tree result is
  negative, so this criterion is currently unmet.

No transport/proxy architecture, token minting scheme, Git signing/hook
semantics or exact API mapping is selected here. Those require a reviewed
design and bounded experiment before the current #93 draft can be promoted.
