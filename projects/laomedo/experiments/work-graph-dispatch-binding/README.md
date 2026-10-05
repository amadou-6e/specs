---
title: Work Graph mock dispatch binding experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph mock dispatch binding

[EXP-16 #46](https://github.com/amadou-6e/laomedo/issues/46) asks whether a selected immutable work and graph snapshot can become a frozen run input without bypassing blockers, freshness or a grant. This is a credential-free mock-runner experiment. It does not launch a Codex agent, mutate GitHub, or establish the real Langflow adapter's component identity. [#77](https://github.com/amadou-6e/laomedo/issues/77) owns that real-adapter refusal.

The [bounded installed-wheel attempt](iterations/2026-10-05/README.md) matched all 20 frozen cases. It supports mock binding only and leaves real-adapter launch at no-go until its separate gates pass. Read the [prospective protocol](protocol.md), [sources](sources.md), and [attempt index](iterations/README.md).
