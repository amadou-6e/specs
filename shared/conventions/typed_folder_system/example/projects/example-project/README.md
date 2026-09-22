# Example Project

This is the minimal worked example for the
[typed and named folder hierarchy](../../../README.md) convention. It is not a real
project; it exists so the convention can be demonstrated and validated in isolation.

## Contained elements and relationships

```text
example-project/
├── 1 README.md
├── 1 SPECS.md
├── 1 spec.json
├── 1 architecture/
├── 1 subsystems/
└── 1 decisions/
```

`SPECS.md` is authoritative for the category set below and each category's
structural type; this README only orients a new reader.

## Categories

- [Architecture](architecture/README.md) — fixed top-structured system map.
- [Subsystems](subsystems/README.md) — expandable folder collection of owned
  behavioral contracts.
- [Decisions](decisions/README.md) — expandable document collection of durable
  choices.
