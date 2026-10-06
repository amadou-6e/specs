---
title: Post-timeout job-status source pins
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- Governing [Langflow Q11/E03](../../subsystems/langflow-integration/design/decision-readiness.md)
  and [EXP-10 evidence](../long-call-timeout/README.md) were at specs merge
  `92bcdcdc189809920bbf905fa88fcc4b841f531b` before this follow-up.
- Laomedo base was `99ff3801faa821f731158a152f7a5129dfd62368`;
  protocol `c5f2f68`, initial probe `5a44f98`, amendment `1c6790a`,
  first observation `95e991b`, diagnostic probe `3f1e947`, and direct
  observation/tests `3543a66`. These are issue-branch sources, not merged
  product features at experiment time.
- Pinned Langflow 1.12.3 image:
  `langflowai/langflow@sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`.
  Its installed `get_workflow_status` handler can return HTTP 500 for
  `JOB_FAILED` or an internal status error; the amended observation captured
  the former. The documented read-only endpoint was
  `GET /api/v2/workflows?job_id=<id>`.
- The runner was EXP-10's pinned in-container synthetic HTTP fixture, not a
  native agent. Its delayed effect and response are separately journaled.
