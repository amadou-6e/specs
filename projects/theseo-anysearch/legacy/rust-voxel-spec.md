---
title: Imported Voxel Renderer Specification
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

The fixed world dimensions, storage model, and renderer milestones must not override current world and replay contracts. Current authority: [worlds-and-geometry README.md](../subsystems/worlds-and-geometry/README.md).
No unverified historical claim is promoted by this move. Its original authority
ended no later than this classification under specs issue #110; an earlier
supersession date has not been established. The source revision remains available
in Git history.

## Archived material

# Voxel Renderer Specification

## Overview

A Rust-native interactive 3D voxel renderer using `eframe`/`egui`.
Displays a 1000x1000x1000 voxel world with a 10x10x10 solid cube centered at (495..505, 495..505, 495..505).

---

## World Definition

| Property | Value |
|---|---|
| World dimensions | 1000 x 1000 x 1000 voxels |
| Coordinate type | `(u16, u16, u16)` |
| World size constant | `WORLD_SIZE = 1000` |
| World center constant | `WORLD_CENTER = (500, 500, 500)` |
| Default cube range | x, y, z in [495, 505) — 10 voxels each axis |
| Empty state | coord absent from HashMap |
| Filled state | coord present in HashMap with a `Block` value |

### Storage Implementation

The world uses a sparse `HashMap<Coord, Block>`:

```rust
pub type Coord = (u16, u16, u16);

pub struct WorldState {
    filled: HashMap<Coord, Block>,
}
```

This stores only filled voxels. The default 10x10x10 cube = 1000 entries.

**Dense memory (not used):** 1000^3 = ~954 MB — materialized only for local algorithms if needed.

### Index Formula (for dense algorithms only)

```rust
fn index(x: usize, y: usize, z: usize) -> usize {
    x + y * 1000 + z * 1000 * 1000
}
```

---

## World Interface

```rust
pub trait World {
    fn set_block(&mut self, coord: Coord, block: Block) -> Result<(), WorldError>;
    fn remove_block(&mut self, coord: Coord) -> Result<(), WorldError>;
    fn update_block(&mut self, coord: Coord, update: BlockUpdate) -> Result<(), WorldError>;
    fn get_block(&self, coord: Coord) -> Option<&Block>;
}
```

`WorldState` is the concrete implementation of `World`.

**Convenience methods on `WorldState`:**

```rust
fn set(&mut self, coord: Coord, filled: bool)
fn toggle(&mut self, coord: Coord)
fn is_filled(&self, coord: Coord) -> bool
fn iter_filled(&self) -> impl Iterator<Item = &Coord>
fn len(&self) -> usize
fn estimated_sparse_bytes(&self) -> usize
```

**Error variants:**
- `WorldError::OutOfBounds(coord)` — coord not in [0, WORLD_SIZE)
- `WorldError::NotFound(coord)` — update/remove on absent coord

---

## Rendering (Interactive)

### Stack

- **Crate:** `eframe = "0.31"` + `egui = "0.31"`
- **Math:** `glam = "0.29"` (Vec3, Mat4, perspective projection)
- **Viewport:** `egui::CentralPanel` with custom software rasterizer
- **Projection:** Right-handed perspective (`Mat4::perspective_rh`)

### Camera

| Property | Default |
|---|---|
| Position | (500.0, 500.0, -200.0) |
| Target | (500.0, 500.0, 500.0) |
| Up vector | (0, 1, 0) |
| FOV | 60 degrees |
| Near clip | 1.0 |
| Far clip | 2000.0 |
| Orbit sensitivity | 0.01 rad/px |
| Movement speed | 180 units/s |
| Zoom clamp | [3.0, 5000.0] |

### Rendering Pipeline (per frame)

1. Compute MVP = `projection_matrix(aspect) * view_matrix()`
2. Fill background (`Color32::from_rgb(12, 16, 22)`)
3. Draw grid overlay (optional, at world center Y plane, step=5, range 450..550)
4. For each filled voxel:
   a. Frustum cull: project center to NDC, skip if outside `[-1.2, 1.2]` on all axes
   b. Face cull (if enabled): skip faces whose neighbor is also filled
   c. Project 4 corners of each visible face to screen
   d. Push `FaceDraw { points, depth: dist(center, camera), color }`
5. Sort all `FaceDraw` back-to-front by depth (painter's algorithm)
6. Draw faces: `Shape::convex_polygon` with optional wireframe stroke
7. Draw selected voxel outline (yellow, 12 edges)
8. Hit test pointer against faces for click events

### Face Shading (per-face intensity multipliers)

| Face | Normal | Shade |
|---|---|---|
| +X | (1,0,0) | 1.0 |
| -X | (-1,0,0) | 0.75 |
| +Y (top) | (0,1,0) | 1.2 |
| -Y (bottom) | (0,-1,0) | 0.65 |
| +Z | (0,0,1) | 0.9 |
| -Z | (0,0,-1) | 0.8 |

### Render Settings

```rust
pub struct RenderSettings {
    pub face_culling: bool,   // default: true
    pub wireframe: bool,      // default: false
    pub show_grid: bool,      // default: true
    pub voxel_color: Color32, // default: rgb(80, 170, 240)
}
```

---

## Controls

### Mouse

| Input | Action |
|---|---|
| Left drag | Orbit camera (yaw/pitch) |
| Right drag | Pan camera + target together |
| Scroll wheel | Zoom (exponential, clamped to [3, 5000]) |
| Left click on voxel | Select voxel (yellow outline) |
| Right click on voxel | Toggle voxel (fill/clear) |

### Keyboard

| Key | Action |
|---|---|
| `R` | Reset camera to default |
| `G` | Toggle grid overlay |
| `W` / `S` | Move camera + target forward / backward |
| `A` / `D` | Strafe camera + target left / right |
| `Esc` | Deselect voxel |

### UI Sidebar (egui)

- **World:** filled voxel count, sparse memory estimate
- **Camera:** position (x, y, z), FOV slider
- **Voxel editor:** X/Y/Z integer inputs + Set/Clear buttons
- **Render settings:** face culling toggle, wireframe toggle, grid toggle, color picker
- **Performance:** FPS counter, visible face count, render time (ms)

---

## Milestone Status

### M1 — Static Render ✅ Complete
- [x] Window opens with 3D viewport
- [x] Default 10x10x10 cube visible at world center
- [x] Perspective projection (right-handed, glam)
- [x] Face shading (per-face intensity)
- [x] Face culling (skip faces bordering filled neighbors)

### M2 — Camera Interaction ✅ Complete
- [x] Mouse orbit (yaw/pitch with pitch clamp at +-1.45 rad)
- [x] Mouse pan (target + position translate together)
- [x] Scroll zoom (exponential, clamped)
- [x] Keyboard movement (W/A/S/D)
- [x] Camera reset (R key)

### M3 — Voxel Editing ✅ Complete
- [x] Left-click to select voxel (yellow wire outline)
- [x] Right-click to toggle voxel
- [x] Sidebar coordinate editor with Set/Clear buttons
- [x] Frustum culling (skip off-screen voxels)

### M4 — Performance Hardening (partially done)
- [x] Frustum culling implemented
- [x] Face-level culling (hidden-surface neighbor check)
- [x] Render stats: visible faces, visible voxels, render time
- [ ] Dirty flag — only re-sort/re-project on world or camera change
- [ ] LOD or chunking for scenes with >10k filled voxels

---

## Performance Targets

| Metric | Target | Notes |
|---|---|---|
| Frame time (static, default cube) | < 8 ms | 120 fps |
| Frame time (10x10x10 cube visible) | < 16 ms | 60 fps |
| Voxel toggle latency | < 1 ms | HashMap insert/remove |
| Startup time | < 500 ms | |
| Memory (default scene) | < 1 MB | 1000 HashMap entries |

---

## Dependencies

```toml
eframe = "0.31"      # windowing + egui
egui = "0.31"        # immediate-mode UI
glam = "0.29"        # linear algebra
pyo3 = "0.28"        # Python bindings (cdylib target)
rand = "0.9"         # sampling for RL environments
serde = "1.0"        # serialization
serde_json = "1.0"   # JSON output
image = "0.25"       # GIF/PNG output for headless renderer
```

---

## Known Rendering Limitation

The interactive renderer uses a software painter's algorithm (no GPU depth buffer).
For **headless GIF output** this causes view-dependent face artifacts at certain camera angles.

**Current workaround:** fixed camera at `yaw=245deg, pitch=20deg` (see `rendering.md`).
**Long-term fix:** replace headless raster with wgpu offscreen or CPU ray marcher.

The interactive eframe renderer is not affected in practice for normal voxel counts.

---

## Out of Scope (v1)

- Lighting / shadows / ambient occlusion
- Texture mapping
- Physics
- Save / load world to disk
- Networked / multiplayer state
- LOD / chunked streaming for millions of voxels
