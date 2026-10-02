---
title: Issue integration interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration interfaces

These are proposed boundaries from the [interface map](../../README.md), not
deployed endpoints. A reference identifies a GitHub resource without asserting
that its text was frozen at selection time.

## IF-01 — issue context for run setup

- **Provider / consumer:** Issue integration →
  [Langflow integration](../../langflow-integration/contract/interfaces.md).
- **Trigger:** a user selects an issue, or an enabled GitHub issue/PR event
  selects a saved run configuration.
- **Minimum handoff:** repository identity, issue identity, event identity and
  type if event-triggered, and a PR reference only when the user supplied one.
  The launch layer adds its own run identity and version selection.
- **Rule:** the agent retrieves current issue content and checks open PRs while
  executing. A related open PR does not silently become the target PR. Missing
  or inaccessible GitHub content remains an error/unknown, not an empty issue.
- **Open:** event deduplication, GitHub authorization binding and whether the
  issue reference is revalidated before dispatch.

## IF-12 — reviewed follow-up issue publication

- **Provider / consumer:** [Results and artifacts](../../results-artifacts/contract/interfaces.md)
  → Issue integration; Issue integration then writes to GitHub.
- **Trigger:** user reviews and edits a failure-to-issue draft and requests
  publication.
- **Minimum handoff:** target repository, reviewed title/body, prior run and
  trace/artifact references, and the user's publication decision.
- **Rule:** an unsuccessful run alone does not publish an issue. A successful
  write returns the new GitHub issue reference; a failed write retains the
  reviewed draft and reports the failure without claiming publication.
- **Open:** duplicate-write detection, repository permissions and exact draft
  retention policy.

GitHub PR creation remains an [agent-execution](../../agent-execution/README.md)
activity. This subsystem may surface issue and PR references for selection but
does not own a PR-delivery workflow.
