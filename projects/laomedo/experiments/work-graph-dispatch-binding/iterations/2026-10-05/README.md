---
title: EXP-16 mock dispatch binding attempt
status: complete
kind: experiment-attempt
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Mock dispatch binding attempt

All 20 frozen cases matched the handwritten expected matrix against an installed Laomedo wheel. This is a **go for the bounded mock snapshot-to-run binding experiment** and a **no-go for claiming the real Langflow stage adapter safely launches work**. The mock constructed its own preflight and grant-field checks; it did not exercise production grant verification or native component revision attestation. EXP-03's failed native freeze and [#77](https://github.com/amadou-6e/laomedo/issues/77) remain explicit integration limits.

See [execution](execution.md), [results](results.md), and [evidence manifest](evidence/manifest.md).
