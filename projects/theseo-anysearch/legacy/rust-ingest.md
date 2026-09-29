---
title: Imported Ingest Specification
status: superseded
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-27
applies_to: [theseo-anysearch]
supersedes: null
related: []
---

> Historical source. This document is not an authoritative current specification.
> Its original wording is retained below for traceability.

## Migration disposition

The historical STL and voxelization design is not the current universal geometry contract. Current authority: [worlds-and-geometry README.md](../subsystems/worlds-and-geometry/README.md).
No unverified historical claim is promoted by this move. Its original authority
ended no later than this classification under specs issue #110; an earlier
supersession date has not been established. The source revision remains available
in Git history.

## Archived material

# Ingest Specification

## Purpose

Convert an ASCII STL geometry file into voxel placements in `WorldState`.
The ingest pipeline is a two-stage process:

```
ASCII STL text
    └── parse_ascii_stl()  →  StlMesh
            └── voxelize_mesh()  →  Vec<BlockPlacement>
                    └── caller inserts into WorldState via World::set_block()
```

All functions are pure (no I/O, no global state). File reading is the caller's responsibility.

---

## Module layout (`world/ingest/`)

| File | Responsibility |
|---|---|
| `stl.rs` | ASCII STL parser: text → `StlMesh` |
| `voxelize.rs` | Mesh → voxel placements: `StlMesh` → `Vec<BlockPlacement>` |

Current source location is `import/` (a legacy name). It is renamed to `world/ingest/`
in the target structure to reflect that ingest is part of the world subsystem.

---

## `world/ingest/stl.rs` — STL Parser

### Types

```rust
pub struct StlMesh {
    pub triangles: Vec<[[f32; 3]; 3]>,   // each triangle: [v0, v1, v2], each vertex: [x, y, z]
}

pub enum ImportError {
    InvalidFormat(String),
}
```

### Function

```rust
pub fn parse_ascii_stl(source: &str) -> Result<StlMesh, ImportError>
```

### Algorithm

1. Scan lines; collect any line that starts with `"vertex "` after trimming
2. Parse each vertex line as three `f32` values (x, y, z)
3. Return `InvalidFormat` if any float fails to parse
4. Require total vertex count ≥ 3 and divisible by 3; else return `InvalidFormat`
5. Group consecutive triples into `[[f32; 3]; 3]` triangle entries

### Constraints

- ASCII STL format only — binary STL is not supported
- Normal vectors in the STL file are ignored (not parsed, not stored)
- The parser is tolerant: lines that do not start with `"vertex "` are skipped silently
- No face-count validation against the STL header (header is ignored entirely)

### Error cases

| Condition | Error |
|---|---|
| Vertex coordinate is not a valid `f32` | `InvalidFormat("could not parse float value '...'")` |
| Vertex count < 3 or not a multiple of 3 | `InvalidFormat("vertex list must be a multiple of 3")` |
| Missing x, y, or z token on a vertex line | `InvalidFormat("missing x/y/z")` |

---

## `world/ingest/voxelize.rs` — Voxelizer

### Types

```rust
pub struct BlockPlacement {
    pub coord: Coord,
    pub block: Block,   // always Block::default() — colour/kind set by caller if needed
}
```

### Function

```rust
pub fn voxelize_mesh(mesh: &StlMesh, origin: Coord, scale: f32) -> Vec<BlockPlacement>
```

### Algorithm

**Phase 1 — Surface sampling**

For each triangle, sample four point sets into a `HashSet<Coord>`:

1. **Vertices** — the three corner points of the triangle
2. **Edge AB** — linear interpolation along each of the three edges, with step count = `ceil(edge_length_in_voxels)`
3. **Interior** — barycentric grid over the triangle face, with step count = `ceil(max_edge_length_in_voxels)`

Sampling density is proportional to `scale`: a scale of 1.0 places one voxel per STL unit.

Each sampled floating-point point is converted to a world coordinate:
```
world_coord = (floor(origin.x + point.x * scale),
               floor(origin.y + point.y * scale),
               floor(origin.z + point.z * scale))
```

Points that would be negative or outside `[0, WORLD_SIZE)` on any axis are discarded silently.

**Phase 2 — Solid fill**

After surface sampling, `solid_fill` converts the shell into a solid volume:

1. Compute the axis-aligned bounding box of all surface voxels; extend by 1 on each side (clamped to world bounds)
2. BFS flood fill from all bounding-box face cells that are **not** surface voxels — these seed the exterior
3. Any cell inside the bounding box that is neither surface nor exterior is classified as interior
4. Interior cells are added to the filled set — the result is a fully solid geometry

**Phase 3 — Output**

Each coordinate in the filled set is emitted as a `BlockPlacement` with `Block::default()`.
Order of output is unspecified (comes from `HashSet` iteration).

### Properties

| Property | Value |
|---|---|
| Output | Solid voxel geometry (surface + interior) |
| Duplicate voxels | Eliminated by the intermediate `HashSet` |
| Out-of-bounds points | Silently discarded |
| Empty mesh | Returns empty `Vec` |
| Block kind | Always `Block::default()` — caller assigns semantic meaning |

### Scaling guidance

| Scale | Effect |
|---|---|
| 1.0 | 1 STL unit = 1 voxel |
| 0.5 | 1 STL unit = 0.5 voxels (geometry shrinks) |
| 5.0 | 1 STL unit = 5 voxels (geometry expands) |

Choose scale such that the voxelized geometry fits within the intended region of the 1000³ world.

---

## Caller Pattern

```rust
// Typical usage in py_bindings.rs
let mesh = parse_ascii_stl(&stl_ascii)?;
let placements = voxelize_mesh(&mesh, (origin_x, origin_y, origin_z), scale);
let mut world = WorldState::new();
for p in &placements {
    world.set_block(p.coord, p.block.clone())?;
}
```

---

## Limitations

| Limitation | Notes |
|---|---|
| ASCII STL only | Binary STL requires a separate parser (out of scope v1) |
| No normal-based culling | All faces are sampled regardless of orientation |
| Solid fill is local | Operates within bounding box + 1 margin; correct for closed convex and most concave meshes; may mis-classify for meshes with internal voids |
| No LOD | All triangles sampled at full density; very large meshes with high scale may produce many voxels |
| No partial update | `voxelize_mesh` always returns a full placement list; incremental voxelization is not supported |
