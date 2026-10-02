---
title: OpenCode authenticated verification protocol
status: complete
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

Retrospective record of the 2026-10-02 verification, not a prospectively reviewed
protocol. Harnesses were prepared before their respective dispatches. Preserve
previous failures and obtain explicit additional turn budgets; no automatic retry.

Direct CLI: tools denied, exact marker response using the existing terminal login.
Isolated flow: native skill loading for two pinned bundles, forbidden controller
credential-path read, fixture read and marker write. Restart the runner and resume
the same native session. Finally, start a command worker with a delayed write,
request native abort while that worker is observed, and independently check that
the worker is absent and delayed file was not created. All outputs remain private
except sanitized evidence. Unknown usage and untested access routes remain unknown.
