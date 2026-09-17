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

Each mature subsystem entry contains one overview, one `contract/`, one `design/`, and
one `validation.md`. It may additionally contain consumer `guides/` and active
`migrations.md`. Contract details, language mappings, and diagnostics remain grouped
under their owning area rather than appearing as unrelated root-level files.
Subsystems may depend on other subsystems but must not silently share ownership of one
contract.

Copy [template/](template/README.md) to create an entry. The template itself is not a
subsystem entry.
