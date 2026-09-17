# Trajectory and replay design

## Contained elements

```text
design/
├── 1 README.md
├── 1 python.md
└── 1 rust.md
```

Python owns trajectory collection and run selection. Rust owns replay state, regional
world reads, meshing, camera projection, z-buffering, UI execution, and headless frame
rendering.
