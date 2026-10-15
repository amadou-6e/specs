---
title: Graph-wide agent observability feasibility
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-15
applies_to: [laomedo]
supersedes: null
related: []
---

# Graph-wide agent observability feasibility

The user selected a graph-wide Agents tab with a shared Gantt time axis, multiple
turns, subagents, thread messages, tool calls and usage/cost over time. The
original Laomedo Codex Agent remains the execution component; a PR node must not
introduce a new PR-specific agent. The user explicitly selected removal of the
earlier adapter from the product on 2026-10-15.

## Feasibility result

Conditional go for native-event/OTLP correlation, not product acceptance. Docker
was unavailable, so the original 0.159.2 runner could not execute. A separately
identified real host App Server at 0.162.0-alpha.17.2 performed exactly three
top-level turns: completed, completed, interrupted. There was one real read-only
command with output and exit code 0. No subagent or GitHub write was requested.

The probe observed user/assistant items, message deltas, three token updates,
14 OTLP batches and one tool-call identity shared by the native and OTLP feeds.
Analysis found 1,529 timed spans and 1,478 parent IDs. These are mostly internal
runtime spans, not 1,529 agent actions. OTel logs used the `event.timestamp`
attribute (26 manually observed in private receipts; not counted in the published
summary) while the protobuf log timestamp was absent; ingestion
must distinguish source attributes, span clocks and receipt clocks.

The ephemeral thread refused `thread/read(includeTurns=true)`. The native stream
had already captured the messages; no further model turn or retry was made.
Persist events as they arrive rather than assuming post-run history is available.
No monetary cost attribute was observed in log attributes; span attributes were
not searched for cost. Missing amounts stay unknown.

Implementation-owned reproducible protocol, source hashes and content-free JSON
observations are in `experiments/feasibility/agent-observability/`. Raw events,
OTLP payloads, messages, tool outputs and login state remain private and outside
Git. The live test used the installed default model without a model override;
the manually observed model in private receipts was `gpt-6.1-sol` (the published
summary does not record its value). It is not a Docker parity test.

Observed OTLP attribute names include user email/account identity and tool
arguments/output despite prompt logging being disabled. A product collector
needs explicit content/identity filtering and access/retention policy before any
external export. Only attribute names and structural counters are published here.

## Required integration

Bind host-owned graph execution / node invocation identity to native session,
turn and item IDs and OTel trace/span IDs before showing them together. Do not
join by wall-clock overlap or agent label. A native session may span invocations;
an invocation can contain multiple turns. Keep those identities separate.

Use native events for message/tool detail and OTel for correlated request/tool
spans and metrics. Preserve source provenance and expose missing/redacted content
as such. A provider event and its OTel counterpart must not become two counted
actions or two charges. Keep cumulative token snapshots separate from increments;
the observed first turn had multiple usage updates. Do not sum the snapshots.

Use provider cost when supplied, labelled as a provider estimate rather than an
invoice. A calculated estimate needs model, versioned rates, currency and cache
semantics. A subscription session's token counters alone establish no billed cost.
No pricing table or estimated amount was invented in this probe.

The editable [Agents tab target](agent-activity.drawio) owns the proposed layout:
one graph-run selector; shared agent lanes; expansion into invocations, turns,
observed subagents and tools; a selected-segment detail panel; and token/cost
series. Messages render as messages, JSON/code is highlighted and expandable,
local-time/duration labels are readable, exact UTC timestamps remain inspectable.
Diagram content is a design target, not fabricated runtime acceptance.

## Open gates

- Original Docker runner and pinned CLI parity; no original-agent acceptance yet.
- Host graph-run/invocation binding, parallel-agent capture and Gantt interaction.
- Native subagent execution and explicit parent identities; none ran in this probe.
- Claude runtime/exporter acceptance; its reviewer calls are not telemetry probes.
- Resume/reconnect, durable tail handling, deletion and sensitive-content policy.

## Primary references, accessed 2026-10-15

- [Codex telemetry](https://developers.openai.com/codex/config-advanced/#observability-and-telemetry)
- [Codex App Server](https://developers.openai.com/codex/app-server/)
- [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Dynatrace's Claude example](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples/tree/main/claude-code)

Current documentation supports investigation, not compatibility guarantees for
the older pinned Docker runtime. Claude's cost and subagent telemetry have not
been empirically accepted here.

## Later original-runner graph evidence

The [2026-10-15 graph validation](../validation.md#original-docker-agents-graph-inspection-2026-10-15)
records the subsequent real Docker 0.159.2 graph execution, concurrent original
agents, a resumed thread, one explicit native child and local OTLP receipt.
The [bounded inspection slice](../contract/interfaces.md#original-agent-graph-inspection-slice-2026-10-15)
states the implemented identity, read-only, usage and estimation guarantees.
The host-only observations above remain historical evidence. Other providers,
metrics, full exporter completeness, crash reconciliation and the remaining
Draw.io interactions are still open; this update does not promote maturity.
