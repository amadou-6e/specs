# Agent execution exchange schemas

Container: `README.md` (1), one named Markdown sketch for each direct exchange
touching agent execution (5), other files (0). The five files are individually
addressable draft payload shapes, not executable schemas or settled wire formats.

| Exchange | Direction | Schema |
| --- | --- | --- |
| IF-04 skill materialization | Agent execution requests from skill registry | [if-04-skill-materialization.md](if-04-skill-materialization.md) |
| IF-05 stage invocation | Langflow integration sends to agent execution | [if-05-stage-invocation.md](if-05-stage-invocation.md) |
| IF-06 invocation outcome | Agent execution returns to Langflow integration | [if-06-invocation-outcome.md](if-06-invocation-outcome.md) |
| IF-08 agent event | Agent execution sends to run traces | [if-08-agent-event.md](if-08-agent-event.md) |
| IF-10 output manifest | Agent execution sends to results and artifacts | [if-10-output-manifest.md](if-10-output-manifest.md) |

This folder owns the approximate payload shapes for these five exchanges.
Behavior and failure rules remain in [agent execution interfaces](../interfaces.md)
and the respective provider/consumer contracts. The [subsystem index](../../../README.md#payload-sketch-conventions)
defines `?`, `Ref`, IDs and the shared-record relationship. Each file records
the producer, consumer, shape, and unresolved details; changing a shape also
requires checking both ends of its handoff. New exchanges need their own file
and an index entry, not another aggregate code block here.
