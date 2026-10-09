---
title: Early-run cancellation sources
status: draft
kind: experiment-sources
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Sources

- [Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22): early identity, cancellation races and partial evidence.
- [Early-run cancellation contract](../../subsystems/agent-execution/contract/early-run-cancellation.md): target behavior and limits.
- [Phase B direct-runner result](https://github.com/amadou-6e/laomedo/blob/dc803a967b630bf8489a46c849e5af8f7f89eb43/experiments/exp22/PHASE-B-RESULTS.md): native interruption before this graph test.
- [EXP-94 synthetic visible Stop result](https://github.com/amadou-6e/laomedo/blob/7d37ff6/experiments/exp94/RESULTS.md): UI propagation to a fake runner, not a real Codex turn.
- [Phase D input freeze](https://github.com/amadou-6e/laomedo/blob/bda5a6b9f4ac27a4f5be99fb4901496355d9907e/experiments/exp22/PHASE-D-LANGFLOW-PROTOCOL.md) and [published result](https://github.com/amadou-6e/laomedo/blob/a0a25d304a18466e3f1446cbd10e317a303e3525/experiments/exp22/PHASE-D-RESULTS.md).
- [Phase E visible Stop protocol](https://github.com/amadou-6e/laomedo/blob/35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac/experiments/exp22/PHASE-E-UI-PROTOCOL.md), [no-model gate](https://github.com/amadou-6e/laomedo/blob/35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac/experiments/exp22/PHASE-E-PREFLIGHT.md), and [published bounded result](https://github.com/amadou-6e/laomedo/blob/7460da39ee4d2922469e04895adf4d56de32615c/experiments/exp22/PHASE-E-RESULTS.md).
- [Phase F prepared-state protocol](https://github.com/amadou-6e/laomedo/blob/0b3053f2029fd754eb2e9abb2f720be397ab97e3/experiments/exp22/PHASE-F-PRETHREAD-PROTOCOL.md), [no-model setup](https://github.com/amadou-6e/laomedo/blob/0b3053f2029fd754eb2e9abb2f720be397ab97e3/experiments/exp22/PHASE-F-PREFLIGHT.md), and [published bounded result](https://github.com/amadou-6e/laomedo/blob/6d9dbc8076bf7e41b64c55cfb662f07db6ee2fa9/experiments/exp22/PHASE-F-RESULTS.md).
- [Phase G identity protocol](https://github.com/amadou-6e/laomedo/blob/e52194a/experiments/exp22/PHASE-G-CORRELATION-PROTOCOL.md) and [zero-model installed-server result](https://github.com/amadou-6e/laomedo/blob/4f12370/experiments/exp22/PHASE-G-IDENTITY-RESULTS.md): graph/flow/stage identity observation only, not a durable runner join.
- [Phase G lazy-bridge design](https://github.com/amadou-6e/laomedo/blob/6c6bf37558fbafb2697f6e6c279a19cdcad49a5c/experiments/exp22/PHASE-G-JOIN-DESIGN.md) and [no-model Playground seam result](https://github.com/amadou-6e/laomedo/blob/6c6bf37558fbafb2697f6e6c279a19cdcad49a5c/experiments/exp22/PHASE-G-SEAM-RESULTS.md): fake host binding and Stop routing only, with no runner POST or restart.
- [Phase G one-turn protocol frozen at `aa12af6`](https://github.com/amadou-6e/laomedo/blob/aa12af6cd6389dc4fdf81528772fdc6e58d4ef1d/experiments/exp22/PHASE-G-LIVE-PROTOCOL.md), [no-model preflight](https://github.com/amadou-6e/laomedo/blob/aa12af6cd6389dc4fdf81528772fdc6e58d4ef1d/experiments/exp22/PHASE-G-LIVE-PREFLIGHT.md), and [bounded real-turn result](https://github.com/amadou-6e/laomedo/blob/74a2c13f37d8bb3463aff990aca76c06e7504d33/experiments/exp22/PHASE-G-LIVE-RESULTS.md): exact identity join across restart, but the native turn failed before visible Stop.
