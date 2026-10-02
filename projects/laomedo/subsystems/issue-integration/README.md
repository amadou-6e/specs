---
title: Issue integration
status: draft
kind: subsystem
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration

Owns issue identity and selection, GitHub issue/PR event context as applicable,
and publication of a user-reviewed follow-up issue. It supplies references to
the launch path; the executing agent reads current GitHub issue content and
checks related open PRs. This boundary does not own agent work or PR creation.

Consumers: [Langflow integration](../langflow-integration/README.md) and
[results and artifacts](../results-artifacts/README.md). External dependency:
GitHub. This is a proposed subsystem; no issue API implementation is evidenced
by this page.

Read the [contract](contract/README.md), [design](design/README.md) and
[validation](validation.md). Entry schema: those pages plus this overview
(1 each); focused contract/design pages (0..*).
