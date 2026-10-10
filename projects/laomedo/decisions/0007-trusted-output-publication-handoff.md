---
title: Trusted active handoff through output validation
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Trusted active handoff through output validation

## Status and source

The owner selected **Trusted active handoff** in this Codex conversation on 2026-10-10 when asked to choose between that route and a separate publisher grant for [Laomedo #138](https://github.com/amadou-6e/laomedo/issues/138). This reconstructs that answer; exact message time is not retained. Tracking: [specs #338](https://github.com/amadou-6e/specs/issues/338). Concrete state/expiry mechanisms below are engineering proposals, not additional owner-selected values.

## Context and decision

[Decision 0005](0005-active-run-pr-feedback.md) requires publication while the trusted stage grant remains active. [Decision 0006](0006-release-packages.md) requires downstream Output Contract validation before the demo publishes. Keep a trusted stage handoff active through validation and publication, rather than revoking a grant at agent completion and later reusing or extending it. Agent execution completion and trusted handoff termination are distinct records.

The trusted controller, outside the untrusted executor, owns that handoff. The `agent_active` phase includes any permitted output-correction continuation. When that phase ends, stop admitting further agent-issued mutations; there is no transition from `validation_pending` back to `agent_active`. The handoff can admit only the already-scoped publisher operation after an accepted-success contract result, bound to exact run, repository, branch, immutable artifact digest and requirements revision. Results remains an artifact owner, not an implicitly authorized publisher. No raw GitHub token enters the agent or graph data.

## Proposed lifecycle and stopping rules

States are `agent_active`, `validation_pending`, `publication_pending`, then terminal `completed | rejected | failed | unknown | expired | cancelled`. Only the trusted controller changes them. The configured handoff deadline is frozen at dispatch and cannot be reset when the agent ends. No new numeric default is selected; refuse launch if no finite handoff deadline is configured. Rejection, task failure, interruption, cancellation or expiry revokes the grant without publication. Successful publication/readback revokes it on completion. Unknown write effects fence further mutation and revoke the capability; they never trigger automatic resend.

The independent lease supervisor and startup sweep cover the whole handoff, not just the executor lifetime. Runner/controller death must revoke within the existing 60-second orphan bound. Waiting indefinitely for graph validation is forbidden. A downstream publisher with only agent-visible data cannot mint or extend a grant. Existing Q16 durable effect identity must precede dispatch; readback reconciles uncertainty without another write.

## Consequences and verification

This refines the demo sequencing without relabelling earlier decision-0005 evidence or granting additional live privileges. It requires an explicit trusted mediator handoff implementation. Before live publication, credential-free tests must show all non-success routes deny publication, arbitrary graph data cannot authorize it, expired/revoked grants cannot be used, and controller loss revokes the same capability while another run continues.

[Laomedo #104](https://github.com/amadou-6e/laomedo/issues/104) and [#100](https://github.com/amadou-6e/laomedo/issues/100) remain live acceptance gates. [#139](https://github.com/amadou-6e/laomedo/issues/139) still requires a separate model-turn cap and scoped disposable GitHub identity. This decision supplies neither and activates no running configuration.

## Open questions

The exact controller-to-graph acknowledgment, handoff persistence/restart reconciliation, immutable artifact verifier and mediator command binding require implementation review under #138. A completed agent record alone is insufficient. No claim of production-grade authorization or safe generic retry is made.
