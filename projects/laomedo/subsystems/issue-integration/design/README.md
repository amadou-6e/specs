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
Design container: README.md (1), focused mechanism pages (0..*).

The [decision-readiness ledger](decision-readiness.md) records the open
GitHub-read, publication and event-policy choices separately from the draft
interface shapes.
