# Rust Testing Specification

## Approach

Rust tests live alongside the code they test using `#[cfg(test)]` modules.
Integration tests that exercise multiple modules together live in `rust/tests/`.

Run all tests:
```bash
cd theseo_anysearch/core
cargo test
```

Run a specific module's tests:
```bash
cargo test world::
cargo test ingest::
cargo test environments::
```

---

## Unit Tests — `world/`

### `world/state.rs`

| Test | Assertion |
|---|---|
| `set_block_inserts` | `is_filled` returns true after `set_block` |
| `set_block_replaces` | Second `set_block` on same coord does not grow `len()` |
| `remove_block_clears` | `is_filled` returns false after `remove_block` |
| `remove_block_not_found` | `remove_block` on absent coord returns `WorldError::NotFound` |
| `update_block_mutates` | `get_block` reflects field change after `update_block` |
| `update_block_not_found` | `update_block` on absent coord returns `WorldError::NotFound` |
| `out_of_bounds_set` | `set_block` with coord >= 1000 returns `WorldError::OutOfBounds` |
| `out_of_bounds_remove` | `remove_block` with coord >= 1000 returns `WorldError::OutOfBounds` |
| `toggle_fill` | `toggle` on empty coord fills; `toggle` on filled coord clears |
| `iter_filled_count` | `iter_filled().count()` matches `len()` |
| `estimated_sparse_bytes` | Returns `len() * size_of::<(Coord, Block)>()` |
| `default_world_has_cube` | `WorldState::default().len() == 1000` |
| `empty_world_is_empty` | `WorldState::new().len() == 0` |

### `world/api.rs`

| Test | Assertion |
|---|---|
| `in_bounds_true` | `(0, 0, 0)` and `(999, 999, 999)` are in bounds |
| `in_bounds_false` | `(1000, 0, 0)` is out of bounds |

---

## Unit Tests — `world/ingest/`

### `ingest/stl.rs`

| Test | Assertion |
|---|---|
| `parse_valid_single_triangle` | One triangle, 3 vertices parsed correctly |
| `parse_valid_two_triangles` | Six vertices → two triangles |
| `parse_ignores_non_vertex_lines` | `solid`, `facet normal`, `endfacet` lines skipped |
| `parse_empty_input` | Returns `InvalidFormat` (vertex count < 3) |
| `parse_vertex_count_not_multiple_of_3` | 4 vertices → `InvalidFormat` |
| `parse_bad_float` | `vertex 1.0 abc 3.0` → `InvalidFormat` |
| `parse_missing_coord` | `vertex 1.0 2.0` (only 2 tokens) → `InvalidFormat` |

### `ingest/voxelize.rs`

| Test | Assertion |
|---|---|
| `single_triangle_produces_voxels` | Non-empty result for a valid triangle at origin |
| `scale_increases_voxel_count` | Higher scale produces more voxels (broader sampling) |
| `origin_shifts_placement` | All coords offset by origin |
| `out_of_bounds_points_discarded` | Negative coords or coords >= 1000 not in result |
| `solid_fill_fills_interior` | A closed cube mesh produces interior voxels |
| `empty_mesh_returns_empty` | `voxelize_mesh` on zero-triangle mesh returns empty vec |
| `no_duplicates` | No two `BlockPlacement` entries share the same coord |

---

## Unit Tests — `environments/`

### `environments/traits.rs`

`StepResult` and `Environment` trait — no logic to test directly; covered by env tests.

### `environments/voxel_env.rs`

| Test | Assertion |
|---|---|
| `reset_returns_observation` | `reset(42)` returns `VoxelObservation` with `filled == world.len()` |
| `noop_step_no_change` | `step(VoxelAction::Noop)` does not change world, reward == 0 |
| `place_step_fills` | `step(VoxelAction::Place(coord))` fills coord; reward changes |
| `remove_step_clears` | `step(VoxelAction::Remove(coord))` clears coord |
| `done_at_max_steps` | `done == true` after `max_steps` steps |
| `deterministic_reset` | Two `reset(42)` calls produce identical observations |

### `environments/surface_env.rs`

| Test | Assertion |
|---|---|
| `from_filled_surface_builds_exterior` | Surface coords are all marked exterior in mask |
| `reset_assigns_start_goal` | Each agent gets distinct start and goal from surface |
| `step_all_advances_agents` | Agent positions change after `step(SurfaceAction::StepAll)` |
| `reached_agent_counted` | Agent at goal coord increments `reached_agents` |
| `trail_blocks_cells` | Cells an agent has visited are blocked for other agents |
| `goal_reachable_through_own_trail` | Agent can step into its own goal even if blocked |
| `done_when_all_reached` | `done == true` when `reached_agents == total_agents` |
| `done_at_max_steps` | `done == true` after `max_steps` steps even if not all reached |
| `deterministic_same_seed` | Two episodes with same seed and geometry are identical |
| `different_seeds_differ` | Different seeds produce different start/goal assignments |
| `reward_success` | Reaching goal yields reward >= 1.0 |
| `reward_stuck` | No valid move yields negative reward |

---

## Unit Tests — `rendering/`

### `rendering/camera.rs`

| Test | Assertion |
|---|---|
| `view_matrix_not_identity` | `view_matrix(camera)` differs from identity |
| `projection_matrix_fov` | FOV change produces different projection |
| `orbit_changes_position` | Applying orbit delta changes camera position |
| `zoom_clamped` | Zoom beyond [3.0, 5000.0] is clamped |

### `rendering/renderer.rs`

| Test | Assertion |
|---|---|
| `render_empty_world` | Returns `RgbaBuffer` filled with background color only |
| `render_single_voxel` | At least some pixels differ from background |
| `buffer_dimensions` | `pixels.len() == width * height * 4` |
| `face_culling_reduces_faces` | `face_culling: true` produces fewer faces than `false` |

Rendering tests do not assert exact pixel values — they assert structural properties (dimensions, non-empty output, culling counts).

---

## Integration Tests (`theseo_anysearch/core/tests/`)

Integration tests exercise multi-module flows without going through PyO3.

### `tests/ingest_to_world.rs`

```rust
// Parse STL -> voxelize -> insert into world -> verify count
fn round_trip_single_triangle()
fn round_trip_closed_mesh_is_solid()
```

### `tests/ingest_to_env.rs`

```rust
// Parse STL -> voxelize -> build SurfaceEnv -> run full episode
fn surface_env_from_stl_completes()
fn surface_env_deterministic_across_runs()
```

---

## What Is Not Tested (v1)

| Area | Reason |
|---|---|
| GIF output correctness | Pixel-exact GIF comparison is brittle; assert file is non-empty instead |
| Render integration test | `tests/render_smoke.rs` not yet written |
| eframe app (interactive viewer) | Requires a display; out of scope for headless CI |
| Binary STL parsing | Not implemented |
| PyO3 boundary functions | Covered by Python integration tests that import `theseo_core` |

---

## CI Requirements

- `cargo test` must pass with zero failures
- `cargo clippy -- -D warnings` must produce no warnings
- `cargo fmt --check` must report no formatting differences
