---
title: Output Contract v1 form, precheck and routing
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Output Contract v1 form, precheck and routing

Engineering proposal for [Laomedo #135](https://github.com/amadou-6e/laomedo/issues/135), [#136](https://github.com/amadou-6e/laomedo/issues/136) and [#137](https://github.com/amadou-6e/laomedo/issues/137), tracked in [specs #338](https://github.com/amadou-6e/specs/issues/338). The [owning contract](../contract/output-contract.md) and [decision 0006](../../../decisions/0006-release-packages.md) remain authoritative for product intent. This page fixes a minimal implementation interface; no runtime acceptance is asserted.

## Declarative form and exact revision

Users configure a JSON form in the Output Contract node. It is a bounded declarative form, not arbitrary JSON Schema or executable validation code:

```json
{
  "schema_version": 1,
  "fields": [
    {"name": "task_outcome", "type": "string", "required": true,
     "checks": {"enum": ["success", "failure"]}},
    {"name": "report", "type": "string", "required": true,
     "checks": {"nonempty": true, "max_length": 4096}}
  ]
}
```

The root submission is an object. Fields have unique names, a declared type and optional `required` (false by default) and `checks` (empty by default). Supported types: `string`, `integer`, `number`, `boolean`, `object`, `array`. Boolean values do not satisfy integer/number checks; numbers must be finite. Present null does not satisfy these types. Missing optional fields are allowed; extra submission fields are allowed. `task_outcome` is reserved: if declared, its type must be `string` and its enum must be exactly `success` and `failure`; refuse a conflicting declaration. Omitting it is allowed but cannot yield a reported success. Unknown requirement keys, duplicate fields, malformed or incompatible checks and invalid limits refuse before dispatch.

Checks: `nonempty` for string/array/object, scalar `enum`, numeric `minimum`/`maximum`, and string/array `min_length`/`max_length`. Length means characters for strings and items for arrays. No shell, network, file-path or executable test checks are supported in v1. Maximum 64 fields, 64 KiB requirements, 256 KiB submission and 64 reported errors. Limits apply before evaluation; untrusted values are never included in errors.

The revision is `sha256:` followed by the SHA-256 of validated requirements encoded as UTF-8 canonical JSON: sorted object keys, compact separators, unescaped Unicode, no nonfinite numbers. Field order remains significant. Requirements travel as Data containing the specification and revision; recompute and refuse a mismatch. A shared `laomedo.output_contract` evaluator serves native precheck and downstream validation. Installation of that package is explicit; no divergent embedded evaluator is claimed.

## Agent submission and routable validation

The Codex node adds a `submission` Data output while retaining existing `answer` and `run` ports. Its envelope has `schema_version: "laomedo.agent-submission.v1"`, `submission` (parsed report object or null), `task_outcome` (`success | failure | unknown`), `executor_status`, `evidence_complete` (boolean or `unknown`), `run_reference`, nullable `requirements_revision`, `precheck` evidence (`installed` and observed `call_count`, or unknown), available answer/trace references and a stable `error_category` or null. The envelope task outcome is derived only from the reserved `submission.task_outcome` value; absent or invalid values become `unknown`. Routing uses that envelope value. A noncompleted executor clamps an apparent reported success to `unknown`; downstream validation checks this projection and rejects a contradictory envelope. Process exit zero never implies task success. Runtime uncertainty cannot retain an apparent task success from partial output. Preserve unknown usage, effects and missing evidence as unknown, and never fabricate a PR reference.

Input errors before dispatch can still refuse. Known runtime failures are routable on the new port. Existing `answer`/`run` error behavior remains compatible; consuming several ports in one build must not dispatch twice.

Output Contract has `requirements` and `validation` Data outputs. A requirements-only instance connects to the agent's precheck input; a separate downstream instance with the same pinned form evaluates the handed-off envelope with the same pinned revision. Validation contains `accepted | rejected`, `requirements_revision`, bounded `errors` (stable code and field path only), and the original submission/outcome/reference metadata. Two instances avoid a requirements-to-agent-to-validator cycle in Langflow's DAG. Compare the envelope requirements revision against the downstream form: a null/unreported revision rejects with `requirements_unbound`, and a different revision rejects with `requirements_revision_mismatch`. An installed precheck is not a claim that it was called. Invalid form configuration is a build error; an invalid submission is a rejection outcome, not an exception. A valid task-failure form can be accepted. Runtime interruption retains partial evidence and is never eligible for publication, irrespective of form validity.

Routing is explicit: accepted form plus reported task success, completed executor and `evidence_complete: true` goes to the success destination; accepted task failure goes to reviewer/HITL; rejected form goes to correction/review; noncompleted/unknown execution or false/unknown evidence completeness goes to recovery/review. These routes do not authorize external writes by themselves. The demo publisher is explicitly simulated.

## Native precheck and bounded continuation

For a fresh thread, install the pinned requirements as a native dynamic tool named `laomedo_output_precheck`. The controller handles the native `item/tool/call` request, runs the shared evaluator and returns only the revision, accepted/rejected result and bounded path/code errors. The agent can call it and self-correct within the same submitted request. Supplying requirements in a prompt alone does not prove an executable precheck. Native dynamic-tool support is a feasibility item to verify against pinned Codex 0.159.2 with synthetic protocol tests. Without a successfully bound tool, mark the revision unbound and the installation evidence false/unknown; do not hide this downstream.

If a completed request ends with invalid output, the configurable default permits one additional continuation request in the same native thread, with validation feedback and the original pinned requirements. Count that request in the existing model-turn ledger and preserve the campaign cap. Do not resubmit the original task. Never continue merely because the agent reports task failure. No continuation on transport uncertainty, runtime interruption, outstanding commands or uncertain external effects. The controller permits continuation only when the run held no external-write capability and has no effect receipts; otherwise return the invalid output for downstream routing instead of repeating a write. An absence of observed receipts does not establish absence of write capability. Infrastructure/crash retries remain deferred.

The final downstream evaluation remains authoritative even when precheck accepted an earlier submission. Requirements mismatch is refused. Tests must distinguish same-request precheck calls, additional submitted continuations and downstream rejection without automatic rerun.

## Verification gate

Credential-free tests must establish shared evaluator/revision parity, accepted success and accepted task failure, bounded rejection, no value echo, in-request feedback, one same-thread continuation, exhausted correction and runtime interruption with partial evidence. Legacy saved flow ports must remain buildable.

The committed demo flow must be imported into pinned Langflow 1.12.3 and all six fixture paths executed through its graph engine. Issue ingestion uses a frozen fixture identity/body, no ambient host `gh` login. Record machine-written sanitized outcomes and hashes over committed fixture/evidence bytes; distinguish simulated publication from a real PR. Standalone Laomedo UI, live Codex calls and real GitHub publication are outside this gate.

## Downstream form discovery and integrated routes

For pinned Langflow 1.12.3, the Codex component uses its native vertex/graph
metadata during request preparation to locate one direct Submission-to-Agent
Submission connection to LaomedoOutputContract. It reads and validates the
static Output Form without building the downstream component. Freeze a deep
copy on the agent invocation before any HTTP dispatch. Final validation compares
the frozen pin with the downstream form. A later edit rejects, never changes the
agent's expectations. Dynamic form-input connections, multiple downstream
contracts, multiple agent sources and conflicting explicit requirements refuse.
No contract leaves existing no-precheck operation unchanged. Legacy graphs with
an explicit requirements connection retain their original final drift rejection;
integrated routes additionally require discovery and equality of both pins.

Integrated routing reads a retained copy of the connected agent adapter's
submission envelope and verifies equality with the delivered Data. The adapter
builds its executor metadata from the runner response, separately from parsed
model output. A fabricated Data envelope is not accepted as execution evidence.
There is no new cryptographic attestation or custom-code security boundary.

Use native grouped outputs and stop inactive branches. Preserve the existing
{route, validation} envelope so existing destinations and Accepted Validation
continue to work. Legacy requirements/validation outputs remain available on the separate
LaomedoOutputContractLegacy component, but
are not themselves conditional routes; connecting those is explicit fan-out.
The caller must not interpret such a diagnostic output as another authorization.
Keep the historical EXP-139 export intact. A separately named simplified export
and credential-free native/imported tests own evidence for the new behavior.

Compatibility details: an older graph with no explicit requirements wire but
with a directly downstream contract now receives automatic precheck requirements,
even when it uses only Validation Outcome. This intentionally changes that
request: the existing configured continuation policy applies within its turn
ledger. Legacy flows with an explicit requirements wire retain their pin.

Integrated discovery requires exact native types LaomedoCodexAgent and
LaomedoOutputContract. Renamed/copied custom components and OpenCode are not
supported for automatic binding; missing integrated provenance fails closed.
The new LaomedoOutputContract exposes only the four route ports. Current
legacy examples use LaomedoOutputContractLegacy for Requirements/Validation;
existing saved flows retain their embedded original class code and edges.
Do not automatically replace those legacy instances with the new class.
The native editor reconstructs output metadata from code and does not honor
the hidden-output approach tested locally. Separate classes avoid silent
edge loss and keep the integrated node free of compatibility ports.
