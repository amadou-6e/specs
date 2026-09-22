# Model Garden implementation

Implementation is a fixed, top-structured category for contributor rules and local
workflows. It describes how Model Garden code is organized and maintained without
redefining the behavior owned by subsystem contracts.

## Contained elements

```text
implementation/
|-- 1 README.md
|-- 1 python/
|   `-- 1 README.md
`-- 0..* cross-stack implementation documents
```

Model Garden currently has one implementation partition, [Python](python/README.md),
because its implementation resides under `theseo_anysearch/garden/`. Add a language or
framework partition only after the project gains a real responsibility in that stack
and this structure is revised explicitly.

This category intentionally has no copyable template: its partitions are fixed project
structure, not independently created specification entries. End-to-end local workflows
for dataset construction, pretraining, qualification, publication, cache recovery, and
artifact inspection belong here when they span subsystems. Subsystem-specific usage and
diagnostics remain in the owning subsystem's guides.
