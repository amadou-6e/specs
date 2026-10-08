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

The [2026-10-08 integrated attempt](iterations/2026-10-08/README.md) used a real Codex turn and a fake GitHub transport. It observed independent service survival and revocation within 60 seconds, but service-attributed cleanup and agent-originated post-revocation denial remain inconclusive. It is not a full #93 pass.
