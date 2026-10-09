---
title: Early-run cancellation experiment
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Early-run cancellation

This trial records bounded [#22](https://github.com/amadou-6e/laomedo/issues/22) cancellation checks: an installed in-process Langflow graph stopped a real Codex turn; a visible Playground Stop interrupted a real active command; and a separate visible Stop cancelled one prepared run before native thread creation. A later no-model server probe observed graph, flow and stage identities needed for a future trace join. These are distinct iterations, and none establishes a durable Langflow invocation-to-runner trace join. Read the [retrospective protocol index](protocol.md), [sources](sources.md), and [dated iterations](iterations/README.md). The target behavior remains in the [early-run contract](../../subsystems/agent-execution/contract/early-run-cancellation.md).
