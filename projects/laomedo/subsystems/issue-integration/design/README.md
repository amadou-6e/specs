---
title: Issue integration design
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration design

The candidate design separates issue reference selection from the agent's live
GitHub read. Event adapters may normalize GitHub issue/PR events into the run
entry path; failed Actions workflows also enter that path but do not require
an issue. The publication path consumes only a reviewed follow-up draft.

No transport, webhook deduplication strategy, credential store or retry policy
is selected. Observable behavior belongs to [interfaces](../contract/interfaces.md).
The [decision-readiness triage](decision-readiness.md) separates first-slice
contract candidates from choices, research, experiments and deferred event work;
it is not an accepted mechanism.
Design container: README.md (1), focused mechanism pages (0..*).
