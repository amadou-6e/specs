---
title: Visible Playground host-bridge seam execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The [Laomedo design draft at `6c6bf37`](https://github.com/amadou-6e/laomedo/blob/6c6bf37558fbafb2697f6e6c279a19cdcad49a5c/experiments/exp22/PHASE-G-JOIN-DESIGN.md)
proposes a lazy host reservation when the custom component first calls a
bridge. Claude rejected a pre-graph reservation for visible Playground Send,
then accepted the revised route in a focused recheck. That recheck read only
the design document. The executable seam probe was not a separately frozen
protocol; its first review narrowed several overclaims, and the final probe
was rerun after adding browser-click-to-lookup-to-cancel ordering.

The final run used the pinned Langflow 1.12.3 image, the five-node saved flow,
a disposable auto-login server, and a loopback fake host bridge. Browser
automation clicked Send and Stop with a synthetic task. The fake called
`WorkflowRunStore` to persist a run, invocation, request digest, synthetic
runner binding and cancel receipt. It did not contact a runner or model. A
host-side self-test replayed the same request body and a changed one against
the fake. Only the sanitized summary and teardown conclusions are published.

The private test state is
`%LOCALAPPDATA%/Laomedo/exp22-phase-g-seam-20261009-c/`. It contains a
disposable bridge token, browser profiles and SQLite data and stays outside
Git. The result does not change the active Langflow or runner configuration.
