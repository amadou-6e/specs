# Rendering Specification

## Architecture

There is one rendering pipeline with two consumers:

| Consumer | How it uses the renderer | Output |
|---|---|---|
| `rendering/app/` (eframe) | Calls `renderer.rs`, maps `RgbaBuffer` to `egui::Painter` shapes | Screen (egui window) |
| `bridge/py_bindings.rs` (headless) | Calls `renderer.rs`, encodes `RgbaBuffer` frames to GIF | `.gif` file |

`renderer.rs` knows nothing about egui or GIF encoding. It only produces pixels.

---

## Core Renderer (`rendering/renderer.rs`)

### Output type

```rust
pub struct RgbaBuffer {
    pub width: u32,
    pub height: u32,
    pub pixels: Vec<u8>,   // RGBA, row-major
}
```

### Key types

```rust
pub struct Vertex {
    pub x: f32,
    pub y: f32,
    pub z: f32,   // depth value for z-buffer comparison
}

pub struct FaceDraw {
    pub points: [Vertex; 4],
    pub depth:  f32,          // distance from face centre to camera
    pub color:  [u8; 4],
}
```

`project(coord, camera) -> (f32, f32)` maps a world coord to screen (x, y).
`project_with_depth(coord, camera) -> (f32, f32, f32)` returns screen (x, y) and depth z.

### Pipeline (per frame)

1. Compute MVP = `projection_matrix(aspect) * view_matrix(camera)`
2. Fill buffer with background color `rgb(12, 16, 22)`
3. For each filled voxel in `WorldState`:
   a. Frustum cull: `project` center to NDC, skip if outside `[-1.2, 1.2]`
   b. Face cull: skip faces whose 6-connected neighbor is also filled
   c. `project_with_depth` each visible face's 4 corners → `[Vertex; 4]`
   d. Push `FaceDraw { points, depth: dist(center, camera), color }`
4. Sort all `FaceDraw` back-to-front by depth (painter's algorithm)
5. Rasterize each quad into `RgbaBuffer` pixels
6. Optionally draw ground-plane grid (Y = world center plane, step = 5)

### Face Shading

| Face | Normal | Shade multiplier |
|---|---|---|
| Top (+Y) | (0,1,0) | 1.2 |
| Right (+X) | (1,0,0) | 1.0 |
| Front (+Z) | (0,0,1) | 0.9 |
| Back (-Z) | (0,0,-1) | 0.8 |
| Left (-X) | (-1,0,0) | 0.75 |
| Bottom (-Y) | (0,-1,0) | 0.65 |

### Render Settings

```rust
pub struct RenderSettings {
    pub face_culling: bool,   // default: true
    pub wireframe: bool,      // default: false
    pub show_grid: bool,      // default: true
    pub voxel_color: [u8; 4], // default: rgba(80, 170, 240, 255)
}
```

### Known Limitation

Painter's algorithm is order-dependent and has no per-pixel depth buffer.
For sparse voxel counts this is acceptable. For dense or overlapping geometry,
artifacts may appear at certain camera angles.

**Current workaround for GIF export:** fixed camera at `yaw=245°, pitch=20°`
(confirmed working: `runtime/pathfinding_videos_rust_camflip2/epoch_0001.gif`).

**Long-term fix options:**

| Option | Effort | Correctness |
|---|---|---|
| Keep fixed camera | None | Good for current use case |
| wgpu offscreen pass with depth buffer | High | Correct for all angles |
| CPU ray marcher | Medium | Correct for all angles |

---

## Camera (`rendering/camera.rs`)

Shared by both consumers. Passed into the renderer per frame.

```rust
pub struct Camera {
    pub position: Vec3,
    pub target:   Vec3,
    pub up:       Vec3,
    pub fov_y:    f32,   // degrees
    pub near:     f32,
    pub far:      f32,
}
```

### Interactive defaults

| Property | Value |
|---|---|
| Position | (500.0, 500.0, -200.0) |
| Target | (500.0, 500.0, 500.0) |
| Up | (0.0, 1.0, 0.0) |
| FOV | 60° |
| Near / Far | 1.0 / 2000.0 |
| Orbit sensitivity | 0.01 rad/px |
| Movement speed | 180 units/s |
| Zoom clamp | [3.0, 5000.0] |

### Headless (GIF export) fixed camera

```
yaw   = 245°
pitch = 20°
```

---

## Consumer: eframe App (`rendering/app/`)

1. On each frame, call `renderer::render(world, camera, settings) -> RgbaBuffer`
2. Convert `RgbaBuffer` pixels to `egui::ColorImage`
3. Upload as a texture, display in `egui::CentralPanel`
4. Draw selection outline (yellow wireframe, 12 edges) via `egui::Painter`
5. Hit-test pointer position against projected face list for click/select

### Controls

**Mouse**

| Input | Action |
|---|---|
| Left drag | Orbit camera (yaw/pitch) |
| Right drag | Pan camera + target together |
| Scroll wheel | Zoom (exponential, clamped) |
| Left click on voxel | Select (yellow outline) |
| Right click on voxel | Toggle voxel fill/clear |

**Keyboard**

| Key | Action |
|---|---|
| `R` | Reset camera to default |
| `G` | Toggle grid overlay |
| `W` / `S` | Move forward / backward |
| `A` / `D` | Strafe left / right |
| `Esc` | Deselect voxel |

**Sidebar panels (`ui/panels.rs`)**

- **World:** filled voxel count, sparse memory estimate
- **Camera:** position (x, y, z), FOV slider
- **Voxel editor:** X/Y/Z integer inputs + Set/Clear buttons
- **Render settings:** face culling, wireframe, grid toggles, color picker
- **Performance:** FPS, visible face count, render time (ms)

---

## Consumer: Headless GIF Encoder (`bridge/py_bindings.rs`)

1. For each training step (or every N epochs per `--video-every`):
   a. Call `renderer::render(world, camera, settings) -> RgbaBuffer`
   b. Append `RgbaBuffer` as a frame to an `image::Frame`
2. Write accumulated frames to `epoch_XXXX.gif` via `image` crate

### Output format

| Property | Value |
|---|---|
| Format | Animated `.gif` |
| Frame schedule | Every N epochs (`--video-every N`) |
| Output dir | Configurable (`--output-dir`) |
| Filename pattern | `epoch_XXXX.gif` |

---

## Visibility Rules

1. Geometry voxels render as solid shaded cubes
2. Path-painted voxels render with agent-assigned color
3. Trail blocking persists as painted voxels until epoch reset
4. Empty voxels are invisible

---

## Milestone Status

### M1 — Static Render ✅
- [x] Perspective projection (right-handed, glam)
- [x] Face shading (per-face intensity multipliers)
- [x] Face culling (skip faces bordering filled neighbors)

### M2 — Camera Interaction ✅
- [x] Mouse orbit, pan, zoom
- [x] Keyboard movement (W/A/S/D), reset (R)

### M3 — Voxel Editing ✅
- [x] Click-to-select, right-click toggle
- [x] Sidebar coordinate editor

### M4 — Performance Hardening (partial)
- [x] Frustum culling
- [x] Face-level culling
- [x] Render stats (faces, voxels, ms)
- [ ] Dirty flag — skip re-sort on no world/camera change
- [ ] LOD or chunking for >10k filled voxels

### M5 — Unified Renderer (pending)
- [ ] Extract `RgbaBuffer` output type from `renderer.rs`
- [ ] Remove duplicate headless rasterizer from `bridge/py_bindings.rs`
- [ ] Both `app/` and `bridge/` consume the same `renderer::render()` call

---

## Out of Scope (v1)

- Lighting / shadows / ambient occlusion
- Texture mapping
- Physics
- Save / load world to disk
- wgpu or GPU-accelerated rendering
- LOD / chunked streaming for millions of voxels
