---
title: Post-timeout job-status experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Post-timeout job status

[Laomedo #65](https://github.com/amadou-6e/laomedo/issues/65) follows the
[EXP-10 timeout result](../long-call-timeout/README.md): can Langflow's v2 job
ID expose state after `408`, and does it account for a later external effect?
The [protocol](protocol.md) was frozen before a one-call run; a prospective
[amendment](protocol.md) allowed one separate diagnostic replication. The
[2026-10-05 result](iterations/2026-10-05/results.md) is a negative
first-slice observation, not a product trace or cancellation implementation.

Read [source pins](sources.md) and the [evidence manifest](iterations/2026-10-05/evidence/manifest.md)
before generalizing beyond the pinned Langflow image.
