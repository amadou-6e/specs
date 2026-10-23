---
title: Descriptive node errors
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-23
applies_to: [laomedo]
supersedes: null
related: []
---

# Descriptive node errors

Tracks [Laomedo #181](https://github.com/amadou-6e/laomedo/issues/181).
The [editable state design](../design/node-error-details.drawio) owns layout,
controls and transitions. This derived contract describes their semantics.

Laomedo node failures show a plain-language explanation, affected node and
operation, and recovery that matches available controls. A missing prior run
must not suggest an unavailable run picker. When a saved reference is visibly
present but the component reports it missing, distinguish that contradiction
without claiming an unverified loading cause.

Pre-component validation may only produce a flow-level failure. The flow error
panel must use the same explanation and diagnostics. A node is attributed only
when execution metadata identifies it or the graph contains exactly one node;
never guess a failing node from the requested graph endpoint. The generic Retry
button is hidden for the descriptive errors.

Every public validation code emitted by the shipped Agent components has an
explicit explanation. Future safe codes, including numeric segments, retain
their original value in diagnostics. Native notification history retains the
safe diagnostic code alongside the explanation; raw exception payloads are
not copied into that history by this presentation layer.

Preserve stable API codes, error categories and original execution receipts.
Expandable technical details show the code and only allowlisted identifiers.
Copying includes only those details; credentials, endpoint URLs, task text,
arbitrary payloads and stack traces are excluded. Report copy success only
when the browser confirms it; offer manual selection when copying fails.

Explain validation, lifecycle bindings, authentication, transport, model and
reasoning support, allowance and uncertain execution failures. Unknown codes
have a safe generic explanation without an invented cause. Unconfirmed remote
outcomes require checking existing runs before a new request, never a blind
retry. A routed failed runner result exposes details even when graph routing
itself succeeds; do not describe it as a successful agent answer.

## Verification boundary

Check code mappings, unknown fallback, safe diagnostics and original code
preservation with focused tests. Validate native node errors in an actual
Langflow graph, including explanation and expanded technical details. Tests
with fixtures do not establish real integration acceptance. Provider-backed
failure classes not exercised live must remain explicit coverage gaps.
