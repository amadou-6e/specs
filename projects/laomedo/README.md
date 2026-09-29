# Laomedo specifications

Laomedo is a proposed design environment for agent workflows. The [historical AGENTVIZ reference workshop](deprecated/ui/README.md) records existing screen geometry and demo content. It does not specify new Laomedo behavior.

The [agent and skill components proposal](components/agent-and-skill-components.md)
defines versioned skills, Codex and Claude execution, isolated persistence,
trace inspection, and a phased implementation estimate. It is a technical
proposal, not a UI interaction specification.

Feasibility findings test that proposal against upstream tools. The
[Claude runner isolation probes](feasibility/121.md) for issue #121
pin `claude-agent-sdk 0.2.161`, reproduce the missing-CLI blocker precisely,
and prepare setting-source, streaming, and resume probes behind a credential
gate.
