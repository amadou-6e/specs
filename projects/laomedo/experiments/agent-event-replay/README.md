---
title: Agent-event replay experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent-event replay

[EXP-09](https://github.com/amadou-6e/laomedo/issues/39) tests the selected
first-slice [at-least-once IF-08 policy](../../decisions/0003-agent-event-replay.md)
on a bounded synthetic SQLite ingest/projection path. It does not test a
provider or production adapter. Read the [frozen protocol](protocol.md),
[source pins](sources.md), and [2026-10-04 attempt](iterations/2026-10-04/README.md).
