# Internal architecture

## Contained elements

```text
design/
├── 1 README.md
├── 0..1 python.md
└── 0..1 rust.md
```

This folder explains how the subsystem realizes its contract. The language mappings
assign implementation responsibilities but do not own observable behavior.

Describe internal components, data flow, control flow, state ownership, persistence,
caching, concurrency, failure boundaries, performance model, and trust boundaries.
Link durable choices to decision records.
