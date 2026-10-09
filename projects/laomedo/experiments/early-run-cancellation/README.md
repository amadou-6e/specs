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

This trial records bounded [#22](https://github.com/amadou-6e/laomedo/issues/22) cancellation checks: an installed in-process Langflow graph stopped a real Codex turn; a visible Playground Stop interrupted a real active command; and a separate visible Stop cancelled one prepared run before native thread creation. Later no-model probes observed graph, flow and stage identities and exercised a persistent host bridge. An initial real bridge turn failed before Stop. After private-login repair, a [fresh continuation](iterations/2026-10-09-host-join-stop/results.md) composed visible real-agent Stop and a durable identity join across restart in the same bounded local run, at ledger 8/12. Executing-graph attestation and broader #93 outage/credential guarantees remain unverified. Read the [retrospective protocol index](protocol.md), [sources](sources.md), and [dated iterations](iterations/README.md). The target behavior remains in the [early-run contract](../../subsystems/agent-execution/contract/early-run-cancellation.md).
