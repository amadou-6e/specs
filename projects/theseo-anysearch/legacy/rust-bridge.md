---
title: Imported Bridge Specification
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

The historical bridge layout and DTO catalog predate the current cross-language architecture and may describe planned rather than current exports. Current authority: [architecture README.md](../architecture/README.md).
No unverified historical claim is promoted by this move. Its original authority
ended no later than this classification under specs issue #110; an earlier
supersession date has not been established. The source revision remains available
in Git history.

## Archived material

# Bridge Specification

## Purpose

The bridge is the **only layer Python calls directly**.
It owns three concerns:

1. **DTOs** (`dto.rs`) — plain Rust structs that carry input data from Python into the Rust simulation
2. **Serialisation structs** (`py_bindings.rs`) — serde output types sent back to Python as JSON
3. **PyO3 exported functions** (`py_bindings.rs`) — thin wrappers that parse inputs, call into `world/`, `environments/`, `rendering/`, and serialise results

No business logic lives here that belongs elsewhere.
The headless renderer currently embedded in `py_bindings.rs` is an exception — it is slated for extraction to `rendering/renderer.rs` (M5 milestone).

---

## DTOs (`bridge/dto.rs`)

Plain `Clone + Debug` structs. Not `#[pyclass]` — they are constructed inside the `#[pyfunction]` wrappers from flat Python arguments.

```rust
pub struct GeometrySubmission {
    pub name:      String,
    pub stl_ascii: String,       // full ASCII STL file contents
    pub origin:    Coord,        // world-space placement origin (u16, u16, u16)
    pub scale:     f32,          // voxelization scale factor (STL units → voxels)
}

pub struct EnvConfig {
    pub max_steps: u32,          // maximum steps per episode
}
```

### Planned addition (pre-M5)

A `TrainConfig` DTO should be added to bundle the per-run training parameters
currently passed as individual arguments to `py_train_videos`:

```rust
pub struct TrainConfig {
    pub agent_count:      usize,
    pub max_steps:        u32,
    pub iterations:       u32,
    pub video_every:      u32,
    pub output_dir:       String,
    pub camera_yaw_deg:   f32,
    pub camera_pitch_deg: f32,
    pub seed:             u64,
}
```

---

## Serialisation Structs (`bridge/py_bindings.rs`)

These types are `#[derive(Serialize)]` and returned to Python as JSON strings.
They are not `#[pyclass]`; Python receives them via `serde_json::to_string`.

```rust
pub struct PaintVoxel {
    pub coord: (u16, u16, u16),
    pub owner: usize,             // index into agent list
}

pub struct EpisodeStep {
    pub step:           u32,
    pub agents:         Vec<AgentState>,
    pub reached_agents: usize,
    pub new_paints:     Vec<PaintVoxel>,  // voxels painted for the first time this step
}

pub struct EpisodeTrace {
    pub triangles:       usize,
    pub filled:          usize,
    pub surface:         usize,
    pub total_agents:    usize,
    pub max_steps:       u32,
    pub steps_executed:  u32,
    pub reached_agents:  usize,
    pub total_reward:    f32,
    pub geometry_coords: Vec<(u16, u16, u16)>,
    pub surface_coords:  Vec<(u16, u16, u16)>,
    pub trace:           Vec<EpisodeStep>,
}

pub struct EpochSummary {
    pub epoch:          u32,
    pub reached:        usize,
    pub total_agents:   usize,
    pub steps:          u32,
    pub reward:         f32,
    pub painted_voxels: usize,
}

pub struct TrainingSummary {            // was: RustVideoRunSummary
    pub status:       String,
    pub iterations:   u32,
    pub video_every:  u32,
    pub output_dir:   String,
    pub summary_file: String,
}
```

`TrainingSummary` is the JSON object returned by `py_train_videos`.
`EpisodeTrace` is the JSON object returned by `py_surface_env_trace`.
`EpochSummary` items are accumulated into the `training_summary_rust.json` file written to disk.

---

## PyO3 Exported Functions

All functions use the `py_` prefix (marks the Python-facing boundary when reading Rust code).
All return `PyResult<String>` — either a short summary string or a serialised JSON string.
Errors are propagated as `PyRuntimeError`.

### Module registration

```rust
#[pymodule]
pub fn theseo_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_submit_geometry, m)?)?;
    m.add_function(wrap_pyfunction!(py_world_smoke_test, m)?)?;
    m.add_function(wrap_pyfunction!(py_surface_env_from_stl, m)?)?;
    m.add_function(wrap_pyfunction!(py_surface_env_trace, m)?)?;
    m.add_function(wrap_pyfunction!(py_train_videos, m)?)?;
    m.add_function(wrap_pyfunction!(py_render_stl, m)?)?;
    m.add_function(wrap_pyfunction!(py_render_cube, m)?)?;
    Ok(())
}
```

### Function catalogue

| Function | Was | Returns | Purpose |
|---|---|---|---|
| `py_submit_geometry` | (unchanged) | summary `String` | Parse STL, voxelize, run one VoxelEnv step; smoke test for the geometry → world pipeline |
| `py_world_smoke_test` | `py_world_interface_poc` | summary `String` | Exercise set/update/remove on WorldState; temporary until Rust unit tests cover this |
| `py_surface_env_from_stl` | `py_surface_pathfinding_from_stl` | summary `String` | Full episode rollout (greedy, no rendering); returns agent counts and reward |
| `py_surface_env_trace` | `py_surface_pathfinding_trace_from_stl` | JSON `EpisodeTrace` | Full episode rollout with per-step recording; used by the Python training loop for trajectory analysis |
| `py_train_videos` | `py_train_pathfinding_rust_videos` | JSON `TrainingSummary` | Run N iterations of greedy episodes, render a GIF every `video_every` iterations, write `training_summary_rust.json` |
| `py_render_stl` | `py_render_stl_test` | summary `String` | Render voxelised STL geometry (no agents) to a GIF; visual debugging tool |
| `py_render_cube` | `py_render_cube_test` | summary `String` | Render a solid NxNxN cube to a GIF; visual debugging tool |

### Signature reference

```rust
#[pyfunction]
pub fn py_submit_geometry(
    name: String, stl_ascii: String,
    origin_x: u16, origin_y: u16, origin_z: u16,
    scale: f32, max_steps: u32,
) -> PyResult<String>

#[pyfunction]
pub fn py_world_smoke_test() -> PyResult<String>

#[pyfunction]
pub fn py_surface_env_from_stl(
    stl_ascii: String,
    origin_x: u16, origin_y: u16, origin_z: u16,
    scale: f32, agent_count: usize, max_steps: u32, seed: u64,
) -> PyResult<String>

#[pyfunction]
pub fn py_surface_env_trace(
    stl_ascii: String,
    origin_x: u16, origin_y: u16, origin_z: u16,
    scale: f32, agent_count: usize, max_steps: u32, seed: u64,
) -> PyResult<String>   // JSON-encoded EpisodeTrace

#[pyfunction]
pub fn py_train_videos(
    stl_ascii: String,
    origin_x: u16, origin_y: u16, origin_z: u16,
    scale: f32, agent_count: usize, max_steps: u32,
    seed: u64, iterations: u32, video_every: u32,
    output_dir: String,
    camera_yaw_deg: f32, camera_pitch_deg: f32,
    disable_culling: bool,
) -> PyResult<String>   // JSON-encoded TrainingSummary

#[pyfunction]
pub fn py_render_stl(
    stl_ascii: String,
    origin_x: u16, origin_y: u16, origin_z: u16,
    scale: f32, output_path: String,
    camera_yaw_deg: f32, camera_pitch_deg: f32,
) -> PyResult<String>

#[pyfunction]
pub fn py_render_cube(
    output_path: String, cube_size: u16,
    origin_x: u16, origin_y: u16, origin_z: u16,
    camera_yaw_deg: f32, camera_pitch_deg: f32,
) -> PyResult<String>
```

---

## Headless Renderer (current state vs. target)

Currently, `py_bindings.rs` contains the entire headless software rasterizer:

| Component | Lives in | Should live in (post-M5) |
|---|---|---|
| `CameraAngles` | `py_bindings.rs` | `rendering/camera.rs` |
| `Vertex` (was `ProjVertex`) | `py_bindings.rs` | `rendering/renderer.rs` |
| `project`, `project_with_depth` | `py_bindings.rs` | `rendering/renderer.rs` |
| Face draw, z-buffer rasterizer | `py_bindings.rs` | `rendering/renderer.rs` |
| GIF frame encoder | `py_bindings.rs` | `rendering/renderer.rs` or `bridge/` |

Post-M5, `py_bindings.rs` calls `renderer::render(world, camera, settings) -> RgbaBuffer`
and `bridge/` encodes the buffer to GIF frames.
The `py_bindings.rs` file itself should shrink to thin dispatch functions only.

---

## Invariants

1. `py_bindings.rs` never directly mutates a live `WorldState` across calls — each `py_` function constructs its own local world
2. All `py_` functions are stateless — no module-level mutable state
3. JSON output keys are `snake_case`, matching Python attribute names
4. Errors propagate as `PyRuntimeError` with a human-readable message — no panics escape the boundary
