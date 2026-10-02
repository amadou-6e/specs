---
title: Agent execution interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Agent execution interfaces

> First-slice choices and open questions are triaged in
> [decision readiness](../design/decision-readiness.md). In particular, the
> three-attempt container recovery below remains a later target: first-slice
> container failure is terminal for its invocation. IF-08 deduplication,
> IF-10 manifest supersession, approval ownership, network scope and writable
> checkout protections are not established by these draft interfaces.

Agent execution is the provider-neutral boundary used by Langflow agent nodes.
It owns provider dispatch, session binding, Docker stage lifetime, workspace
mount choice and external access requests. The [interface map](../../README.md)
lists each contact. Provider-specific behavior remains in
[Codex](codex.md) and [Claude](claude.md).

## IF-05 — invoke a configured agent stage

- **Provider / consumer:** [Langflow integration](../../langflow-integration/contract/interfaces.md)
  requests an invocation; Agent execution validates and executes it.
- **Minimum command:** Laomedo run identity; graph revision, stage and new
  invocation identities; frozen provider, model, effort, prompt and skill refs;
  structured/text input and user/upstream file refs; explicit session choice;
  workspace mount choice; effective permission/grant ref and limits.
- **Rule:** one stage can be invoked repeatedly, with separate invocation
  records but its own container persisting until workflow completion. A stage
  may choose a local mounted workspace or isolated checkout. Stage containers
  are not shared, though an external Codex home mount may be shared by
  configuration. Session data persists outside containers.
- **Failure:** missing revision, incompatible resume binding, unavailable
  input/mount or unsupported requested protection fails before dispatch. A
  concurrent attempt to use the same session errors at execution time; a
  predictable conflict can be warned about before launch without blocking it.

## IF-04 — obtain exact skill bytes

Agent execution consumes [skill registry](../../skill-registry/contract/interfaces.md)
materialization for the frozen skill ref. The registry returns validated
content, dependency closure and hashes. A mutable catalog path alone is not
enough. The exact effective workspace and post-run state remain linked to
the invocation/session as in [shared contracts](../../../architecture/shared-contracts.md).

## IF-06 — report invocation outcome

Return the invocation identity, terminal or partial status, native session
identity if available, output and artifact refs, and error classification to
Langflow integration. An error identifies the affected invocation so Langflow
can block dependent stages while permitting independent branches under the
chosen end-on-error policy. Stop requests interrupt active agents promptly.

Container crashes have up to three automatic recovery attempts by default,
within the same invocation and native session. Each recovery sends the agent
a prompt to inspect existing state before repeating a potentially completed
action. After failed recovery attempts, report an invocation error. This
differs from a user-requested new run or selective rerun.

## IF-08 — emit agent telemetry

Send [run traces](../../run-traces/contract/interfaces.md) native provider
events with run, stage, invocation and session correlation. Retain partial
events on crash, denial or interruption; do not label an incomplete stream
complete. The event interface may expose a raw payload reference rather than
putting sensitive content into every projection.

## IF-10 — report produced outputs

Send [results and artifacts](../../results-artifacts/contract/interfaces.md)
known output refs with type, location, invocation identity and saved/published
state, including a GitHub PR ref after the agent creates or updates one. Do
not claim publication from a local diff or require artifacts to be copied into
the run directory.

## External access approval boundary

Tool integrations are enabled explicitly. An additional access request follows
run-scoped auto-approval. If auto-approval is disabled or denies the request,
escalate it to the user. Approval resumes the current invocation; denial and
optional user text return to the agent so it can try another approach. The
transport, grant identity and policy evaluation API remain to be designed.
This boundary is shared with chat-assisted actions; it is not a separate
PR-delivery subsystem.

The older [isolation draft](isolation.md) specifies read-only defaults and
dedicated private profiles. The newer [decision record](../../../architecture/subsystem-decision-record.md)
allows a mounted local workspace and potentially shared external Codex home.
Those policies conflict as written; this interface draft does not silently
relax the older contract. A reviewed permission/isolation decision is needed.

## Exchange payloads

The [schemas index](schemas/README.md) gives each exchange touching agent
execution its own approximate payload file: [IF-04](schemas/if-04-skill-materialization.md),
[IF-05](schemas/if-05-stage-invocation.md),
[IF-06](schemas/if-06-invocation-outcome.md),
[IF-08](schemas/if-08-agent-event.md), and
[IF-10](schemas/if-10-output-manifest.md). The files describe data shapes;
the behavior and failure rules above remain here.
