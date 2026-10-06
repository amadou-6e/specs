---
title: Mediate agent git and gh capabilities
status: draft
kind: decision
owners: [laomedo-maintainers]
last_reviewed: 2026-10-06
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
also found that its child supervisor dies under a whole-tree kill. Neither
result proves a production mediated path.

## Decision and scope

Laomedo owns mediation of agent GitHub writes. The agent should still be able
to perform the `git` and `gh` operations its user-approved GitHub identity and
run grant permit; mediation must not arbitrarily reduce that capability to a
PR-only subset. This is a **capability-parity target**, not a claim that the
existing runner, a particular proxy, or a particular credential can already
provide it. A familiar CLI-facing workflow may be retained, but its transport
and enforcement mechanism are not selected here.

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

## Open questions

- Q16 still owns operation/effect identity, retry and duplicate-write
  semantics, especially after an uncertain PR create/update result. Mediation
  permits a journal but does not by itself make GitHub writes exactly once.
- Credential source and custody, CLI/transport compatibility, signing/hooks,
  audit retention and service placement need research and a frozen experiment.
- The supervisor must survive the selected whole-tree/service-manager failure
  boundary; the current child process does not. This record does not select a
  platform service mechanism or lift #93/Q11.
