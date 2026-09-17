# Worlds and geometry design

## Contained elements

```text
design/
└── 1 README.md
```

The native core owns sparse/chunked storage, overlay resolution, disk residency,
compiled-world reads, and geometry conversion. Python owns offline compiler and
artifact orchestration surfaces where documented.

## Imported sources

- [World implementation](../../../rust/world.md)
- [Ingestion](../../../rust/ingest.md)
- [Terrain geometry generator](../../../terrain-geometry-generator.md)
