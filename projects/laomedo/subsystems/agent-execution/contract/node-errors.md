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

## Runner diagnostic observations

For Agent dispatch and submission requests handled by the graph adapter's runner
HTTP boundary, including its run-status lookups, Technical details and the
existing copy action expose the observed HTTP status and a fixed failure stage.
Independent Stop/cancellation, model-catalogue and activity-polling transports
are outside this extension and retain their existing error contracts.
Where the runner supplies
them, also expose a diagnostic UUID, fixed failure kind, bounded numeric OS errno
and safe original runner code. The UUID correlates the displayed error with the
host diagnostic log; it is neither a run ID nor authority to access a run. Do not
invent a host correlation UUID when an older or external server supplies none.

An optional `runner_diagnostics` envelope on a failed runner response carries
these observations without changing existing status or error fields. Both
structured graph outcomes and exception-rendered failures preserve the admitted
fields. The receiving HTTP status is authoritative over a claimed envelope
status. Each boundary independently admits fields and rejects arbitrary keys,
free-form text, URLs, paths, credentials, task contents and stack traces. OS errno
is an observation, not an arbitrary exception message; explain only recognized
values as interpretations of the reported OS code, not a verified root cause or proof that no work ran. Distinguish unknown causes honestly.

The host log uses the same diagnostic UUID and safe observations even if a run
record does not exist. Expected request-lookup misses during cancellation polling
must not flood warning logs. An execution failure must not be labelled proof of
pre-dispatch refusal. For HTTP 5xx without a new run identity, preserve uncertain
execution outcome and retain a safe reported code as diagnostic context; a code
alone cannot prove that no work started. Do not automatically retry.

This extension tracks [Laomedo #289](https://github.com/amadou-6e/laomedo/issues/289)
and [specs #428](https://github.com/amadou-6e/specs/issues/428).

## Verification boundary

Check code mappings, unknown fallback, safe diagnostics and original code
preservation with focused tests. Validate native node errors in an actual
Langflow graph, including explanation and expanded technical details. Tests
with fixtures do not establish real integration acceptance. Provider-backed
failure classes not exercised live must remain explicit coverage gaps.

Check no-run HTTP failures through transport, graph output, expanded details and
copy projection, matching the host diagnostic UUID. Check malformed/absent
envelopes, 5xx uncertainty and private-field rejection. A rendered authentication
failure does not establish provider execution or all OS-error cases.
