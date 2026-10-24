---
title: Agent execution design
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution design

Native app-server/SDK processes operate behind a separate runner. Source, effective and post-run snapshots are distinct. Resume restores the last post-run files before native thread reuse. Docker is a bounded prototype mechanism, not proof of production confinement.

Reconstructed from local specs and evidence reports; implementation was not re-executed
or independently verified by this migration. [Validation](../validation.md) pins the
observation boundary. Public behavior belongs to [contract](../contract/README.md).
Design container: README.md (1), focused mechanism pages (0..*). No language partitions
are needed for currently inspected material.

The [decision-readiness ledger](decision-readiness.md) separates first-slice
choices, unresolved ownership, research and bounded experiments. It is a draft
triage, not an additional execution contract.
The [mediated CLI transport proposal](mediated-cli-transport.md) compares a
credential-free per-run Git/CLI adapter with a proxy alternative and defines
the parity evidence still required by Laomedo #100.

The [Output Contract v1 design](output-contract-v1.md) proposes the declarative form, shared precheck evaluator, routable outcomes and bounded continuation for the credential-free Langflow demo.

The [node error states](node-error-details.drawio) own descriptive error popovers and safe diagnostic interactions for issue #181.

The [local runner recovery states](local-runner-recovery.drawio) own the app connection-error recovery controls and transitions.

The first pages of the recovery diagram are an editable **typography proposal**:
normalized collapsed/expanded panels and their type rules. The existing state
map is retained on its original page. The [current real panel reference](references/local-runner-recovery-current.png)
records the pre-normalization UI; it is not evidence that the proposal is implemented.
