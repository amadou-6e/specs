# Worlds and geometry contract

## Contained elements

```text
contract/
└── 1 README.md
```

The contract owns coordinate interpretation; occupied, free, and unknown semantics;
bounded queries; immutable base geometry and mutable overlays; world identities; and
failure behavior for invalid coordinates or corrupt artifacts.

## Imported sources

- [Voxel model](../../../rust/voxel-spec.md)
- [Legacy world contract](../../../rust/world.md)
- [Ingestion contract](../../../rust/ingest.md)
- [Routing geometry integration roadmap](../../../routing-geometry-integration-roadmap.md)

Conflicting coordinate widths, extents, or backend assumptions are unresolved
migration work rather than simultaneous guarantees.
