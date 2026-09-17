# Architecture

Architecture is a fixed, top-structured category describing how Theseo's subsystems
fit together. It is one project-wide specification entry, not a collection of
independent architecture entries.

## Contained elements

```text
architecture/
├── 1 README.md
├── 1 template.md
├── 0..* focused architecture documents
└── 0..* editable diagrams
```

Focused documents may describe system context, subsystem relationships, data flow,
execution lifecycle, artifact models, and cross-subsystem invariants. Decisions own
the rationale for individual durable choices. Subsystems own their internal behavior
and contracts.

Use [template.md](template.md) when adding a focused architecture document.
