---
title: Agent handoff evidence sources
status: complete
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- Implementation [ac204ab](https://github.com/amadou-6e/laomedo/tree/ac204ab): harness,
  runtime, selected importer and generated graph definitions. This revision records
  the delivered tree; the live harness ran before this commit. Its later added
  outside-Git output guard did not consume or repeat either observed turn.
- [Sanitized live evidence](https://github.com/amadou-6e/laomedo/blob/ac204ab/examples/agent-handoffs/live-evidence.json).
- [Native-controller graph tests](https://github.com/amadou-6e/laomedo/blob/ac204ab/tests/langflow/test_bounded_controller.py).
- [Artifact/restart tests](https://github.com/amadou-6e/laomedo/blob/ac204ab/tests/test_artifact_handoffs.py).
- Langflow 1.12.3 image digest: `sha256:34055a07d446de51760e28dab6332e22624e5f48dca611567779992fc32c5ec0`.
- Existing Codex CLI 0.159.2 Docker profile and pinned permission configuration;
  no image/auth/config change for this acceptance.
- Resume-only follow-up [9a46a50](https://github.com/amadou-6e/laomedo/tree/9a46a50):
  explicit pinned skill-set mismatch rejection and 55 passing host checks; no new
  model turns. Earlier live evidence and pinned runtime checks retain ac204ab.

Private authorization linkage, run records, raw events and full graph output remain
outside Git. They are not published reproducibility artifacts.
