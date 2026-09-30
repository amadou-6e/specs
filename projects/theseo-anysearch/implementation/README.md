# Implementation

Implementation is a fixed, top-structured category for contributor guidance and local
development workflows. It has exactly four technology partitions:

- [Python](python/README.md)
- [Rust](rust/README.md)
- [RLlib](rllib/README.md)
- [Ray](ray/README.md)

Adding another implementation partition requires an explicit update to
[SPECS.md](../SPECS.md); contributors do not copy a template to create arbitrary
implementation categories.

## Contained elements

```text
implementation/
├── 1 README.md
├── 1 python/
├── 1 rust/
├── 1 rllib/
├── 1 ray/
└── 0..* cross-stack implementation documents
```

The four partitions are fixed containers, not repeatable entries. Cross-stack
documents are individual implementation entries and must not create new technology
partitions implicitly.

## Shared responsibilities

Cross-stack rules live in this README or in a clearly named document directly under
`implementation/`. They include repository organization, Python/Rust ownership,
serialization, coordinate conventions, deterministic identity, compatibility,
dependency policy, testing, and review expectations.

Put a test beside the production concern whose behavior it proves, then choose
the appropriate unit or integration boundary. The annotated target trees and
placement rules live with [Python testing](python/testing.md) and
[Rust testing](rust/testing.md); cross-language checks should link both sides
without duplicating every assertion.

## Local workflows and runbooks

This category also owns end-to-end local workflows formerly described as operations:
installation, training, tuning, monitoring, artifacts, caches, recovery,
troubleshooting, and releases. Put technology-specific instructions in the owning
partition. Put a genuinely cross-stack workflow directly under `implementation/` and
link to the subsystem contracts it exercises.

These are local development and execution instructions, not deployed-service
operations or incident-management procedures. Subsystem-specific usage and
troubleshooting remain with the owning subsystem.
