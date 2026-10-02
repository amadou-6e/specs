# Owned subsystems

Folder collection: README.md (1), template/ (1), named subsystems (0..*). Each entry has
README.md, contract/README.md, design/README.md and validation.md (1 each); focused
contract/design pages (0..*) are conditional. Templates define the internal schema.

- [Agent execution](agent-execution/README.md): provider dispatch, grants and session/workspace binding.
- [Skill registry](skill-registry/README.md): immutable revision, selection, drafts and promotion separation.
- [Run traces](run-traces/README.md): raw events, identity, projection and evidence semantics.
- [Work Graph](work-graph/README.md): repository-work snapshots, dependency evidence and readiness.
- [Copyable example](template/README.md): illustrative snapshot-bound execution boundary.

Contracts own target behavior, design explains mechanisms, validation qualifies maturity.
Shared record definitions stay in architecture. Copy template/ directly, rename, replace
every example fact and metadata/lifecycle, then add the entry to this index.
