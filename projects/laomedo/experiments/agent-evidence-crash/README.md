---
title: Agent evidence crash experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent evidence crash windows

[EXP-05](https://github.com/amadou-6e/laomedo/issues/35) probes which
synthetic invocation identities and events survive seven process-kill/control
boundaries after the [EXP-04](../durable-pre-dispatch/README.md) run reservation.
See the [retrospective protocol](protocol.md), [source pins](sources.md), and
[2026-10-03 attempt](iterations/2026-10-03/README.md).

The experiment does not call a model or real provider, resume an interrupted
agent, or establish an IF-08 replay/deduplication policy. Those remain separate
from the observed persistence result.
