---
title: Orphan stage and grant lifetime experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Orphan stage and grant lifetime

[EXP-07](https://github.com/amadou-6e/laomedo/issues/37) tests the user's selected independent stage lease supervisor plus startup sweep after the fate-shared backend dies. The [protocol](protocol.md) uses a disposable HTTP external-write grant with independent expiry and a user-selected 60-second bound. The [2026-10-02 result](iterations/2026-10-02/results.md) passed for this synthetic mechanism. It does not validate every credential or production stage-launch path.
