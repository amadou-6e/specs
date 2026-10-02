---
title: Langflow integration interfaces
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Langflow integration interfaces

The [interface map](../../README.md) identifies direct Laomedo contacts. The
embedded Langflow runtime is an external dependency: its actual hooks and
durability must be verified before this becomes an implementable API. A run is
distinct from a stage invocation and from a native agent session.

## Run entry and definition resolution — H1-H4

- **Consumes IF-01** from [issue integration](../../issue-integration/contract/interfaces.md):
  issue/repository reference and event context, where applicable.
- **Consumes IF-02** from [prompt and skill library](../../prompt-skill-library/contract/interfaces.md):
  exact prompt/skill revision references. A saved workflow configuration uses
  `latest` by default or a user-pinned revision; all selectors are resolved at
  launch and frozen for the run and recovery.
- **Offers to Langflow:** selected graph definition/revision or one-agent
  graph, resolved stage configurations, user files and event/direct inputs,
  Laomedo run identity and correlation context.
- **Failure:** an unavailable selected revision, invalid stage configuration
  or inaccessible required input prevents dispatch and yields a visible
  launch error. It must not silently substitute another revision.

## IF-05/IF-06 — agent-node invocation and return

Langflow sequencing invokes [agent execution](../../agent-execution/contract/interfaces.md)
through this adapter. The command carries run, graph revision, configured
stage and invocation identities; frozen provider/model/effort/prompt/skill
references; user and upstream file/artifact refs; session choice; and
workspace choice. A loop creates a new invocation identity for the same
stage. The outcome returns that invocation identity, status, output refs and
error classification to Langflow. The Langflow-specific mechanism for all
component types to exchange artifact refs is open.

Predictable simultaneous use of one session is a pre-launch warning, not a
launch block. Actual concurrent use errors at invocation. An errored
invocation blocks dependent stages; independent branches continue unless
end-on-error was selected. Immediate Stop interrupts active agents.

## IF-07 — workflow events to run traces

Send workflow start, stage/invocation lifecycle, completion, error and
interruption events to [run traces](../../run-traces/contract/interfaces.md).
Each event carries run, graph revision, stage and invocation correlation where
applicable, plus source event identity when Langflow provides it. Missing
native IDs are recorded as unknown rather than fabricated.

## IF-09 — run context to results and artifacts

At launch, supply [results and artifacts](../../results-artifacts/contract/interfaces.md)
the exact resolved configuration reference, run identity and graph revision.
At terminal state, supply workflow outcome and end time or an explicit
incomplete/unknown state. Results combines this context with IF-10 and IF-11;
it cannot reconstruct the exact launch selection solely from tool events.

## IF-13 — follow-up run context

Consume a user-requested follow-up from results: prior run identity, existing
PR reference when supplied, and explicit existing/new session selection.
Create a new linked run with separate invocation identities and trace. The
agent receives a hint that PR comments exist and fetches them itself. A
selective stage rerun using prior upstream outputs is desired but not part of
this interface until Langflow feasibility is verified.

## Ownership gap

Langflow owns graph sequencing, while Laomedo must keep enough run identity
and trace linkage for reconnection after the UI closes. The authoritative
persisted workflow state and its recovery protocol are unresolved. The
[existing shared contract](../../../architecture/shared-contracts.md) still
uses broader runner-ownership wording; this draft does not silently replace it.
