---
title: Pinned skill materialization sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [EXP-08 #38](https://github.com/amadou-6e/laomedo/issues/38) and
  [agent-execution readiness E04](../../subsystems/agent-execution/design/decision-readiness.md).
  The issue's EXP-09 dependency is inconsistent with the user's explicit
  independent-track direction and the skill-specific scope; it was not used
  as a technical prerequisite.
- [Skill registry](../../subsystems/skill-registry/contract/README.md)
  owns immutable revisions. [Agent execution](../../subsystems/agent-execution/contract/interfaces.md)
  owns effective delivery and provider evidence.
- [Laomedo `839f2bb`](https://github.com/amadou-6e/laomedo/commit/839f2bbaa41f4bf0d3801f3f2e34796a6e57314b)
  contains the synthetic probe, tests and sanitized observation. At
  submission it is a published issue branch, not a merged product capability.
- [Laomedo #9](https://github.com/amadou-6e/laomedo/issues/9) and
  [#25](https://github.com/amadou-6e/laomedo/issues/25) own production
  materialization and the Langflow Skill node; this experiment is not a
  second registry or a claim those tickets are complete.
