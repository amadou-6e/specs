# Architecture

Fixed category: README.md, shared-contracts.md, component-proposal.md (1 each), focused
cross-subsystem documents (0..*). No independent entry folders or copyable folder template.

[Shared contracts](shared-contracts.md) own cross-boundary records and edges. The
[original proposal](component-proposal.md) retains historical 2026-09-28 estimates and
open choices plus its dated pilot update. Its planning ranges are not current commitments.

The flow adapter supplies frozen inputs and skill refs. The registry owns exact bundle
bytes and draft candidates. Execution owns profiles, workspace snapshots, dispatch and
resume binding. Monitoring owns raw event storage and projections. Langflow must not
hold the only copy of runs, revisions or traces.

These are target relationships. The [pilot](../experiments/local-skill-agent-pilot/README.md)
implements a narrower adapter. Definition-version correlation, Claude parity, production
identity and complete normalized monitoring remain gaps. New UI requires reviewed Draw.io.

[Issue-to-agent user traversal](user-traversal.md) links the editable graph of the
user-confirmed journey, its generation input and unresolved product choices. It is
cross-subsystem navigation, not a screen-geometry or implementation specification.

[Proposed subsystem handoffs](subsystem-handoffs.md) links a two-page editable
Draw.io graph and inventories the commands, events and references crossing the
current Laomedo boundaries. It records open interface decisions rather than
asserting an implemented wire protocol.
[Subsystem decision record](subsystem-decision-record.md) preserves the
individual user choices used to derive those handoffs and identifies the
remaining open product and feasibility questions.
