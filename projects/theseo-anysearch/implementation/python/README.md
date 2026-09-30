# Python implementation

This fixed partition owns contributor guidance for the Python package and its local
workflows.

## Contained elements

```text
implementation/python/
├── 1 README.md
└── 0..* Python implementation documents
```

Each additional document owns one bounded contributor rule or local workflow. This
partition is fixed; documents do not create nested implementation categories.

## Scope

- Package and module organization.
- Public API and typing expectations.
- Configuration models and path handling.
- Optional dependencies and provider discovery.
- General Python multiprocessing and Python-side determinism; Ray actors,
  workers, and distributed execution belong under [Ray](../ray/README.md).
- The Python/Rust ownership and binding boundary.
- Python test organization, diagnostics, and performance hazards.
- Python-owned installation, training, tuning, cache, and recovery procedures.

Implementation guidance links to subsystem contracts and must not redefine their
observable behavior.

## Investigation queue

These draft pages plan source-backed contributor guidance; they are not yet accepted
rules. Resolve each against a pinned product revision and relevant tests:

- [Python package and module ownership](module-ownership.md)
- [Python extension implementation](extensions.md)
- [Python code conventions](code-conventions.md)

The [testing guide](testing.md) records the source-pinned layout, selection,
prerequisites, and CI boundaries; it does not claim unrun tests pass.
