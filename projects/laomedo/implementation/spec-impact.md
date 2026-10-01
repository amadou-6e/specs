---
title: PR specification impact
status: active
kind: procedure
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Specification impact for every implementation PR

## PR authoring requirements

Use the shared [PR creation skill](../../../shared/skills/create-spec-linked-pr/SKILL.md)
and its [body template](../../../shared/skills/create-spec-linked-pr/assets/pr-body.md).
Every PR includes a checklist derived from applicable spec criteria, with links
to governing sections and evidence. Check only verified outcomes; identify
untested, failed, inconclusive, and inapplicable criteria explicitly. Spec-only
PRs use authoring and change acceptance criteria without claiming runtime proof.

Every PR also reports definitive unresolved blockers and relevant failures.
Each definitive blocker links a new follow-up issue, or an existing issue that
already owns the same work, with evidence and merge impact. Recovered failures
record their resolution. A follow-up issue does not authorize merging unmet
requirements. If no blockers were observed, say so and retain verification gaps.
Existing issue edits still require explicit approval.

Non-`fix/` branches declare `Spec PR:` with a specs PR URL. Fix branches can
declare `Spec PR: exempt (fix/ branch)` but retain coverage, checklist, and blocker
requirements; behavior-changing fixes still require authoritative spec updates.
This is contributor policy. The proposed link check and required-check rules
are not installed or activated by this document.

## Coverage and merge order

Contributor policy; no new automatic merge gate is activated by this trial. Maintain
one PR section with these fields:

```text
Spec impact: update | existing-coverage | none
Canonical coverage: specs repository, exact merged commit, file and section
Affected guarantees: observable changes, or why behavior is unchanged
Evidence: tests/results with implementation and evidence revisions
Review order: specs merged before implementation, or existing coverage already merged
Remaining gaps: unknowns and unsupported claims
```

For update, amend the owning contract/validation, review and merge to amadou-6e/specs
main, then pin that merged commit before implementation merges. A linked PR is insufficient.
For existing-coverage, cite sections and explain conformance without a behavior change.
For none, provide concrete behavior-preserving justification and checks, without meaningless
spec diffs. Reviewers verify referenced repository, commit and merge status manually.

## Illustrative declarations

Update: a future Langflow resume input changes the supported interface. Update execution
contract and interface validation; cite mismatch checks and the merged specs revision.
The current saved node is fresh-only; API evidence does not prove Langflow resume UI.

Existing coverage: enforce missing-snapshot failure before reserving a turn. Cite execution
isolation lifecycle and linked validation; provide a synthetic response/ledger regression.
This example does not assert a new PR or test has been executed.

None: extract an internal event serializer while emitted fields, IDs, ordering and errors
stay unchanged. Cite traces contract and compare fixtures. If missing-value semantics or
IDs change, reclassify as update.

Check behavior, interfaces, defaults, identity/persistence, permissions and failures.
New results update experiment records and validation links, not requirements automatically.
Branch evidence supports review but does not prove merge or hosted readiness. Open issues
remain proposals; issue edits need separate approval. The validator has no semantic coverage
or PR merge-status enforcement. Future automation remains a proposal until tested and
separately activated; this document changes no workflows or repository settings.
