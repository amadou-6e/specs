---
title: Mediated GitHub access for agent stages
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Mediated GitHub access for agent stages

This page owns the target execution boundary selected in
[decision 0004](../../../decisions/0004-mediated-git-gh.md). It is **not** a
claim about the present local runner. [GitHub account connection](github-account-connection.md)
selects browser sign-in by default and explicit tokens as an alternative, but
their concrete identity/permission verification, CLI transport, credential
custody and multi-user isolation still need design and evidence. The Q16 rules
below are a proposed contract, not an implemented
exactly-once guarantee.

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
The first-slice grant identified in [#175](https://github.com/amadou-6e/specs/issues/175)
covers pushing the run's branch, PR create/update and Actions read; a broader
CLI capability target does **not** enlarge that particular grant. The
[authentication contract merged in #150](https://github.com/amadou-6e/specs/commit/af7e7ea4c4e8d721aecc570c620e3943f607b9f0)
defines the narrower first-slice grant, but the live broker remains unverified.
Agent-created follow-up issues still require the user's review under
[IF-12](../../issue-integration/contract/interfaces.md#if-12--reviewed-follow-up-issue-publication);
calling `gh api` or GraphQL must not bypass that boundary. The mediator must
classify the effect and required approval before forwarding a general API
write; an unclassifiable write is denied, not treated as unrestricted access.

## Authority and lifetime

The agent container may receive a run-scoped **capability to ask Laomedo** to
perform a GitHub operation, but not an ambient host `gh` login or reusable
GitHub credential. The mediator checks run, invocation, repository, grant,
operation and expiry against durable records. It journals request identity,
authorization decision, dispatch and known result without storing credential
values in traces. Denial and uncertainty are distinct from confirmed success.
The trusted approval and grant carry the selected GitHub `connection_id` and
credential generation. The broker validates user and repository ownership;
the mediator rejects a new effect if that generation is no longer current,
and the credential owner resolves only the matching connection. A legacy
unbound grant is not sufficient evidence of the account-connection path.
It must stop accepting the run's writes when a grant is revoked, expires, or
the owned stage is orphaned; the selected orphan bound is 60 seconds. A
stopped container alone is not revocation evidence. Another run's grant must
remain unaffected.

## Failure and verification

- A repeated or lost response does not by itself authorize reissuing a
  non-idempotent GitHub write. The proposed Q16 rules below govern that
  boundary; they do not provide exactly-once remote execution.
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
  another valid run is unaffected. EXP-93's child-supervisor whole-tree
  result was negative; the later independently started lease-service probe
  survived that kill and revoked a **synthetic** grant, but did not test a
  real GitHub credential or the production service launch. This criterion
  remains unmet for live writes.

No transport/proxy architecture, token minting scheme, Git signing/hook
semantics or exact API mapping is accepted here. Those require a reviewed
design and bounded experiment before the current #93 draft can be promoted.
The [candidate transport and comparison matrix](../design/mediated-cli-transport.md)
is such a design proposal, not an acceptance of its architecture or a parity result.

## Q16: effect identity and uncertain writes (proposed)

For every remote mutation, Laomedo persists a run/invocation ID, grant ID,
repository, operation class, caller-visible effect ID, canonical request hash,
authorization decision and `sending` intent **before** dispatch. An effect ID
identifies one intended mutation within a run, not one network attempt. The
complete request includes target, method, body bytes or durable body reference,
relevant expected Git ref/commit, and approval identity. A later identical
delivery returns the saved confirmed result or `unknown` without dispatching
again; a different request under that identity is a conflict. The durable
journal distinguishes `not_sent`, `sending/unknown`, `confirmed`, and a known
non-creating `rejected` result. Losing the response after dispatch never
becomes `not_sent` merely because the remote item cannot be found.

For a known, complete, non-creating rejection, Laomedo may report `rejected`.
A timeout, disconnected caller, process death, HTTP 5xx, or ambiguous provider
response remains `unknown`. A retry by the transport, adapter, agent recovery
or backend restart must not emit a second remote write for the same effect ID.
Reconciliation is read-only and operation-specific:

| Operation | Evidence that may confirm the intended effect | If not conclusively found |
| --- | --- | --- |
| Git push | The exact target ref resolves to the intended commit, with ownership and intervening-ref changes checked. | `unknown`; a later different ref is not proof the push never happened. |
| PR create | Exactly one PR with the reviewed branch/target and an exact durable reconciliation marker or known provider ID. | `unknown`; zero or multiple candidates do not authorize another create. |
| PR update | The known PR ID plus an exact expected version/content check for the requested update. | `unknown` or conflict; do not apply an update twice merely because the first response was lost. |
| Reviewed follow-up issue create | [IF-12's](../../issue-integration/contract/interfaces.md#if-12--reviewed-follow-up-issue-publication) exact reviewed-request marker and unique remote match. | Keep IF-12 `unknown`; the user decides whether to abandon, bind or authorize a fresh attempt. |
| Arbitrary REST/GraphQL mutation | A documented operation-specific idempotency key, exact provider ID or explicit read-only equality check, if available. | `unknown`; there is no generic safe replay. |

The mediator must know the graph-level PR owner or supplied target PR before
authorizing create/update; discovering a related PR does not silently make it
the writable target. A new run or a newly authorized effect ID is a **new
attempt**, not crash recovery. If the previous effect remains unknown, show
the possible duplicate to the user and require explicit authorization before
another write. Read-only reconciliation may continue under its own valid
grant; revocation forbids new writes. This policy is at-most-one automatic
dispatch per recorded effect identity, not a promise that GitHub applied the
effect exactly once.
