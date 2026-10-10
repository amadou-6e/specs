---
title: Laomedo release packages and product scope
status: draft
kind: architecture
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Two release packages

Product brief updated from the owner's release interview on 2026-10-10.
Inspected specs base: `e1aaa5fc356ae14d948cd8cf38f9509a55299d98`.
The [owner decision record](../decisions/0006-release-packages.md) preserves
the answers, corrections and question map. This specification work is tracked
by [specs #336](https://github.com/amadou-6e/specs/issues/336) on docs/336 in
the visible checkout. It records product intent and proposed acceptance, not
runtime evidence or release readiness. No implementation, configuration,
outreach or live write/model budget is granted by these documents. New UI
geometry/states/transitions still require reviewed Draw.io.

## Confirmed product direction and owners

The owner chose two packages, with independent component distribution alongside
upstream engagement and a single-user local application. Codex and Windows
come first. The initial success journey is issue → workflow → run → inspect →
automatically created draft PR. Immediate implementation is Langflow-only.

Canonical owners:

- [Decision 0006](../decisions/0006-release-packages.md): rationale, dated answers,
  corrections, question map, parked work and historical boundaries.
- [Community distribution](../subsystems/langflow-integration/contract/community-distribution.md):
  release/setup/support requirements.
- [Application execution](../subsystems/work-graph/contract/application-execution.md):
  assignment, tag resolution, explicit editing/chat handoff and demonstration.
- [Output Contract](../subsystems/agent-execution/contract/output-contract.md):
  downstream validation, precheck/correction and routed task outcomes.
- [Results](../subsystems/results-artifacts/contract/interfaces.md#interrupted-work-retention-selected-in-the-release-interview)
  and [run traces](../subsystems/run-traces/contract/interfaces.md#interrupted-trace-retention):
  interrupted changes and partial trace retention.

The two design briefs below explain mechanism/research work and preserve the
original review links. They no longer carry competing behavioral ownership.

## Package boundaries

| Package | Consumer | Proposed contents | Independent release gate |
| --- | --- | --- | --- |
| Langflow components | Langflow users and maintainers | Custom nodes, compatible runner/client distribution, sample flows and installation/account-connection documentation | Clean installation and supported-version component tests without depending on this developer's machine; distribution/credential/license review |
| Laomedo local application | One local operator | Issue board, workflow assignments, explicit workflow editing, run launch/progress, PR links and monitoring | Clean local setup and real issue-to-workflow execution with trustworthy identity, cancellation, output and trace evidence |

The components must not require the Laomedo UI. The installation experience
provides and configures their required runner automatically. Artifact format
and service lifecycle are technical design questions, not additional user setup.
The application reuses those components and the shared runner contracts rather
than maintaining a second execution implementation. Package versions must
declare compatible runner API, component and Langflow versions.

## Three different graphs and identities

The issue graph describes repository work and prerequisites. A workflow graph
describes configured executable stages. A run records execution of a frozen
workflow revision against a frozen task/issue snapshot. These are linked, not
interchangeable. Filtering the issue board does not modify readiness; editing
a workflow does not mutate an existing run.

Canonical owners remain [Work Graph](../subsystems/work-graph/contract/work-graph.md),
[Langflow integration](../subsystems/langflow-integration/contract/interfaces.md),
[agent execution](../subsystems/agent-execution/contract/interfaces.md),
[run traces](../subsystems/run-traces/contract/interfaces.md) and
[results/artifacts](../subsystems/results-artifacts/contract/interfaces.md).

## Reading and delivery sequence

- [Community component plan](../subsystems/langflow-integration/design/community-components.md): packaging investigation, maintainer approach and adoption evidence.
- [Application experience brief](../subsystems/work-graph/design/application-experience.md): issue assignment/launch, explicit editing, stage progress and node monitoring.
- Existing [resume/feedback acceptance audit](../implementation/resume-feedback-acceptance.md): a dated execution foundation, not evidence for the proposed UI.

The next owner-requested deliverable is the
[complete Langflow workflow demonstration](../subsystems/work-graph/contract/application-execution.md#next-requested-demonstration-the-complete-langflow-graph):
issue ingestion, Skill and Agent nodes, Output Contract, conditional success/
failure/rejection routing and actual draft PR creation. Separate node tests
do not meet this expectation. It can precede the standalone Laomedo UI.

Proposed sequence: complete existing runtime gates; investigate component
distribution; identify UI references and draft/review the owning Draw.io;
specify adapters and projections; implement a one-issue/one-workflow vertical
slice; test clean installation and failure handling; review each release
candidate independently. A community release need not wait for the full UI,
but neither may claim guarantees established only by the other's tests.

## Review scope

Review these three draft specifications together. Confirmed product choices
are recorded above; proposed gates and unresolved choices remain labelled in
each focused specification. They do not claim implementation or release readiness.

- Component package: review the candidate node scope, independent distribution
  route, research deliverables and proposed maintainer approach.
- Local application: review label assignment, alphabetical precedence,
  `latest`/pinned tags, workflow creation/editing, direct chat assistance,
  execution progress and agent monitoring.
- Shared boundary: review whether the two packages can release independently
  while sharing the same runner and execution contracts.

## Interview map and remaining work

The agreed [question map](../decisions/0006-release-packages.md#open-questions-and-agreed-map)
is the source of truth for progress. It records what each answer unblocks,
prefilled choices, redirections and remaining engineering/product questions.
No numeric execution budget or safe infrastructure-recovery protocol was
selected. [Decision 0007](../decisions/0007-trusted-output-publication-handoff.md)
selects a trusted active handoff through validation; its mediator lifecycle and
existing live gates still need acceptance. Reuse existing issue ingestion;
do not create a parallel importer for the demonstration.

## Proposed release acceptance

- Each package has a version, reproducible install/uninstall instructions,
  compatibility matrix, license/provenance inventory and supported-scope statement.
- A clean account connects using the selected provider's normal login. No
  credential, private session or developer path is included in an artifact.
- On Windows with Docker available, installation sets up the Codex components
  and runner automatically; the user signs in without manually configuring
  service addresses or component connections.
- The selected issue workflow automatically creates a draft PR, whose recorded
  reference opens from the run. Failures route according to the graph rather
  than being silently treated as successful publication.
- Agent prechecks provide correction feedback; the downstream Output Contract
  emits a validation outcome consumable by conditional routing.
- Interrupted work and partial traces remain inspectable until explicitly deleted.
- Installed examples and UI launch the same frozen workflow/run identity;
  failures, partial results and unknown usage remain visible.
- Editing while a run is active leaves that run on its original revision.
- Public documentation distinguishes tested providers/versions and local limits
  from proposed hosted, multi-user, Claude-provider or broader monitoring support.

These are candidate gates for review, not passing results. Remaining technical
and UX decisions belong in the focused briefs; they are not resolved merely
because related feasibility or triage issues have closed.
