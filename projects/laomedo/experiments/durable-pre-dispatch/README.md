---
title: Durable pre-dispatch experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Durable pre-dispatch identity

[EXP-04](https://github.com/amadou-6e/laomedo/issues/34) tests a Laomedo SQLite launch-store prototype with a deterministic callback and six process-crash phases. See [protocol](protocol.md) and [2026-10-02 attempt](iterations/2026-10-02/README.md). The store persists run, trace, graph/component revisions and resolved config before callback dispatch. This does not yet prove the live Langflow adapter calls the store.
