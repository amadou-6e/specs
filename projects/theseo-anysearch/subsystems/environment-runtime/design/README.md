# Environment runtime design

## Contained elements

```text
design/
├── 1 README.md
├── 1 python.md
└── 1 rust.md
```

Rust owns authoritative state transitions and performance-sensitive queries. Python
owns standards-compliant wrappers, configuration translation, spaces, and framework
registration. The bridge owns DTO and conversion fidelity.
