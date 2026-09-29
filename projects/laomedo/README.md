# Laomedo specifications

Laomedo is a proposed design environment for agent workflows. The [historical AGENTVIZ reference workshop](deprecated/ui/README.md) records existing screen geometry and demo content. It does not specify new Laomedo behavior.

The [agent and skill components proposal](components/agent-and-skill-components.md)
defines versioned skills, Codex and Claude execution, isolated persistence,
trace inspection, and a phased implementation estimate. It is a technical
proposal, not a UI interaction specification.

Feasibility findings test that proposal against upstream tools. The
[upstream dependencies matrix](feasibility/118.md) records
inspected versions, licenses, extension points, and gaps for AGENTVIZ,
Langflow, Codex, Claude Code, and Deep Agents.

The [bounded skill discovery findings](feasibility/119.md) for issue #119
record Codex discovery, a manifest pilot, one completed combined skill
invocation, auth isolation limits, and the bundled-script permissions to test.
Claude execution and selected-subset isolation remain unproven.

The [Codex runner isolation probes](feasibility/120.md) for issue #120
build no-model checks for model/effort validation, profile isolation, thread
persistence, and streamed events. Probes are written; results are pending.
