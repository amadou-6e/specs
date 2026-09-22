# Voxel Observation Modes

## Motivation

The current `VoxelEnv` observation (`voxel_count`, `steps_remaining`) gives the agent no
spatial information: it cannot see where it is, what is around it, or where the nearest
filled voxels are. This severely limits what policies can learn. Two richer observation
modes are introduced:

- **Box** — the agent receives the fill state of every cell in a cube centred on the
  cursor position. This provides full local spatial context.
- **Radial** — the agent receives, for each of 27 directions in a 3×3×3 neighbourhood,
  the normalised distance to the nearest filled cell along that ray. Direction (0,0,0)
  reports whether the cursor cell itself is filled. This is a compact, direction-aware
  sensor suited to avoiding redundant placements.

Both modes are computed in Rust for performance and exposed to Python through new
`#[pymethods]` on `PyVoxelEnv`. The Python `VoxelEnv` wrapper selects a mode via a
config key and assembles the final `gymnasium.spaces.Dict` observation.

---

## Observation Modes

### `scalar` (default — current behaviour)

No changes to Rust or Python. Kept for backwards compatibility with existing YAML configs
and integration tests.

```
obs space:
  steps_remaining : Box(1,) in [0, 1]    — steps left / max_steps
  voxel_count     : Box(1,) in [0, ∞)    — absolute filled voxel count
```

---

### `box`

A flattened binary voxel grid of side length `2 * box_radius + 1` centred on the cursor.

```
obs space:
  steps_remaining : Box(1,)  in [0, 1]
  voxel_count     : Box(1,)  in [0, ∞)
  cursor_pos      : Box(3,)  in [0, 1]   — (x, y, z) normalised to [0, 1] within 32³ grid
  local_grid      : Box(N³,) in {0, 1}   — N = 2*box_radius+1, flattened in x-y-z order
```

Cells outside world bounds are treated as empty (0.0).

Config params:

| Key | Type | Default | Notes |
|---|---|---|---|
| `obs_mode` | `str` | `"scalar"` | Set to `"box"` to enable |
| `box_radius` | `int` | `2` | Box side = 2r+1; radius 2 → 5³ = 125 cells |

Sensible values for `box_radius`: 2 (125 cells), 3 (343 cells), 4 (729 cells).

---

### `radial`

For each of the 27 directions in a 3×3×3 neighbourhood (dx, dy, dz ∈ {-1, 0, +1}),
emit a **proximity value** in `[0, 1]` that encodes both whether a filled cell was
found and how close it is.

```
obs space:
  steps_remaining : Box(1,)   in [0, 1]
  voxel_count     : Box(1,)   in [0, ∞)
  cursor_pos      : Box(3,)   in [0, 1]
  ray_hits        : Box(27,)  in [0, 1]  — proximity per direction (see encoding below)
```

#### Encoding

| Situation | Value |
|---|---|
| No hit within `ray_max_len` steps | `0.0` |
| Hit at step `d` (d ∈ 1 … ray_max_len) | `1.0 - (d - 1) / ray_max_len` |
| Direction (0,0,0): cursor cell filled | `1.0` |
| Direction (0,0,0): cursor cell empty | `0.0` |

Properties:
- **0.0 = nothing detected** in that direction (or empty at cursor for (0,0,0)).
- **1.0 = immediately adjacent** (d = 1) or "self filled" for (0,0,0).
- Values strictly decrease with distance: closer hit → higher value.
- A hit at `d = ray_max_len` → `1.0 - (ray_max_len - 1) / ray_max_len` > 0, so
  it is always distinguishable from no-hit (0.0).

Example with `ray_max_len = 16`:

| d | Value |
|---|---|
| 1 (adjacent) | 1.000 |
| 2 | 0.9375 |
| 8 | 0.5625 |
| 16 | 0.0625 |
| no hit | 0.000 |

Direction ordering: sorted lexicographically on (dx+1, dy+1, dz+1), so index maps
deterministically. Index 13 = (0, 0, 0) in a 3×3×3 grid.

Config params:

| Key | Type | Default | Notes |
|---|---|---|---|
| `obs_mode` | `str` | `"scalar"` | Set to `"radial"` to enable |
| `ray_max_len` | `int` | `16` | Maximum steps per ray; no-hit → 0.0 |

---

## Cursor Position

For `box` and `radial` modes the cursor position is always exposed as `cursor_pos: Box(3,)`.
Components are normalised to `[0, 1]` within the 32×32×32 grid:

```
cursor_pos[i] = (coord[i] - 1) / 31.0   for i in {x, y, z}
```

This gives the agent a fixed-size, grid-relative sense of its own location without
exposing absolute world coordinates.

---

## Rust Changes (`py_bindings.rs` + `voxel_env.rs`)

### Two new `#[pymethods]` on `PyVoxelEnv`

```rust
/// Returns a flattened (2*radius+1)³ array.
/// Each element is 1.0 if the world cell at (cursor + offset) is filled, else 0.0.
/// Cells outside world bounds are 0.0.
/// Elements are ordered (x_outer, y_mid, z_inner) — x changes slowest.
pub fn box_obs(&self, radius: u32) -> Vec<f32>

/// Returns a 27-element proximity array, one per direction
/// (dx, dy, dz) ∈ {-1,0,+1}³ sorted lexicographically on (dx+1, dy+1, dz+1).
///
/// Encoding:
///   0.0                              — no hit within max_len (or cursor cell empty for (0,0,0))
///   1.0 - (d - 1) as f32 / max_len  — hit at step d  (d ∈ 1..=max_len)
///   1.0                              — (0,0,0) direction: cursor cell is filled
///
/// Lower value = no detection; higher value = closer hit.
/// A hit at max_len yields 1/max_len (> 0), always distinguishable from no-hit (0.0).
pub fn radial_obs(&self, max_len: u32) -> Vec<f32>
```

`cursor_coord()` is already a private method on `PyVoxelEnv`; both new methods use it
as the centre of the box / origin of the rays. No changes to `VoxelEnv`, `VoxelObservation`,
or the Rust `Environment` trait are required.

### Expose `cursor_pos` as a `#[pymethods]` getter

```rust
/// Returns the current cursor (x, y, z) as a Python tuple.
pub fn cursor_pos(&self) -> (u16, u16, u16)
```

This is called by the Python wrapper to build `cursor_pos` without re-implementing
the grid-to-coord mapping in Python.

---

## Python Changes (`voxel_env.py`)

### New config keys

```yaml
obs_mode: "scalar"    # or "box" or "radial"
box_radius: 2         # only used in "box" mode
ray_max_len: 16       # only used in "radial" mode
```

### `_observation_space()` — returns the correct space based on `obs_mode`

`scalar`:
```python
spaces.Dict({
    "steps_remaining": spaces.Box(0.0, 1.0, (1,), np.float32),
    "voxel_count":     spaces.Box(0.0, np.inf, (1,), np.float32),
})
```

`box`:
```python
n = 2 * box_radius + 1
spaces.Dict({
    "steps_remaining": spaces.Box(0.0, 1.0, (1,),    np.float32),
    "voxel_count":     spaces.Box(0.0, np.inf, (1,), np.float32),
    "cursor_pos":      spaces.Box(0.0, 1.0, (3,),    np.float32),
    "local_grid":      spaces.Box(0.0, 1.0, (n**3,), np.float32),
})
```

`radial`:
```python
spaces.Dict({
    "steps_remaining": spaces.Box(0.0, 1.0,   (1,),  np.float32),
    "voxel_count":     spaces.Box(0.0, np.inf, (1,),  np.float32),
    "cursor_pos":      spaces.Box(0.0, 1.0,   (3,),  np.float32),
    "ray_hits":        spaces.Box(0.0, 1.0,   (27,), np.float32),
})
```

### `_obs_to_numpy(rust_obs)` — assembles the dict from `rust_obs` fields

For `box` and `radial` modes, calls the new Rust methods on `self._rust_env`
(`box_obs(radius)` / `radial_obs(max_len)`) and `cursor_pos()` after every
`reset()` / `step()`.

```python
def _obs_to_numpy(self, rust_obs):
    max_steps = self._config.get("max_steps", 200)
    base = {
        "steps_remaining": np.array([rust_obs.steps_remaining / max(max_steps, 1)], np.float32),
        "voxel_count": np.array([rust_obs.filled], np.float32),
    }
    mode = self._config.get("obs_mode", "scalar")
    if mode == "scalar":
        return base
    cx, cy, cz = self._rust_env.cursor_pos()
    base["cursor_pos"] = np.array(
        [(cx - 1) / 31.0, (cy - 1) / 31.0, (cz - 1) / 31.0], np.float32
    )
    if mode == "box":
        radius = self._config.get("box_radius", 2)
        base["local_grid"] = np.array(self._rust_env.box_obs(radius), np.float32)
    elif mode == "radial":
        max_len = self._config.get("ray_max_len", 16)
        base["ray_hits"] = np.array(self._rust_env.radial_obs(max_len), np.float32)
    return base
```

### Backward compatibility

`obs_mode` defaults to `"scalar"`. Existing YAML configs with no `obs_mode` key continue
to work unchanged. Existing integration tests pass without modification.

---

## Algorithm Compatibility

All three modes return a `gymnasium.spaces.Dict`. The existing RLlib legacy-stack
configuration (`api_stack(enable_rl_module_and_learner=False, ...)` + `model=fcnet`) can
consume flat Dict observations after concatenation — this is already how the current
`scalar` obs works. No changes to trainers or `model=` configs are required.

The `local_grid` key (125 or 343 floats) and `ray_hits` key (27 floats) are
small enough for standard FC nets (`hidden_sizes=[256, 256]`).

---

## Testing

### Unit tests (no Rust required)

`tests/unit/test_environments.py` — new class `TestVoxelEnvObsModes`:

| Test | Assertion |
|---|---|
| `test_box_obs_space_shape` | obs space `local_grid` shape = `(n³,)` for `box_radius=r` |
| `test_radial_obs_space_shape` | obs space `ray_hits` shape = `(27,)` |
| `test_cursor_pos_in_obs_keys` | `cursor_pos` key present in both box and radial dicts |
| `test_scalar_mode_unchanged` | no `cursor_pos` or `local_grid` keys; same as before |
| `test_unknown_mode_raises` | config `obs_mode="bogus"` raises `ValueError` on space build |

These run with `_rust_env = None` (no Rust wheel). The observation dict structure and
space shapes come from Python alone.

### Integration tests (require theseo_core wheel)

`tests/integration/test_voxel_env.py` — new class `TestVoxelEnvObsModesIntegration`:

| Test | Assertion |
|---|---|
| `test_box_obs_values_in_range` | all `local_grid` elements ∈ {0.0, 1.0} |
| `test_box_obs_shape_after_reset` | `local_grid.shape == ((2r+1)**3,)` |
| `test_box_obs_shape_after_step` | same shape returned from `step()` |
| `test_radial_obs_values_in_range` | all `ray_hits` ∈ [0, 1] |
| `test_radial_obs_shape` | `ray_hits.shape == (27,)` |
| `test_cursor_pos_normalised` | all `cursor_pos` ∈ [0, 1] |
| `test_cursor_pos_changes_after_step` | `cursor_pos` differs after a step |
| `test_place_action_visible_in_box_obs` | after `Place` at cursor: corresponding cell in `local_grid` = 1.0 on next reset/step |
| `test_direction_0_0_0_filled_is_1` | `ray_hits[13]` = 1.0 after filling cursor cell |
| `test_direction_0_0_0_empty_is_0` | `ray_hits[13]` = 0.0 when cursor cell is empty |
| `test_adjacent_hit_proximity_is_1` | fill cell adjacent to cursor; its ray value = 1.0 |
| `test_no_hit_proximity_is_0` | empty world; all `ray_hits` values = 0.0 |

### Rust unit tests (`voxel_env.rs` / `py_bindings.rs`)

| Test | Assertion |
|---|---|
| `box_obs_empty_world` | all zeros for empty world |
| `box_obs_single_filled_at_cursor` | centre element = 1.0 |
| `box_obs_radius_0_single_cell` | length = 1; equals is_filled(cursor) |
| `box_obs_out_of_bounds_is_zero` | cells outside [1,32] grid = 0.0 |
| `radial_obs_empty_world_all_zeros` | all 27 values = 0.0 (no hits anywhere) |
| `radial_obs_self_cell_filled` | index 13 = 1.0 when cursor cell is filled |
| `radial_obs_self_cell_empty` | index 13 = 0.0 when cursor cell is empty |
| `radial_obs_adjacent_hit` | direction (+1,0,0) filled at cursor+1 → value = 1.0 (d=1, fully proximate) |
| `radial_obs_distant_hit` | hit at d=8, max_len=16 → value = 1.0 - 7.0/16.0 = 0.5625 |
| `radial_obs_hit_at_max_len` | hit at d=max_len → value = 1/max_len > 0.0 (distinguishable from no-hit) |
| `radial_obs_no_hit_is_zero` | direction with no hit within max_len → exactly 0.0 |
| `radial_obs_length_is_27` | always exactly 27 elements |

---

## Implementation Order

1. **Rust** — add `box_obs`, `radial_obs`, `cursor_pos` to `PyVoxelEnv` in `py_bindings.rs`; add Rust unit tests
2. **Rust** — rebuild wheel: `VIRTUAL_ENV=.venv .venv/Scripts/maturin.exe develop`
3. **Python** — update `VoxelEnv._observation_space()` and `_obs_to_numpy()`; add unit + integration tests
4. **Verify** — `pytest tests/unit/` (189+ pass), `pytest tests/integration/ -m integration` (34+ pass)
5. **RLlib** — no trainer changes needed; existing YAML configs with `obs_mode: box` or `obs_mode: radial` will work automatically via `VoxelEnv` config pass-through
