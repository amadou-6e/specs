---
title: Mediated Git and GitHub CLI transport proposal
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Mediated Git and GitHub CLI transport proposal

Issue: [Laomedo #100](https://github.com/amadou-6e/laomedo/issues/100),
[specs #284](https://github.com/amadou-6e/specs/issues/284). This is a design
candidate for the [mediated GitHub contract](../contract/github-write-mediation.md),
not an accepted transport or evidence of parity. EXP-100 selected an operation
broker as the next experiment direction; it did not prove that normal `git` or
`gh` commands work. The [S11 check](../validation.md) verified a narrow
host-mediated push/PR path without a model, not an agent-created commit.

## Problem and boundaries

The current agent `/draft` is a file snapshot without `.git`; it cannot
produce a commit for the host's exact-commit push. The agent-side mediation
client accepts JSON operation names, not literal `git`/`gh` syntax. Simply
injecting a reusable GitHub token or mounting the user's `gh` profile would
defeat run-scoped revocation. Running host `gh` on arbitrary agent arguments
would expose token-export and unclassified mutation paths.

Keep the user's selected capability target, but distinguish a tested command
from a promise of all Git/CLI flags. Unsupported syntax must fail visibly;
neither the agent nor an adapter may silently fall back to host credentials.
The first-slice grant remains limited to its approved branch push, PR
create/update and Actions read. Follow-up issue creation still requires the
reviewed IF-12 request. Workflow-file writes need a separate trusted approval.

## Selected command surface (2026-10-09)

The [confirmed choice](../../../decisions/0004-mediated-git-gh.md#native-command-surface-selected-2026-10-09)
keeps normal `git push`/`git fetch` commands through a mediated remote helper
and puts the supported `gh` adapter on the agent container PATH. A separately
named JSON command is not the final compatibility surface. This selects a
direction, not the concrete helper protocol or complete Git/gh coverage.
Unsupported flags/operations fail explicitly; no host credential or raw
provider execution fallback is permitted. Existing narrower grants and
separate workflow/issue-publication approvals are not expanded by installation.

## Candidate transport for the next bounded experiment

1. The trusted controller prepares an isolated per-run Git repository from a
   pinned source commit, with no remote credential, credential helper, signing
   key, host Git config or user `gh` profile. The agent may edit and commit in
   that repository. Its `.git` data and working files are untrusted input to
   the mediator; they are never the place where the provider token is used.
2. A stage-side adapter accepts ordinary *supported* command forms and sends
   a typed request under its revocable run capability. For a push, the agent
   exports the intended ref/commit as a bounded Git bundle into its own run
   workspace. The adapter sends a durable artifact reference and expected
   remote ref, not a host path or arbitrary shell command.
3. The host resolves the artifact through the trusted run-to-workspace record
   saved before dispatch (not an agent-supplied path),
   rejects traversal, links and reparse points, copies its exact bytes into a
   private immutable staging area, and records the artifact hash. A bounded
   Git process first seeds a fresh bare repository with the pinned baseline
   objects from a trusted host source, then imports the bundle with ambient
   config, hooks, signing and credentials disabled. It accepts only a frozen
   bundle version/object format, no partial-object filter, exactly one
   expected ref and a pack passing object-integrity checks; it never checks
   out an agent tree on the host. A thin bundle may rely only on the trusted
   seeded baseline or a previously confirmed staged commit. The host validates the
   intended commit type, pinned baseline ancestry, repository, run branch,
   expected remote ref and workflow-file diff on those staged objects.
4. Only after validation and durable `sending` intent does the host resolve
   the selected credential and push the exact staged commit. The agent's
   remote URL, Git config, hooks, aliases, environment and input path never
   select the destination or credential. A confirmed first push may require
   an absent remote ref; later pushes require an exact expected current ref
   and fast-forward relation. The expected ref comes from the mediator's
   confirmed per-run branch journal or a fresh trusted host read, never the
   agent's remote-tracking ref. A mismatch found before dispatch is a known
   `rejected` result. After dispatch, a nonzero Git exit remains `unknown`
   unless a frozen, tested response category proves no remote creation;
   parsing arbitrary error text is insufficient. Read-only exact-ref
   reconciliation may confirm an uncertain push, but no automatic second
   push occurs. Effects on one run branch are serialized.
5. PR, Actions and later issue/API commands use the same capability and effect
   journal, with operation-specific classification. A `gh`-compatible adapter
   may map reviewed syntax to typed requests, but `gh auth token`, arbitrary
   extensions/aliases, unclassified REST mutations and GraphQL mutations are
   explicit unsupported/denied cases until independently designed and tested.
   The adapter must preserve safe stdin/body-file bytes through a durable body
   reference, or refuse that form; it must not silently drop flags. Unsupported
   syntax, mediator denial and provider 403 have distinct exit/stderr classes.
   Local presentation flags (`--json`, `--jq`, `--template`, pagination) are
   implemented and tested or explicitly unsupported.

This candidate adds a Git bundle transfer, not a mounted reusable token or a
general host command execution endpoint. Bundle byte/object-count/depth and
subprocess-time limits, staging retention and cleanup, concurrent file
replacement defense and exact `git`/`gh` syntax remain to be fixed in a frozen
implementation protocol. The trusted run record retains its workspace mapping
across runner loss for read-only reconciliation, without new write authority.
The same-user host process is not a multi-user security boundary.

First-slice branch history is fast-forward only. Amend/rebase with
`--force-with-lease`, branch deletion, tags, multiple refspecs and pushes to
non-run refs are explicitly unsupported or denied until separately approved
and tested; this is a visible parity gap. Git LFS objects and submodule
contents are not carried by the commit bundle and are unsupported/partial in
the initial comparison. The agent's author/committer metadata is recorded as
supplied, not rewritten. Branch protection requiring a signed commit must
fail visibly.

## Alternative to compare

A Git remote helper plus HTTP/API proxy could preserve more native syntax,
including `git fetch` and `gh api`. It would need a fully specified authenticated
Git wire-protocol route, endpoint/GraphQL mutation classifier, redirect policy,
TLS/hostname binding and explicit credential-export denial. The proxy must
still persist effect identity before a remote mutation and distinguish an
uncertain response from a safe retry. The experiment compares this alternative
with the broker; this page does not reject it as a future route. The
[Git remote-helper protocol](https://git-scm.com/docs/gitremote-helpers) and
[`gh api` syntax](https://cli.github.com/manual/gh_api) are the primary
references for the comparison, not evidence that either route works here.

## Frozen comparison required before a parity claim

### Selected representative REST write (2026-10-10)

The user selected "Use the existing PR-create boundary" for #100's REST-write
case. `gh api repos/OWNER/REPO/pulls --method POST --input FILE` (including `-`
for stdin) is an exact classified alias of the existing `pr_create` typed
operation, not a general REST-write permission. The input JSON contains only
string `title`, `body`, `head` and `base` fields. The body carries the configured
reconciliation marker; a durable effect identity is required. The classifier
rejects extra fields, other endpoints/methods and invalid input before mediation.
The host applies the same repository, run branch/base, explicit grant, Q16
intent/replay and target checks as ordinary PR creation. Old approvals and
first-slice operation sets do not grow. Arbitrary REST/GraphQL mutations remain
unsupported; the paired comparison must record that honestly rather than count
every unsupported case as a successful positive. This selects the mechanism;
the fresh frozen paired comparison is still required before a parity claim.

### Selected Linux service-manager test boundary (2026-10-10)

For #104, the user approved a disposable privileged systemd Docker test with
synthetic credentials and no persistent WSL changes. Its intended boundary is
real systemd unit/cgroup ownership: lease/mediator service and runners A/B have
separate cgroups; killing all of A's unit must leave the service and B alive,
revoke A's exact capability within60seconds, and deny a retained-capability
request without provider dispatch while B remains usable. Service restart and
expired/revoked renewal controls use production grant/lease code, a synthetic
provider and no model. No inner stage container exists; synthetic cleanup
must not claim actual Docker stage teardown. Existing Windows evidence owns
that separate claim.

Freeze and independently review the protocol and exact source/image before
execution. Use only trusted fixture code, network-none, a private cgroup
namespace, bounded runtime/resources, no host filesystem binds or Docker socket,
and exact identity/label/image checks for cleanup. Privileged mode still adds
access to the Docker VM; do not call this a hostile-code isolation proof.
The initial protocol is [S14 SYSTEMD-PROTOCOL.md](https://github.com/amadou-6e/laomedo/blob/9bcf8be/experiments/exp104/SYSTEMD-PROTOCOL.md).
No result is asserted here. This boundary does not prove production Linux
LocalRunner container routing, real GitHub writes on Linux, logout, power loss,
double-manager survival or Q11. The existing non-Windows route refusal stays
in place. A failed setup consumes its capture identity; do not add broader
host/cgroup mounts or replay the capture silently.

Use one disposable permission scope and equivalent **paired** repository
states, with fresh branch/PR/marker identities for direct and mediated sides
so the first side's writes cannot change the second side's preconditions.
Freeze exact command bytes, inputs, expected output and
exit class, remote read-back, run identities and maximum provider attempts
before execution. A control must show the checker fails if a write is silently
omitted, repeated, attributed to the wrong run, or allowed after revocation.

| Surface | Minimum representative cases | Current status |
| --- | --- | --- |
| Local Git | status, diff, add, commit; no host credential, hook or signing inheritance | Run workspace has no history; untested |
| Remote Git | fetch run branch (design gap); first and second fast-forward push; stale expected ref, amend/force-with-lease, tag/deletion/other ref, workflow-file change, timeout/unknown | Only fixed host exact-commit first push exercised; agent commit transfer and fetch untested |
| PR | create, read, update bound PR; wrong base/PR and lost response | Normalized host operations tested; literal `gh pr` untested |
| Issue | read/list; reviewed IF-12 create; unreviewed create denied | No agent-stage literal `gh issue` evidence |
| Actions | list/read for granted repository, wrong repository denied | Normalized read tested; literal `gh run` untested |
| `gh api` REST | same-repository GET, body file/stdin, paging; classified write and unclassifiable write | Diagnostic GET only; general writes untested |
| `gh api` GraphQL | read and mutation, variables, paging; mutation must be classified or denied | Unsupported at current mediator |
| Credential/export | `gh auth token`, aliases/extensions, inherited `GH_TOKEN`/GCM, process environment and mounts | Must be denied or absent, with negative evidence |
| Concurrency and loss | A revoked while B continues; duplicate effect and lost acknowledgement; mediator/service restart | S11 covers one no-model A/B runner-loss route, not literal CLI |

For each case record command, grant, effect ID, provider-attempt count, exit
code, stdout/stderr category, remote result and whether the container held any
reusable credential. Compare direct and mediated behavior by case, marking
`equivalent`, `different but authorized`, `unsupported`, `denied` or `unknown`.
Do not call the whole CLI surface equivalent because a subset passes. No
live write, model turn or service installation follows from this proposal.
Run no-write cases first, then bounded writes under a fixed provider-attempt
budget. A branch push may execute existing repository CI or local/composite
actions on agent-written code even when `.github/workflows/` is unchanged;
that risk is **not** contained by the workflow-file diff check. The pre-run
protocol must record the disposable repository's Actions/secrets exposure and
the user's selected policy before any live push. This page does not silently
add a new approval requirement.

## Native issue command classifier, #100 continuation

`gh issue view NUMBER` uses the existing selected-repository `api_rest_read`
GET for `/repos/OWNER/REPO/issues/NUMBER`, then checks exact issue identity and
refuses a PR returned by the issues endpoint. `gh issue create --title TITLE
--body BODY` (or bounded UTF-8 body file/stdin) emits existing `issue_create`
only with durable effect, marker and reviewed proposal identity. That identity
is an agent-supplied selector, not approval: the host's exact reviewed-request
hash must match every field, including title/body, before dispatch. Edited or
unreviewed drafts remain refused; unknown writes never automatically retry.

The trusted prototype controller can explicitly issue a scope and exact
reviewed_issue_requests through MediationStore. Existing RunGrantAuthority and
LocalRunner first-slice sets remain unchanged; these do not become default
runner issue-publication permissions. Command recognition is not agent-stage
acceptance or a new authorization endpoint. Do not present manually issued
prototype grants as production authority/runner integration evidence.

The frozen [paired comparison protocol](https://github.com/amadou-6e/laomedo/blob/8e219b7f3ae5381324af969d9b0fe2c7810f63eb/experiments/exp100/PAIRED-PROTOCOL.md)
precedes new adapter/harness code. It proposes independent equivalent synthetic
provider states and actual direct Git/gh commands versus mediated commands in
the pinned agent container, with exact source/input/attempt caps independently
reviewed before capture. A direct `gh api` baseline is an effect/normalized-field
comparison, not proof of identical high-level `gh pr`/`gh issue` internals or
formatting. GraphQL and unsupported paging/general writes are classified as
unsupported, never equivalent. A prospective protocol is not executed evidence;
development tests and library-level exact-review controls do not close #100.

## Review questions

- The native remote-helper surface is selected above. Which trusted
  predecessor/fast-forward checks support repeated run-branch pushes while
  retaining the exact staged-object guarantee?
- Which literal `gh` commands/flags make the first usable slice, and which
  return an explicit unsupported exit before any provider call?
- How does the host store the trusted run-workspace mapping across runner loss
  without letting an agent nominate a different file or repository?
- Which remote reads conclusively reconcile each supported uncertain effect?
- How is branch-push-triggered CI exposure handled without silently widening
  the user's grant or assuming a workflow-file diff check is sufficient?
