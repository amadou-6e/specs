---
title: Langflow graph and component freeze experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow graph and component freeze

[EXP-03](https://github.com/amadou-6e/laomedo/issues/33) tests whether a saved-flow edit changes an already running graph. The [protocol](protocol.md) uses pinned Langflow 1.12.3 and two deterministic custom components. The [attempt](iterations/2026-10-02/README.md) observed behavioral non-uptake of the edit, but no native per-run component-code attestation. This is bounded local evidence, not a general freeze guarantee.
