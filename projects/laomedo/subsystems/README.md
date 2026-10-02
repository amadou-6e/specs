# Owned subsystems

Folder collection: README.md (1), template/ (1), named subsystems (0..*). Each entry has
README.md, contract/README.md, design/README.md and validation.md (1 each); focused
contract/design pages (0..*) are conditional. Templates define the internal schema.

- [Issue integration](issue-integration/README.md): issue references, GitHub event context and reviewed issue publication.
- [Langflow integration](langflow-integration/README.md): saved workflow selection, launch correlation and the agent-node boundary to Langflow.
- [Prompt and skill library](prompt-skill-library/README.md): curated prompt/skill entries, backends and version selection.
- [Agent execution](agent-execution/README.md): provider dispatch, grants and session/workspace binding.
- [Skill registry](skill-registry/README.md): immutable skill revisions, drafts and promotion separation.
- [Run traces](run-traces/README.md): raw events, identity, projection and evidence semantics.
- [Results and artifacts](results-artifacts/README.md): run summaries, artifact references and follow-up context.
- [Copyable example](template/README.md): illustrative snapshot-bound execution boundary.

Contracts own target behavior, design explains mechanisms, validation qualifies maturity.
Shared record definitions stay in architecture. Copy template/ directly, rename, replace
every example fact and metadata/lifecycle, then add the entry to this index.

## Interface map

This is a draft map of **direct subsystem contacts** derived from the
[handoff graph](../architecture/subsystem-handoffs.md) and
[decision record](../architecture/subsystem-decision-record.md). `IF-09` makes
explicit the launch/run context that results need in addition to trace and
artifact references. Each row names the provider of the interface; the linked
contract owns its behavior. IDs identify design discussions, not wire methods.

| Interface | Provider → consumer | What crosses | Owning contract |
| --- | --- | --- | --- |
| IF-01 Issue context | Issue integration → Langflow integration | Selected issue/repository reference, optional event and existing PR reference | [Issue integration](issue-integration/contract/interfaces.md) |
| IF-02 Library resolution | Prompt and skill library → Langflow integration | Prompt and skill selection, exact resolved revisions | [Prompt and skill library](prompt-skill-library/contract/interfaces.md) |
| IF-03 Skill revision lookup | Skill registry → Prompt and skill library | Immutable skill identity, exact revision and hashes | [Skill registry](skill-registry/contract/interfaces.md) |
| IF-04 Skill materialization | Skill registry → Agent execution | Validated skill snapshot and dependency closure for the chosen workspace | [Skill registry](skill-registry/contract/interfaces.md) |
| IF-05 Agent invocation | Langflow integration → Agent execution | Stage invocation, frozen configuration, input/file refs, session and workspace choices | [Agent execution](agent-execution/contract/interfaces.md) |
| IF-06 Invocation outcome | Agent execution → Langflow integration | Status, output refs and failure classification for one invocation | [Agent execution](agent-execution/contract/interfaces.md) |
| IF-07 Workflow events | Langflow integration → Run traces | Workflow/run/stage/invocation lifecycle and correlation | [Langflow integration](langflow-integration/contract/interfaces.md) |
| IF-08 Agent events | Agent execution → Run traces | Provider events, native session correlation and partial evidence | [Agent execution](agent-execution/contract/interfaces.md) |
| IF-09 Run context | Langflow integration → Results and artifacts | Exact launch configuration, workflow identity and terminal status | [Langflow integration](langflow-integration/contract/interfaces.md) |
| IF-10 Output manifest | Agent execution → Results and artifacts | Artifact refs, locations, save/publish state and PR reference when produced | [Results and artifacts](results-artifacts/contract/interfaces.md) |
| IF-11 Trace link | Run traces → Results and artifacts | Trace/digest ref, completeness and correlation | [Run traces](run-traces/contract/interfaces.md) |
| IF-12 Follow-up issue | Results and artifacts → Issue integration | User-reviewed editable issue proposal with prior-run evidence refs | [Issue integration](issue-integration/contract/interfaces.md) |
| IF-13 Follow-up run | Results and artifacts → Langflow integration | Existing PR ref, prior-run link and chosen session mode | [Langflow integration](langflow-integration/contract/interfaces.md) |
| IF-14 Skill draft submission | Prompt and skill library → Skill registry | Proposed skill edit and base revision for separate validation/promotion | [Skill registry](skill-registry/contract/interfaces.md) |

GitHub, Langflow runtime, timers, UI and chat are outside this list of
subsystem-to-subsystem contacts. Agent execution writes PRs to GitHub; issue
integration publishes reviewed issues. The shared approval mechanism is a
cross-cutting interface used by agent execution and chat, not a PR-delivery or
workspace-management subsystem. A pair absent from this table has no **known
direct** handoff; it may still communicate through a listed boundary.
