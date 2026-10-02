---
name: create-spec-linked-pr
description: Draft, open, or update a pull request with authoritative specification links, a spec-derived acceptance checklist, verification evidence, and definitive unresolved blockers linked to follow-up issues. Use when preparing a PR or its review handoff, not for implementing an unselected issue or activating repository enforcement.
---

# Create a spec-linked pull request

Read repository guidance, the actual diff against the intended base, applicable
specifications, and available test results. Describe the final implementation,
including limitations, rather than repeating the task plan. Preserve repository
templates and existing PR sections or reviews when updating a PR.

## Identify specification coverage

Identify the owning specs repository, applicable files and sections, and inspected
revision. Separate reviewed requirements from illustrative examples and historical
evidence. Link the specs PR for changed requirements and state the merge order;
when coverage is already merged, pin its commit. Never call an open spec PR merged.

For Laomedo, follow [the project policy](../../../projects/laomedo/implementation/spec-impact.md).
Every non-`fix/` branch declares a specs PR URL in `Spec PR:`. A `fix/` branch
declares `Spec PR: exempt (fix/ branch)` if it has no specs PR, but still cites
applicable coverage and supplies the checklist and blocker report. Fixes that
change a contract still need a spec update. A branch name does not establish
semantic coverage or authorize an unsupported behavior change.

## Derive the acceptance checklist

Create observable checklist items from the affected spec acceptance criteria,
invariants, and failure behavior. Each item links its governing section and its
verification evidence. Do not replace this with generic build/lint checkboxes.
Check an item only when evidence establishes it at the reported implementation
revision. Leave failed, untested, or inconclusive items unchecked and explain why.
Mark genuinely inapplicable criteria with a reason; do not present them as passed.

For a spec-only PR, derive criteria from the authoring/lifecycle requirements and
the stated specification change, such as preserved evidence links or explicit
contract ownership. Do not imply that document validation proves runtime behavior.
Record any missing acceptance criteria as a gap rather than inventing approved
requirements. Useful suggested criteria must be labeled proposals.

## Record failures and follow-up work

Distinguish a definitive unresolved blocker from a recovered failure, an untested
case, and an inconclusive observation. Cite sanitized evidence, observed effect,
and the scope blocked. Do not infer a sandbox denial from the absence of a write,
or infer isolation from configuration alone.

Each definitive unresolved blocker needs a linked follow-up issue with the
problem, reproducer or evidence, desired outcome, and independently verifiable
acceptance criteria. Prefer an existing issue if it already owns exactly that
work; otherwise create a new issue when authorized. Do not duplicate issues just
to populate a PR field. Follow local approval rules before editing existing
issues. If issue creation is outside the authorized scope or fails, prepare the
issue text, record the missing link, and report the PR as incomplete for this
requirement. Never invent an issue URL.

A follow-up issue does not make an unmet acceptance criterion merge-ready.
State whether the blocker prevents merge or is outside this PR's approved scope.
Changing that scope requires review of the owning spec. List recovered failures
with their resolution when they explain the result; they need no unresolved
blocker issue. Say `None observed` when appropriate and retain verification gaps.

## Prepare and verify the PR

Use [the body template](assets/pr-body.md) as a starting point and adapt it to
the repository's existing template. Keep meaningful existing content. Supply
the problem/result, spec-derived checklist, verification, blockers, and scope
limits for every PR, including fixes. Identify the actual head/base and any
stack dependencies. Use relative links only within the same repo; cross-repo
spec and issue links must be usable GitHub links, not local filesystem paths.

Verify references, checklist claims, and commands/results against inspected
artifacts. Run required checks appropriate to the diff. Write multiline PR bodies
to a file and use `gh pr create/edit --body-file` or a structured API argument.
Open or update a PR only within the user's authorized task. Re-read the published
body to confirm the links and checklist survived publication.

This skill authors PRs; it does not activate CI, branch protection, templates in
implementation repositories, or repository settings. Propose those changes
separately and obtain approval as required by repository guidance. Report which
requirements are contributor policy and which are active required checks.
