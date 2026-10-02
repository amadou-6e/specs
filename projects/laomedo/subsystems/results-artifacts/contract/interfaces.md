---
title: Results and artifacts interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results and artifacts interfaces

Results combine three inputs by run identity. A missing input is recorded as
missing or incomplete, not fabricated from another source. Exact field names
and storage destinations remain open. See the [interface map](../../README.md).

## IF-09/IF-10/IF-11 — assemble a run result

| Provider | Minimum input | Result responsibility |
| --- | --- | --- |
| [Langflow integration](../../langflow-integration/contract/interfaces.md) (IF-09) | Run identity, exact launch configuration/graph revision, terminal or incomplete workflow status | Preserve what was requested and whether the workflow finished |
| [Agent execution](../../agent-execution/contract/interfaces.md) (IF-10) | Invocation identity, final/partial output refs, artifact type/location and known saved/published state, PR reference when produced | Inventory outputs without assuming they are co-located with run storage |
| [Run traces](../../run-traces/contract/interfaces.md) (IF-11) | Trace and digest refs, event completeness and correlation identity | Link inspection evidence without copying raw events into the summary |

The result exposed to the user carries status, a semi-structured summary,
trace/digest links, artifact inventory, and PR reference if known. A terminal
workflow may still have partial or unknown artifacts. An agent-created PR is
recorded as an external GitHub reference; this subsystem does not perform the
PR write or infer that a PR exists from a local diff.

## IF-12 — reviewed failure-to-issue proposal

For an unsuccessful run, expose an editable report of completed work, failure,
evidence and remaining work. A user selects, reviews and may edit a proposed
follow-up issue. Only then send that reviewed proposal and prior-run references
to [issue integration](../../issue-integration/contract/interfaces.md). If
publication fails, keep the draft's review state and report the failure.

## IF-13 — follow-up run context

When the user requests another run, give
[Langflow integration](../../langflow-integration/contract/interfaces.md) the
prior run link, existing PR reference if supplied, and the user's explicit
existing/new session choice. The next run gets its own run and trace identities
while retaining links to the PR and previous run.

Selected findings may be stored separately as durable project knowledge with
source/run links. This is optional and does not imply GitHub publication.
Artifact placement, ownership, retention and unsaved-output behavior await the
[later experiment](../../../architecture/user-traversal.md#boundaries-and-open-choices).
