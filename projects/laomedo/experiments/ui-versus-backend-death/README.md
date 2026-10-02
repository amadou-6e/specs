---
title: UI closure versus backend death experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# UI closure versus backend death

[EXP-06](https://github.com/amadou-6e/laomedo/issues/36) uses two synthetic runs through a pinned Langflow 1.12.3 server. Closing a client connection leaves the stage active; hard-killing the backend and restarting with a startup sweep marks its run terminal crashed. Read [protocol](protocol.md) and [attempt](iterations/2026-10-02/README.md). The synthetic stage runs inside the backend container, so orphan stage-container behavior is still EXP-07.
