---
title: Early-run cancellation protocol record
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol record

This page retrospectively indexes the [Laomedo Phase D protocol frozen at `bda5a6b`](https://github.com/amadou-6e/laomedo/blob/bda5a6b9f4ac27a4f5be99fb4901496355d9907e/experiments/exp22/PHASE-D-LANGFLOW-PROTOCOL.md). This specs page was written after the turn and did not authorize or freeze it. The protocol required a credential-free installed-Langflow graph check with a fake runner, a no-model real-runner readiness check, an independent review, then at most one remaining submission under the approved four-turn ledger. A timeout counted.

The real case used a pinned five-node saved flow and a one-turn local Codex runner. The host signalled graph cancellation only after observing the native long-command start or after a 45-second fallback deadline. A pass required exact start/lookup/cancel route identity, native `interrupted`, terminal confirmed runner cancellation, exact-container absence, retained partial raw events and a delayed sentinel still absent. Failure paths required bounded cancellation, exact ownership cleanup and a private teardown record. No real GitHub credential or write was in scope.

The graph cancellation is not a visible Playground Stop. UI-to-real-agent composition and the complete durable Langflow invocation-to-runner trace join remain outside this protocol's pass claim.

The later [Phase E protocol](https://github.com/amadou-6e/laomedo/blob/35a7d3c3f5518e5479b18b9d78a2f67c9b9394ac/experiments/exp22/PHASE-E-UI-PROTOCOL.md) was separately committed and reviewed before a visible browser Stop test. It required a no-model fake-runner browser gate, an exact embedded-component-code check, one reserved submission under the user-extended 12-turn shared ledger, click-to-cancel-to-terminal chronology before browser disconnect, native interruption and exact cleanup. This retrospective index did not freeze that protocol. Its [separate iteration](iterations/2026-10-09-visible-stop/README.md) records the result.
