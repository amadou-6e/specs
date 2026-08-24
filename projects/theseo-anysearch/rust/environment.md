# Environment Specification

## Environments Overview

| Environment | File | Purpose |
|---|---|---|
| `VoxelEnv` | `environments/voxel_env.rs` | Single-agent block place/remove/noop RL loop |
| `SurfaceEnv` | `environments/surface_env.rs` | Multi-agent greedy pathfinding over geometry surface |
| `MultiAgentVoxelEnv` | `environments/multi_voxel_env.rs` | N agents sharing a single voxel grid; cooperative cursor navigation with optional goals |

---

## `Environment` Trait

```rust
pub trait Environment {
    type Action;
    type Observation;

    fn reset(&mut self, seed: u64) -> Self::Observation;
    fn step(&mut self, action: Self::Action) -> StepResult<Self::Observation>;
}

pub struct StepResult<O> {
    pub observation: O,
    pub reward: f32,
    pub done: bool,
}
```

---

## `SurfaceEnv` (primary environment)

### Purpose

Move N agents from randomized surface start positions to randomized surface goal positions,
navigating around voxel geometry in exterior space only.

### Initialization

Two construction paths:

1. `from_surface(surface_coords, agent_count, max_steps)`
   - Accepts pre-computed surface coords
   - All coords treated as exterior; no flood fill

2. `from_filled_surface(filled_coords, agent_count, max_steps)` ← used in training
   - Accepts raw geometry voxels
   - Computes bounding box with +100 margin on all sides
   - Runs flood-fill to build exterior mask
   - Extracts exterior shell: neighbors of geometry voxels that are exterior

### Exterior Mask

Mask values per voxel in bounding box:
- `0` = unknown / interior (unreachable for agents)
- `1` = geometry obstacle
- `2` = exterior (reachable)

Flood fill seeds from all bounding-box face cells that are not geometry,
then BFS-expands into interior through non-geometry cells.
This ensures agents cannot traverse through the inside of solid geometry.

### Agent State

```rust
pub struct AgentState {
    pub current: Coord,
    pub target:  Coord,
    pub reached: bool,
}
```

### Reset

On `reset(seed)`:
1. Shuffle surface coord list with `StdRng::seed_from_u64(seed)`
2. Assign agent i: `start = coords[i*2]`, `target = coords[i*2 + 1]`
3. Mark all start positions as blocked
4. Clear trail records

### Step

Single action: `SurfaceAction::StepAll` — advances all agents once.

Per agent (if not yet reached):
1. Find 6-connected exterior neighbors of current position
2. Filter: must be exterior AND (not blocked OR == goal)
3. Sort candidates by Manhattan distance to goal
4. Move to best candidate (greedy, no lookahead)
5. Add new position to blocked set + trail_owner map
6. Rewards:
   - Move success: `+0.02`
   - No valid move (stuck): `-0.05`
   - Reached goal: `+1.0`

Done when: `steps >= max_steps` OR all agents reached their goals.

### Blocking Semantics

- Agents leave a trail of blocked cells as they move
- Blocking is persistent for the full episode (until reset)
- An agent can move into its own goal even if blocked by another's trail
- Blocking is used for rendering (trail visualization) and collision avoidance

### Observation

```rust
pub struct SurfaceObservation {
    pub steps_remaining: u32,
    pub reached_agents:  usize,
    pub total_agents:    usize,
    pub agents:          Vec<AgentState>,
}
```

### Pathfinding Algorithm

Current: **greedy Manhattan-distance neighbor selection** (not A*, not BFS).
- Agents can get stuck in local minima against geometry obstacles
- This is intentional for RL training (the agent must learn to escape)

---

## `VoxelEnv`

Simple environment for testing the world interface and RL loop.

### Action Space

```rust
pub enum VoxelAction {
    Place(Coord),
    Remove(Coord),
    Noop,
}
```

### Reward

- `+1.0` when filled voxel count reaches/gets closer to target count
- Small penalty for invalid operations

### Done

Target voxel count reached, or `max_steps` exhausted.

---

---

## `MultiAgentVoxelEnv`

### Purpose

N agents navigate a shared 32³ voxel grid simultaneously. Each agent has its own cursor
and, when geometry is provided, its own start/goal pair sampled from the geometry surface.
Agents cannot move into geometry or agent-filled (trail) cells but may share the same cell.

### Construction

```rust
MultiAgentVoxelEnv::new(
    agent_count: usize,
    max_steps: u32,
    trail_mode: bool,      // auto-fill destination on successful move
    geometry: Vec<Coord>,  // pre-voxelized obstacle cells
    reward_config: RewardConfig,
    grid_size: u16,        // default 32; coords in [1, grid_size]³
)
```

`RewardConfig` (shared with `VoxelEnv`): `step_cost`, `goal_reward`, `distance_shaping`, `collision_cost`.

### Surface computation

`compute_surface_cells(geometry, grid_size)` → exterior shell of geometry:
1. Flood-fill from all bounding-face non-geometry cells (BFS via `reachable_from_boundary`)
2. For each geometry cell, add 6-connected neighbours that are reachable (exterior) to the surface set
3. Returns sorted `Vec<Coord>` used for start/goal sampling

### Agent state

```rust
pub struct AgentEntry {
    pub cursor: Coord,
    pub goal: Option<Coord>,
    pub prev_l2: f32,         // L2 distance to goal at previous step (for shaping)
    pub goal_reached: bool,
}
```

### Reset

On `reset(seed)`:
1. Clear world; re-fill geometry
2. For each agent `i`:
   - If ≥2 surface cells: deterministically sample start `idx_s` and goal `idx_g` using `seed + i*7919` → LCG → Knuth hash into surface list; swap if `(seed+i) % 2 == 0`
   - If <2 surface cells (no geometry): place agents on a fixed grid spread pattern
3. Record `prev_l2` for distance shaping

### Step (26-action)

Action space: `OFFSETS_26` — all 26 {-1,0,1}³ neighbours (excludes no-op).
All agents step simultaneously (`step_all(actions: &[i32])`):

Per agent (skipped if `goal_reached`):
1. Clamp proposed position to `[1, grid_size]³`
2. If destination != current AND cell is not filled → move (and trail-fill if `trail_mode`)
3. If destination == current (boundary hit) → apply `collision_cost`
4. If occupied cell (other agent's trail) → blocked, cursor stays, step consumed (no extra penalty)
5. Reward = `step_cost` ± shaping ± `goal_reward` on arrival

Done when: `steps >= max_steps` OR (any agent has a goal AND all agents with goals have reached them).

### Observation (`MultiStepResult`)

```rust
pub struct MultiStepResult {
    pub steps_remaining: u32,
    pub voxel_count:     usize,          // agent-filled cells (excludes geometry)
    pub cursors:         Vec<Coord>,     // one per agent
    pub goal_distances:  Vec<Option<u32>>, // Manhattan distance to goal, None if no goal
    pub rewards:         Vec<f32>,
    pub done:            bool,
}
```

### Shared helpers (exported from `multi_voxel_env.rs`)

| Helper | Used by |
|---|---|
| `OFFSETS_26` | `multi_voxel_env.rs`, `voxel_env.rs` |
| `DIRS_6` | surface/reachability flood fill |
| `manhattan(a, b)` | goal distance computation; also re-exported to `surface_env.rs` |
| `compute_surface_cells(geometry, grid_size)` | `MultiAgentVoxelEnv::new()` |

---

## Determinism

- `reset(seed)` fully determines start/goal sampling for that episode
- Same seed + same geometry = identical episode
- Agent movement is deterministic (greedy, no random tie-breaking)

---

## Training Configuration

Key parameters passed from Python to Rust via PyO3 DTOs in `bridge/dto.rs`:

| Parameter | CLI flag | Description |
|---|---|---|
| STL file | `--stl` | Geometry to voxelize |
| Scale | `--scale` | Voxelization scale factor |
| Origin | `--origin-x/y/z` | Placement origin in world |
| Agent count | `--agents` | Number of concurrent agents |
| Max steps | `--max-steps` | Steps per episode |
| Iterations | `--iterations` | Training iterations |
| Video every | `--video-every` | GIF export frequency |
| Seed | `--seed` | RNG seed for reproducibility |
| Output dir | `--output-dir` | GIF output directory |
