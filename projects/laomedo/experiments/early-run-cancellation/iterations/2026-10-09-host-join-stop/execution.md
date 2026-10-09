---
title: Host join and Stop continuation execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The earlier [failed attempt](../2026-10-09-host-join/results.md) remains
unchanged. The user authorized zero-model diagnosis, repairing the private
runner login copy, and continuing. The
[login diagnosis](https://github.com/amadou-6e/laomedo/blob/266536fefa856c02d2482445387b83289ad069d1/experiments/exp22/PHASE-G-LOGIN-DIAGNOSTIC.md)
found unauthorized/401 in the original native error details. The old runner
token returned 401 on the usage endpoint; the current host token returned 200
on the same endpoint from the same pinned Docker image and network. Replacing
only the private runner auth cache made that check return 200 with usage
allowed. No refresh was requested and the host cache bytes were unchanged.
This identifies the practical credential blocker, without establishing why
the old copy became invalid or preventing future divergence.

The [continuation amendment](https://github.com/amadou-6e/laomedo/blob/85ddbf998e5248a5acd9f6dd74ebc21b10171b80/experiments/exp22/PHASE-G-LIVE-PROTOCOL.md#authorized-continuation-after-login-repair-2026-10-09)
was committed before dispatch and reviewed by the same Claude session, which
cleared exactly one new turn from 7/12. The code and Phase E task were unchanged.
A new empty private state was used; no failed request was redispatched. The
credential-free Playground preflight passed before one real visible Send.
This page is retrospective evidence, not the protocol freeze.

The run used Langflow 1.12.3, a disposable private SQLite mount, the opt-in
loopback host bridge and non-split Codex CLI 0.159.2 profile. The native model
was `gpt-6-luna` at low effort. Langflow received only the bridge token, not the
runner API token or Codex login. No GitHub credential or write grant was used.
The agent's content-free credential read was denied, then a long native command
started. The browser clicked visible Stop before its 30-second sentinel write.
Native cancellation completed before the browser closed.

Afterward the bridge stopped, Langflow was recreated on the same SQLite mount,
and a fresh child reopened the exact host binding. One linked Langflow trace
matched the saved-flow UUID and reported graph-run ID in a span. The ledger
recorded `real_join_visible_stop_passed` at 8/12. There was no second submission.
Private state is `%LOCALAPPDATA%/Laomedo/exp22-phase-g-live-20261009-b/`.
