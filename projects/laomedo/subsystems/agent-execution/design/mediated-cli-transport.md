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

## Review questions

- Is a bounded bundle plus exact staged-object check sufficient for repeated
  run-branch pushes, or is a remote helper required for acceptable Git behavior?
- Which literal `gh` commands/flags make the first usable slice, and which
  return an explicit unsupported exit before any provider call?
- How does the host store the trusted run-workspace mapping across runner loss
  without letting an agent nominate a different file or repository?
- Which remote reads conclusively reconcile each supported uncertain effect?
- How is branch-push-triggered CI exposure handled without silently widening
  the user's grant or assuming a workflow-file diff check is sufficient?
