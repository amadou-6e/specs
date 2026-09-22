# Rust implementation

## Contained elements

```text
implementation/rust/
├── 1 README.md
└── 0..* Rust implementation documents
```

Each additional document owns one bounded contributor rule or local workflow. This
partition is fixed; documents do not create nested implementation categories.

This fixed partition owns contributor guidance for the native core and its local
workflows.

## Scope

- Crate and module organization.
- Trait, ownership, borrowing, and error conventions.
- Panic and unsafe-code policy.
- Storage, memory, cache, and concurrency expectations.
- PyO3 and native ABI boundaries.
- Rust tests, parity checks, benchmarks, and profiling.
- Native build, diagnostic, and release procedures.

Implementation guidance links to subsystem contracts and must not redefine their
observable behavior.
