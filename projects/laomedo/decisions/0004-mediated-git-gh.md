---
title: Mediate agent git and gh capabilities
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-07
applies_to: [laomedo]
supersedes: null
related: []
---

# Mediate agent git and gh capabilities

## Status and source

On 2026-10-06, after the first-slice credential-revocation choice was posed,
the user selected “laomedo mediation but equivalent to git gh in capability.”
The choice is preserved in [specs #244](https://github.com/amadou-6e/specs/issues/244).
This record reconstructs the surrounding discussion; it is not a verbatim
transcript or implementation result. It remains draft until reviewed.

## Context and alternatives

[Agent execution Q07](../subsystems/agent-execution/design/decision-readiness.md)
offered mediated and journaled GitHub writes versus raw agent `git`/`gh` with
ambient credentials. The raw route gives agents a familiar broad interface,
but a credential copied out of an orphaned container cannot be revoked just
by stopping that container. [EXP-93](https://github.com/amadou-6e/laomedo/issues/93)
found that its *child* supervisor died under a whole-tree kill. The later
[independently started service result](https://github.com/amadou-6e/laomedo/blob/7707ba2/experiments/exp93/RESULTS.md)
survived the observed whole-tree runner kill and revoked a **synthetic**
grant. Neither result proves a production mediated path or a production
service launch.

## Decision and scope

Laomedo owns mediation of agent GitHub writes. The agent should still be able
to perform the `git` and `gh` operations its user-approved GitHub identity and
run grant permit; mediation must not arbitrarily reduce that capability to a
PR-only subset. This is a **capability-parity target**, not a claim that the
existing runner, a particular proxy, or a particular credential can already
provide it. A familiar CLI-facing workflow may be retained, but its transport
and enforcement mechanism are not selected here.

On 2026-10-07 the user also selected [browser-based GitHub account connection
by default, with explicit tokens as an alternative](../subsystems/agent-execution/contract/github-account-connection.md),
and rejected reuse of local host credentials. This settles the user-facing
connection modes, not their OAuth/token mechanism or implementation evidence.

The mediator must be able to stop accepting the run's writes on grant expiry,
cancel or orphan cleanup without relying solely on killing the agent
container. It must not expose an ambient host `gh` login or reusable GitHub
credential to that container. GitHub's own permissions and Laomedo's explicit
approval boundaries still apply; “equivalent” does not authorize actions the
user or GitHub has not granted. Workflow-file changes retain their separate
approval rule.

## Consequences and verification

The execution boundary needs an independently owned credential or write
service, run/grant identity, revocation, and a journal of attempted and
observed effects. Before calling parity implemented, compare representative
authorized `git` and `gh` operations through the mediated path with direct
operation under the same GitHub permission set. Include branch fetch/push,
PR and issue work, Actions reads, and the relevant general API surface;
report unsupported commands or endpoint classes rather than silently
claiming equivalence. No real personal credential is used in a disposable
probe. A post-kill write attempt with the same run grant must be denied within
the selected 60-second orphan bound, while another run's grant remains valid.

## Native command surface selected (2026-10-09)

After reviewing the partial literal CLI prototype, the user answered
"Preserve normal git/gh commands (recommended)" to preserving normal
`git push`/`git fetch` through a mediated remote helper and installing the
supported adapter as `gh` on the agent container PATH. The alternative was
a separately named mediation command. [Specs #311](https://github.com/amadou-6e/specs/issues/311)
records this confirmation; JSON-only push remains an intermediate compatibility
gap, not the selected final command surface.

This selects the interface and helper direction, not a Git wire protocol,
unlimited command coverage or runtime acceptance. Unsupported commands and
flags fail explicitly before forwarding. Agent containers retain only a
revocable run capability; no GitHub token, host login or credential fallback.
Existing run grants, workflow-file approval and uncertain-write fencing remain
unchanged. The helper and installed CLI require tests and frozen comparison
evidence before command compatibility can be claimed.

## Scoped native Git reads selected (2026-10-10)

The user answered "Yes, allow those scoped Git reads" to allowing first-slice
run grants to fetch the run branch and its configured base branch. This is
an explicit read-scope extension tracked by
[specs #314](https://github.com/amadou-6e/specs/issues/314), not implicit
authority from choosing normal CLI commands or connecting an account.
The trusted approval fixes the base branch; an agent cannot add arbitrary
refs or choose a different repository. Existing run approvals are not
retroactively expanded. Provider credentials remain host-only, and current
grant/connection checks precede returning acquired objects. No write permission,
workflow-file approval or uncertain-write rule changes. Runtime acceptance
still requires reviewed evidence under Laomedo #100/#104.

## Open questions

- Q16 owns operation/effect identity, retry and duplicate-write semantics,
  especially after an uncertain PR create/update result. The later
  [Q16 contract proposal](../subsystems/agent-execution/contract/github-write-mediation.md#q16-effect-identity-and-uncertain-writes-proposed)
  specifies no automatic resend of an uncertain mutation; mediation still
  does not make GitHub writes exactly once, and real-provider behavior is
  unverified.
- Browser-flow/token mechanisms and custody, CLI/transport compatibility,
  signing/hooks, audit retention and service placement need research and a
  frozen experiment. The selected connection modes do not imply a host-credential
  fallback or relax the run-grant boundary.
- An independently started service survived the observed whole-tree runner
  kill; the child supervisor did not. Service-manager stops, simultaneous
  service failure, deployment lifetime, real GitHub grant revocation, and a
  model stage remain unverified. This record does not select a production
  service mechanism or lift #93/Q11.
