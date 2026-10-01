# Laomedo specifications

Laomedo is a proposed design environment for agent workflows. The [historical AGENTVIZ reference workshop](deprecated/ui/README.md) records existing screen geometry and demo content. It does not specify new Laomedo behavior.

The proposed [Work Graph capability](capabilities/work-graph.md) defines
repository-work snapshots, dependency evidence, and a staged path to pinned
agent execution. Its view-owned UI design is still to be specified.

The [agent and skill components proposal](components/agent-and-skill-components.md)
defines versioned skills, Codex and Claude execution, isolated persistence,
trace inspection, and a phased implementation estimate. It is a technical
proposal, not a UI interaction specification.

Feasibility findings test that proposal against upstream tools. The
[Claude runner isolation probes](feasibility/121.md) for issue #121
pin `claude-agent-sdk 0.2.161`, reproduce the missing-CLI blocker precisely,
and prepare setting-source, streaming, and resume probes behind a credential
gate. No model-backed condition was exercised, so the local Claude MVP is
no-go on current evidence.

The [upstream dependencies matrix](feasibility/118.md) records
inspected versions, licenses, extension points, and gaps for AGENTVIZ,
Langflow, Codex, Claude Code, and Deep Agents.

The [bounded skill discovery findings](feasibility/119.md) for issue #119
record Codex discovery, a manifest pilot, one completed combined skill
invocation, auth isolation limits, and the bundled-script permissions to test.
Claude execution and selected-subset isolation remain unproven.

The [Skill Draft feasibility result](feasibility/122.md) records a versioned
editing policy, deterministic draft validation, and a bounded Codex edit,
resume, and forbidden-write denial under the native Windows sandbox. The
[Docker Skill Draft study](feasibility/docker-skill-draft.md) tests the parallel
container route with an observed agent-originated denial, a pinned candidate,
and persistent resume. Its go decision is limited to a single-user local
prototype.

The [Codex runner isolation findings](feasibility/120.md) for issue #120
record a pinned CLI and a three-turn private ChatGPT handoff. Model/effort
selection and post-restart resume worked, while no tool call appeared in the
stream and the personal-session comparison remained inconclusive. The local
MVP decision is no-go on this evidence.

The [trace completeness study](feasibility/123.md) imports a private Codex
rollout into AGENTVIZ and tests a small event projection without new model
calls. Claude has no credentialed trace yet, and Langflow's outer span does
not provide structured correlation to the private run. Full cross-provider
monitoring remains unverified.

The [feasibility synthesis](feasibility/124.md) recommends a bounded local
Codex pilot using a separate Docker runner, with full dual-provider and hosted
claims deferred until the missing Claude, authentication, trace, and licensing
evidence exists.
