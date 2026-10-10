---
title: Active-run PR delivery and feedback
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Active-run PR delivery and feedback

## Status and source

The user selected this behavior in the 2026-10-09 conversation while the
mediated Git/PR lifecycle of Laomedo [#104](https://github.com/amadou-6e/laomedo/issues/104)
was being designed. This records product intent, not working Langflow or
GitHub-event integration. [Specs #296](https://github.com/amadou-6e/specs/issues/296)
owns the contract work and [Laomedo #123](https://github.com/amadou-6e/laomedo/issues/123)
owns the event-gate experiment.

## Context and decision

The existing bundle verifier accepts a completed run record, but a run's
mediated write grant is revoked at completion. The user chose to have the
agent prepare and submit its commit/PR **while its stage is alive**, so it can
read the resulting PR and correct an unsound body before finishing. Delivery
must still use the run-scoped mediator, not a GitHub credential in the agent
container. Bundle verification therefore needs a trusted active-run handoff;
it cannot be made to work by pretending a mutable running record is final.

A Langflow graph may place a GitHub PR-head/check gate after the agent stage.
It should associate the agent's exact PR head commit with the resulting check
event. A failed check may feed a **new agent invocation** in the graph with
the failure context; it must not silently replay the previous invocation or
repeat an uncertain GitHub write. The loop needs a configured bound and a
visible terminal result when exhausted. If the graph/backend has already
ended, any reaction is a separately authorized new run, not a resumption.

This is distinct from the already specified `pr_opened` or
`workflow_failed` **run-launch** events. A PR check gate observes an external
event during an existing graph run. Whether pinned Langflow can durably wait,
correlate and route that event is unverified; a tested adapter may be needed.

## Consequences and verification

- Agent execution owns safe staging, live grant checks and the mediated
  commit/push/PR operation; the agent may inspect and revise its PR body while
  the invocation remains active.
- An ingress boundary outside the agent must authenticate GitHub deliveries,
  persist correlation and suppress duplicate/stale deliveries. Its exact
  subsystem/process owner remains open; Langflow remains the live graph
  sequencer, not a webhook authentication service.
- Correlation includes repository, PR identity, exact head SHA, graph run,
  waiting gate and delivery/check identity. A check for an older head cannot
  decide a newer one. Events caused by the agent's own corrective commit
  must respect the same loop budget and cannot spawn an unbounded cycle.
- Test the active-run handoff, uncertain-write fencing and PR-body readback
  without a live GitHub write first. Then freeze a pinned-Langflow, no-model
  event-gate protocol before any claim of in-graph feedback. Provider writes
  remain subject to the separate #104 live protocol and review boundary.

## Managed startup and PR correction choice (2026-10-09)

In the continued interview the user selected a Windows per-user scheduled task
on this machine for managed host-service startup. Tasks run independently of
the agent runner, under the selected user's interactive login, without elevated
privileges or credentials in their action arguments. This does not establish
unattended operation after logout, service survival or production readiness;
those require separate checks. The host credential owner/lease service and
credential-free verifier have separate tasks. Replacing an existing task requires
checking its ownership and configuration, not overwriting a matching name.

The user also accepted automatic PR-body correction by reading the latest PR,
comparing the expected title, body, exact head SHA and authorized target before
one journaled update, then performing a fresh authoritative readback. GitHub's
update endpoint has no documented atomic conditional PATCH support: an edit
between the read and update may still be overwritten. This residual concurrent
edit race is accepted, not hidden by a claim of atomic compare-and-swap. A stale
snapshot is refused before writing; failed or mismatching post-write readback
leaves the effect unknown and never triggers an automatic repeat write.

[Specs #301](https://github.com/amadou-6e/specs/issues/301) records this selected
scope. Neither choice proves runtime behavior or authorizes a new live provider
write or model turn.

## Open questions

The GitHub ingress owner, check selection and timeout policy, Langflow's
waiting-node mechanism, graph snapshot behavior during a wait, and exact
failure payload need experiments/design. No choice here authorizes a new live
provider write or consumes a real-agent model turn.

## Output validation handoff refinement (2026-10-10)

[Decision 0007](0007-trusted-output-publication-handoff.md) records the owner-selected trusted active handoff for downstream Output Contract validation before publication. Agent completion must not be confused with the trusted stage handoff ending. The earlier evidence remains unchanged; the new handoff still requires implementation and its existing live gates.
