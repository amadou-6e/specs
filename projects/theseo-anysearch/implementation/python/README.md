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
- Multiprocessing, Ray, and Python-side determinism.
- The Python/Rust ownership and binding boundary.
- Python test organization, diagnostics, and performance hazards.
- Python-owned installation, training, tuning, cache, and recovery procedures.

Implementation guidance links to subsystem contracts and must not redefine their
observable behavior.
