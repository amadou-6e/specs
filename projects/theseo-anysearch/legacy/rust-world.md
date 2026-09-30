---
title: Imported World Specification
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

The fixed-size, HashMap-only world description conflicts with the current compiled and regional world contract. Current authority: [worlds-and-geometry README.md](../subsystems/worlds-and-geometry/README.md).
No unverified historical claim is promoted by this move. Its original authority
ended no later than this classification under specs issue #110; an earlier
supersession date has not been established. The source revision remains available
in Git history.

## Archived material

# World Specification

## Domain

| Property | Value |
|---|---|
| World dimensions | 1000 x 1000 x 1000 |
| Coordinate type | `(u16, u16, u16)` — `Coord` alias |
| World size constant | `WORLD_SIZE: u16 = 1000` |
| World center constant | `WORLD_CENTER: (u16, u16, u16) = (500, 500, 500)` |
| Voxel size | 1 unit |

---

## Storage Strategy

### Primary: Sparse HashMap

```rust
pub struct WorldState {
    filled: HashMap<Coord, Block>,
}
```

- Only filled voxels are stored
- Memory: O(n) where n = number of filled voxels
- Default 10x10x10 cube = 1000 entries
- Dense equivalent would be ~954 MB (never materialized)

### Secondary: Dense index (local algorithms only)

```rust
fn index(x: usize, y: usize, z: usize) -> usize {
    x + y * 1000 + z * 1000 * 1000
}
```

Used internally when a dense local grid is needed (e.g., flood fill, voxelization).
Never allocate a full 1000^3 dense array unless working on a bounded sub-region.

---

## Block Interface Contract

```rust
pub trait World {
    fn set_block(&mut self, coord: Coord, block: Block) -> Result<(), WorldError>;
    fn remove_block(&mut self, coord: Coord) -> Result<(), WorldError>;
    fn update_block(&mut self, coord: Coord, update: BlockUpdate) -> Result<(), WorldError>;
    fn get_block(&self, coord: Coord) -> Option<&Block>;
}
```

`WorldState` is the concrete implementation of `World`.

### Behavioral Rules

1. `set_block` inserts or replaces a block — idempotent for same coord
2. `remove_block` returns `WorldError::NotFound` when coord is absent
3. `update_block` mutates an existing block — returns `WorldError::NotFound` if missing
4. All operations validate bounds and return `WorldError::OutOfBounds` for coords >= 1000

### Convenience Methods (on WorldState directly)

```rust
fn set(&mut self, coord: Coord, filled: bool)       // insert or remove based on bool
fn toggle(&mut self, coord: Coord)                  // flip filled/empty
fn is_filled(&self, coord: Coord) -> bool
fn iter_filled(&self) -> impl Iterator<Item = &Coord>
fn len(&self) -> usize
fn estimated_sparse_bytes(&self) -> usize           // len * size_of::<(Coord, Block)>
fn dense_world_bytes() -> usize                     // static: 1_000_000_000
```

---

## Initialization

### Default World

`WorldState::default()` calls `with_default_cube()`:

```rust
pub fn with_default_cube() -> Self {
    // fills x, y, z in [495, 505) — the 10^3 cube at world center
}
```

### Empty World

```rust
WorldState::new()  // empty HashMap, no voxels filled
```

---

## Invariants

1. All coords must be in `[0, WORLD_SIZE)` on all three axes
2. `remove_block` and `update_block` on absent coords return explicit errors (not panics)
3. World state must produce deterministic output for repeated seeds and identical command streams
4. Sparse storage must not silently cap at a voxel count limit
