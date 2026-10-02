---
title: Runner isolation and persistence
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Runner isolation and persistence

> **Unresolved later-design conflict (2026-10-02):** the
> [subsystem decision record](../../../architecture/subsystem-decision-record.md)
> and [agent execution interfaces](interfaces.md) describe local workspace
> mounts, per-stage containers and an optional shared external Codex home.
> This earlier draft specifies read-only defaults and private provider profiles.
> The grants, identity and profile rules must be reconciled in review before
> either version is treated as an accepted implementation contract.
> For the **first-slice isolated-checkout stage**, the user subsequently chose
> a writable checkout with commit/push/PR capability; the read-only default
> below is superseded for that mode, not deleted. See the
> [decision-readiness triage](../design/decision-readiness.md#question-ledger).
> Whether reduced Docker protection can ever permit dispatch is deferred until
> an experiment is designed and assessed. No warning alone authorizes weaker
> protection.

Status: proposed. This is the shared execution boundary for Codex Agent,
Claude Agent, and Skill Draft. It specifies behavior, not a deployment choice
or a claim that a container alone provides security.

Current implementation: the
[2026-10-01 local pilot](../../../experiments/local-skill-agent-pilot/iterations/2026-10-01/results.md) retains
the tested Docker grant and mounts, uses independent workspaces and private
persistent sessions, and verifies native resume against post-run hashes.
Permission redesign is deferred. Its authorized existing single-user login
in the private volume is a temporary exception to the production identity
target; replacement remains with specs #129.

## Isolation goals

An automated run must not create sessions in the user's personal Codex or
Claude Code profile. It must be resumable and inspectable. Its filesystem,
credentials, network access, and side effects must match a recorded grant.
There are two distinct deployment requirements:

| Mode | Session location | What it guarantees |
| --- | --- | --- |
| Local private runner | Dedicated persistent runner directories on the same computer | Sessions stay out of personal agent histories; files still exist locally |
| Remote runner | Dedicated persistent directories on a server | No native session files are created on the user's computer by Laomedo execution |

The product must state which mode is active. If the user's requirement is
literally no session files on their computer, local private mode is
insufficient. A remote mode still may cache UI metadata locally, subject to a
separate data policy.

## Boundaries and lifecycle

Each run receives a unique ID and a workspace created from a pinned snapshot.
The source workspace and selected skill revision are immutable inputs. After
materializing skills, the runner hashes the effective workspace separately;
after execution it snapshots the resulting files. Read-only runs enforce
filesystem read-only access outside permitted temporary output. Skill edits
use a dedicated draft worktree, never the canonical skill
directory. Validate resolved paths and symlinks before mounting or copying.

Each provider has a runner-owned persistent profile root: `CODEX_HOME` for
Codex and `CLAUDE_CONFIG_DIR` for Claude. The process environment must not
inherit user-level profile paths or unrelated agent settings. A session
registry maps a native thread/session ID to provider, owner, profile root,
source and effective workspace snapshots, last post-run workspace snapshot,
active working directory, skill revision, and grant. Resume restores the
last post-run snapshot so session history and visible files agree; it fails
closed if that snapshot cannot be restored or a binding is incompatible.
Session data survives a runner restart.

Credentials live in the runner's credential store, not in a Langflow node,
flow export, trace, or spec repository. Multi-user deployments isolate
credentials and profiles per user or tenant. A shared personal login is not a
multi-user identity model. The first local prototype may be single-user, but
must still use a dedicated runner identity/profile.

## Permission grants

A grant names allowed filesystem roots, read/write mode, network policy,
tools, external side effects, and expiry or run scope. The executor applies
these restrictions outside the agent's prompt and records the effective
policy. Default flow execution is read-only with no replay of previous
writes, messages, or external calls. A skill-edit grant permits writes only
inside its draft root and approved validation output. Any later downstream
write mode requires its own grant and idempotency strategy. Bundled skill
scripts are disabled by a read-only grant unless it explicitly allows their
execution. Permitted scripts may write temporary output only to a designated
scratch directory, which is excluded from source snapshots but captured as
an output artifact when relevant.

An agent claiming a change was approved is not evidence of a grant. Any
provider-side approval prompt must be routed through the runner and recorded
as an observed decision. Unsupported restrictions block dispatch rather than
silently weakening the boundary.

## Failure and verification

The read-only-grant checks below remain useful for that legacy mode but do
**not** verify the first-slice writable checkout. For that slice, the
[readiness triage](../design/decision-readiness.md) additionally requires
stage-write versus protected-root tests, disposable external-write/orphan
tests, and a separately designed Docker-protection experiment. None has run;
do not infer writable-stage safety from a read-only test.

Timeout, cancellation, crash, or runner restart closes or recovers the job
without promoting a draft or labeling partial output complete. Persist the
event log and native ID if issued. Retention and deletion policy must cover
profiles, workspaces, snapshots, and raw traces together; duration is an open
product decision.

- Verify the personal Codex and Claude session directories are unchanged
  after an isolated run.
- Verify neither runtime discovers skills from the user's personal profile
  or home directory.
- Restart the runner and resume a compatible session from its private store.
- Resume after a file-changing draft turn restores the last post-run files;
  reject resume when that snapshot is unavailable.
- Attempt a path traversal, escaping symlink, source skill write, and network
  call under read-only grant; each must be blocked and traced.
- Verify a draft edit can write allowed files while the canonical tree hash
  remains unchanged.
- In remote mode, verify no native runner profile or session transcript is
  created on the client machine.
