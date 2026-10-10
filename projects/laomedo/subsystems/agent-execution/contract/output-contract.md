---
title: Output Contract node and agent-side submission precheck
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Output Contract node and agent-side submission precheck

Source: [owner interview A08/A10-A13](../../../decisions/0006-release-packages.md).
These are target requirements, not an implemented component. Existing provider
and runner failure rules remain applicable.

## Component boundary and outcomes

Output Contract is its own configurable Langflow node after the Agent node,
distinct from the Skill Reference node. Users configure required output through
a form there. The downstream node validates a handed-off submission and emits
an accepted/rejected outcome that a conditional router can consume. Validation
rejection does not itself require throwing an execution error or re-running the
agent. Route choice belongs to the workflow.

Keep contract validity, reported task outcome, executor status and evidence
completeness separate. A well-formed report of task failure can pass the
contract; it goes to the graph's failure route, such as reviewer or
human-in-the-loop. Success may route to draft PR creation. Rejected output
can take a different correction/review route. Agent-reported failure does not
trigger the output-correction retry.

Do not present process exit zero as semantic success, or a submitted form as
contract-valid before validation. Unknown effects/usage remain unknown and
available run/invocation/trace references accompany the outcome.

## Precheck and correction

The agent can see the configured requirements and precheck its form in the
current session before handoff. Check errors return actionable feedback for
same-request self-correction. If the request ends without valid output, the
default is one additional continuation request in the same session, carrying
feedback; the user can configure that count. It must not restart the original
task from scratch or silently repeat an external write.

The downstream node remains the final contract evaluator. Its rejection is
routed by the graph, rather than overridden by an automatic internal rerun.
Whether a precheck continuation is still appropriate depends on submission
state, not on task failure. No unlimited correction loop is implied.

## Infrastructure recovery boundary

Automatic retries for node/infrastructure failures are a separate desired
mechanism. Their count, category, resume behavior and side-effect reconciliation
remain open. This contract does not turn a transport timeout into permission
to redispatch, change native session binding or lift deferred crash recovery.
Graph loops/new invocations and output correction retain distinct identities.

## Unresolved interfaces and required evidence

The form/schema representation, supported check kinds, requirement version
binding, precheck transport, rejection payload and conditional-port types need
design. No particular JSON schema, submission tool or validator dependency was
selected by the owner. Both evaluators must demonstrably apply the same pinned
requirements before claiming consistent precheck/final evaluation.

The [Langflow demonstration](../../work-graph/contract/application-execution.md#next-requested-demonstration-the-complete-langflow-graph)
must show valid success, valid task failure, rejected submission and precheck
correction through the actual imported graph. Existing Agent and Skill tests
alone are not evidence for this new component.
