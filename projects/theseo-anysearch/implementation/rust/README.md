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

## Investigation queue

The following draft pages are investigation plans, not accepted implementation
rules. Each must be resolved against a pinned product revision and test evidence
before its plan is replaced with contributor guidance:

- [Native module ownership](module-ownership.md)
- [Native extension implementation](extensions.md)
- [Rust code conventions](code-conventions.md)
- [Rust to Python bridge](python-bridge.md)
- [Native build and verification workflow](native-workflow.md)
