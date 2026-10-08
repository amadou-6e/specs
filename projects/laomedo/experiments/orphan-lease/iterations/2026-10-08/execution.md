---
title: Integrated Codex and orphan lease execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-08
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The original [Phase C protocol](https://github.com/amadou-6e/laomedo/blob/fca851a/experiments/exp22/PHASE-C-PROTOCOL.md) was committed before the amendments. The first turn used the amended [protocol](https://github.com/amadou-6e/laomedo/blob/2dcb19b/experiments/exp22/PHASE-C-PROTOCOL.md) and [file bridge](https://github.com/amadou-6e/laomedo/blob/2dcb19b/experiments/exp22/PHASE-C-FILE-BRIDGE.md) at `2dcb19b`; the second used those files at [protocol `e054a98`](https://github.com/amadou-6e/laomedo/blob/e054a98/experiments/exp22/PHASE-C-PROTOCOL.md) and [bridge `e054a98`](https://github.com/amadou-6e/laomedo/blob/e054a98/experiments/exp22/PHASE-C-FILE-BRIDGE.md). The no-model file bridge and lease preflights passed before the two model submissions. The user approved reuse of the current Codex subscription login in the non-split, single-user runner profile and a new four-turn cap. The profile was mounted in the agent container. A content-free agent-originated read-denial check preceded the task in each turn. No real GitHub credential or provider write was used.

At Laomedo `2dcb19b`, the first turn created an early run ID, made one fake mediated update, entered a long command, and was cancelled by the run ID. At `e054a98`, the second turn started an agent command before the runner's Windows process tree was killed. An independently started host process retained the lease and fake mediator. Another run held a separate grant. The private shared ledger records exactly two submitted turns out of four. The implementation and private `pins.json` files record the model, effort, image, skill, task, prompt and source identities. The two raw traces and credential state are retained outside Git.
