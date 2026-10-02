---
title: Choose how a run resolves its saved configuration
status: template
kind: decision
owners: [laomedo-maintainers]
last_reviewed: YYYY-MM-DD
applies_to: [laomedo]
supersedes: null
related: []
---

# Choose how a run resolves its saved configuration

This is an illustrative template, **not** an adopted Laomedo decision. Replace
its example claims and links when copying it to a numbered entry.

## Status and source

Example status: proposed. Record when and where the choice was discussed, the
inspected specification or graph revisions, and whether notes are verbatim or
reconstructed. Name unavailable evidence rather than inventing it.

## Context and question

Example question: should a run use the latest configuration throughout its
execution, or resolve an exact version once at launch?

## Discussion trail

1. Initial proposal: keep a saved configuration selector.
2. Alternative considered: follow its moving latest revision during execution.
3. Example outcome: pin an exact resolved revision at launch, subject to review.

Separate what the user actually confirmed from the author's reconstruction.

## Decision and scope

State the precise choice, its owner and when it applies. Note exceptions and
what this record does *not* decide.

## Consequences and verification

Describe benefits, costs, compatibility effects and evidence needed before
calling the choice implemented. Link the owning architecture, subsystem
contracts and tests rather than repeating their detailed requirements.

## Open questions and supersession

List unresolved matters. If a later record changes this choice, link it and
update `supersedes`/status so readers have one current decision trail.
