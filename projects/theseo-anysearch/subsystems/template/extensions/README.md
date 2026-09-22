# Concrete subsystem extensions

## Contained elements

```text
extensions/
├── 1 README.md
└── 0..* <extension>/
```

A concrete extension adds optional behavior or an optional implementation to its host
subsystem through an extension point declared in `../contract/extensions.md`. It is
not a peer subsystem and cannot weaken or redefine the host contract.

Each extension folder contains its own `README.md`, contract additions, design, and
validation evidence as needed. It must identify its host extension point, optionality,
dependencies, activation mechanism, compatibility boundary, and behavior when absent.
