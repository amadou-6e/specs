# Subsystems

Subsystems is an expandable collection of multi-file specification entries. Each
entry is a functionally cohesive part of Theseo with one stable behavioral and
contractual boundary.

## Contained elements

```text
subsystems/
├── 1 README.md
├── 1 template/
└── 0..* <subsystem>/ entries
```

Each subsystem entry contains one `README.md`, `behavior.md`, and `validation.md` when
mature, plus applicable interface, configuration, architecture, usage,
troubleshooting, language-mapping, extension, and migration documents. Subsystems may
depend on other subsystems but must not silently share ownership of one contract.

Copy [template/](template/README.md) to create an entry. The template itself is not a
subsystem entry.
