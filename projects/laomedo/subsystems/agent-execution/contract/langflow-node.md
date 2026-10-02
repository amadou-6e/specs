---
title: Local Langflow Codex Agent node
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Local Langflow Codex Agent node

Proposed follow-up to the verified pilot. Implementation tracking:
[node contract #18](https://github.com/amadou-6e/laomedo/issues/18),
[fresh node #19](https://github.com/amadou-6e/laomedo/issues/19),
[resume/lifecycle #20](https://github.com/amadou-6e/laomedo/issues/20), and
[acceptance #21](https://github.com/amadou-6e/laomedo/issues/21).
This draft does not declare those issues complete or authorize model turns.

## Boundary and packaging

The operator installs `components/laomedo/codex_agent.py` and its category
`__init__.py` through `LANGFLOW_COMPONENTS_PATH`. Pin Langflow 1.12.3 and inspect
the installed component API. The palette exposes `LaomedoCodexAgent` with display
name Laomedo Codex Agent. Historical saved pilot flows retain their embedded
`LaomedoRunner`; no silent type rename or rewrite is required.

This is a custom execution component, not the built-in Agent's model or tool
interface. It calls the existing local runner; Langflow receives no Codex login,
private profile directory, native session mount, or Docker socket. Keep the
existing Docker permissions unchanged. Hosted authentication, provider parity,
AGENTVIZ and subset skill editing are out of scope.

## Inputs and operations

| Input | Contract |
| --- | --- |
| Task | Message or text; nonempty for fresh/resume |
| Operation | Explicit fresh, resume, status or cancel; fresh default |
| Skill ID/revision | Fresh runs require an immutable whole-skill SHA-256 revision; no latest fallback |
| Model/effort | Required for fresh/resume; runner validates actual provider support |
| Prior Run | Structured Data from a previous run; mandatory for resume/status/cancel |
| Prior Run JSON | Advanced manual/API alternative when no Data input is connected; malformed JSON fails before dispatch |
| Runner URL | Advanced setting; plain HTTP local loopback or host.docker.internal only; no embedded credentials |
| Timeout | Advanced HTTP timeout, 1 to 240 seconds; default 210 |

Resume uses the same run ID, native thread, requested model/effort and exact
completed post-run hash. Invalid or missing bindings fail before dispatch where
detectable locally, otherwise at the runner before a model turn. Never silently
start a new thread. Status/cancel use the existing run ID and submit no new model
turn. A fresh run ignores prior-run state and keeps an independent workspace.

## Outputs and failure behavior

Expose Answer as Message and Run Reference as Data. Multiple output evaluations
within one component build share one dispatch. Each new explicit graph build
can dispatch again; no automatic retries or durable request idempotency are
claimed. The run reference preserves run/thread IDs, status, post-run hash,
model/effort, exact skill revision and use-evidence, answer, artifact and raw-event
references, error category and cancel-request state when available.

Opaque artifact/trace references are not private path strings or transcript bodies.
Usage remains unknown where not measured; outer Langflow token totals do not
measure the Codex turn. Skill delivery remains offered unless native evidence
supports a more specific observation.

Fresh/resume runner failure raises a Langflow error carrying known run ID and
category; no failed run is exposed as a successful answer. Malformed responses
fail explicitly. Status/cancel may report nonterminal states without pretending
an answer was produced. An HTTP timeout or client stop does not prove that the
remote agent was cancelled, and automatic retry risks another model turn.

The existing synchronous start API does not return its new run ID before the
turn finishes. Therefore automatic cancellation of a newly started run from
Langflow UI Stop is not supported by this slice. Explicit cancellation with a
known run ID is supported and must retain partial evidence. Async start/early
run identity is separate follow-up work, not a hidden acceptance claim.
Track that limitation in [Laomedo #22](https://github.com/amadou-6e/laomedo/issues/22).

## Acceptance and evidence

- Palette discovery uses the documented installed component path on pinned runtime.
- An exported/imported flow retains input values, output types and component identity.
- Fresh execution returns answer plus queryable run reference, with observed tool
  call/result and exact skill revision recorded outside the flow export.
- Restart/resume through this node continues the same native thread from its exact
  snapshot; a fresh independent run does not inherit prior artifacts.
- Synthetic tests demonstrate single dispatch across both outputs, input rejection,
  resume binding checks, status/cancel routing and failure/malformed-response handling.
- Bounded model-backed acceptance records submitted turns, failures and unknowns;
  no new run is authorized solely by issue creation or this contract.

Link actual results from [execution validation](../validation.md), distinguishing
credential-free checks from model-backed observations. A pending or failed
acceptance check remains a gap. A follow-up issue does not waive an unmet guarantee.

Reference: [Langflow custom components](https://docs.langflow.org/components-custom-components),
inspected 2026-10-01 alongside installed 1.12.3; newer docs do not establish support
in the pinned runtime.
