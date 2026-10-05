---
title: Timeout trace integration source pins
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- Laomedo base was EXP-65 merge `8b3087751b79266ab3c454fe2cdfa8e15f94b097`.
  #66 store implementation was `c4f506678de783f5be53bd7d12194c56a63bc7df`;
  protocol `2a2a1ad`, initial probe `6931275`, first observation `19f823d`,
  amendment `95c1121`, amended probe `a885197`, and amended direct
  observation/tests `076030c`. These were issue-branch sources at run time.
- The governing [proposed contract](../../subsystems/langflow-integration/contract/timeout-reconciliation.md)
  was specs PR #213 at `ec0485421cf7140ef747a0215b88180bc8816870`.
  Implementation against this unmerged draft was explicitly authorized; it
  was not an accepted contract at execution time.
- Pinned Langflow 1.12.3 image:
  `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`.
  The read-only status endpoint was `GET /api/v2/workflows?job_id=<id>`.
- The runner was EXP-10's disposable in-container synthetic HTTP fixture,
  not a Codex or other agent. Its journal supplied the delayed effect row.
