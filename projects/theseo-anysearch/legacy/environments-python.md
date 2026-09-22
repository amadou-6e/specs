# Python Environments Specification

## Purpose

Wrap the Rust-backed RL environments (exposed via PyO3) behind standard Python
environment APIs so that RLlib, Ray Tune, and any other RL framework can consume
them without knowing anything about Rust or PyO3.

---

## Two APIs, Two Subfolders

| Subfolder | API | Use case |
|---|---|---|
| `environments/gymnasium/` | `gymnasium.Env` | Single-agent environments, RLlib `SingleAgentEnvRunner` |
| `environments/pettingzoo/` | `pettingzoo.ParallelEnv` | Multi-agent environments, RLlib `MultiAgentEnvRunner` |

---

## `gymnasium/base.py` — Abstract RustGymnasiumEnv

```python
class RustGymnasiumEnv(gymnasium.Env, ABC):
    """
    Base for all single-agent Gymnasium wrappers over PyO3-bound Rust environments.
    Subclasses provide observation_space, action_space, and the PyO3 call pattern.
    """

    @abstractmethod
    def _build_rust_env(self, config: dict) -> Any: ...
        # instantiates the Rust environment via PyO3 (e.g. theseo_core.VoxelEnv(...))

    @abstractmethod
    def _observation_space(self) -> gymnasium.Space: ...

    @abstractmethod
    def _action_space(self) -> gymnasium.Space: ...

    def reset(self, *, seed=None, options=None) -> tuple[ObsType, dict]: ...
        # calls rust_env.reset(seed)
        # converts Rust observation struct -> numpy dict

    def step(self, action) -> tuple[ObsType, float, bool, bool, dict]: ...
        # encodes action -> Rust action type
        # calls rust_env.step(action)
        # returns (obs, reward, terminated, truncated, info)
```

### Observation and action encoding

Rust observations are `#[pyclass]` structs returned from PyO3.
The base class converts them to flat numpy arrays or dicts of arrays
so they match the declared `observation_space`.

Rust actions are encoded from numpy/int back to Rust enum variants
via the bridge DTOs before being passed to `rust_env.step()`.

---

## `gymnasium/voxel_env.py` — VoxelEnv Wrapper

| Property | Value |
|---|---|
| Rust env | `theseo_core.VoxelEnv` |
| Action space | `Discrete(26)` — all 26 face/edge/corner neighbors in {-1,0,1}³ |

Observation space depends on `obs_mode`:

| `obs_mode` | Observation keys |
|---|---|
| `scalar` | `steps_remaining: Box(1,)`, `voxel_count: Box(1,)` |
| `box` | `steps_remaining: Box(1,)`, `voxel_count: Box(1,)`, `cursor_pos: Box(3,)`, `local_grid: Box(N³,)` [, `goal_distance: Box(1,)`] |
| `radial` | `steps_remaining: Box(1,)`, `voxel_count: Box(1,)`, `cursor_pos: Box(3,)`, `ray_hits: Box(27,)` [, `goal_distance: Box(1,)`] |
| `hierarchical_box` | `steps_remaining: Box(1,)`, `cursor_pos: Box(3,)`, `local_grid_r{i}: Box(N_i³,)` for each radius in `box_radii` |

`N = 2 * box_radius + 1`. `goal_distance` is included when geometry is set.

---

## `pettingzoo/base.py` — Abstract RustParallelEnv

```python
class RustParallelEnv(pettingzoo.ParallelEnv, ABC):
    """
    Base for all multi-agent PettingZoo wrappers over PyO3-bound Rust environments.
    Implements the PettingZoo parallel API: all agents act and observe simultaneously.
    """

    @abstractmethod
    def _build_rust_env(self, config: dict) -> Any: ...

    @abstractmethod
    def _observation_space(self, agent: str) -> gymnasium.Space: ...

    @abstractmethod
    def _action_space(self, agent: str) -> gymnasium.Space: ...

    def reset(self, seed=None, options=None) -> tuple[dict[AgentID, ObsType], dict]: ...
        # calls rust_env.reset(seed)
        # returns {agent_id: obs} for all agents

    def step(self, actions: dict[AgentID, ActionType]) -> tuple[
        dict[AgentID, ObsType],
        dict[AgentID, float],
        dict[AgentID, bool],
        dict[AgentID, bool],
        dict[AgentID, dict],
    ]: ...
        # encodes actions dict -> Rust StepAll action
        # calls rust_env.step(action)
        # fans out step result to per-agent dicts

    @property
    def agents(self) -> list[AgentID]: ...
        # returns currently active agent IDs (removed when done=True)

    @property
    def possible_agents(self) -> list[AgentID]: ...
        # returns all agent IDs for the episode (fixed at reset)
```

---

## `pettingzoo/multi_voxel_env.py` — MultiVoxelEnv Wrapper

| Property | Value |
|---|---|
| Rust env | `theseo_core.PyMultiVoxelEnv` |
| Ray env ID | `"MultiVoxelEnv-v0"` (registered via `register_with_ray()`) |
| Agent IDs | `["agent_0", ..., "agent_{N-1}"]` where N = `agent_count` (default 2) |
| Observation space (per agent) | `Dict(cursor_pos: Box(3,), face_neighbors: Box(6,), local_grid: Box(N³,), ray_cast: Box(27,), goal_distance: Box(1,), goal_direction: Box(3,))` |
| Action space (per agent) | `Discrete(26)` — all 26 face/edge/corner neighbors in {-1,0,1}³ |
| Termination | Episode ends when `steps_remaining` reaches 0, or all agents reach their goals |

N agents share a single configurable voxel grid. Each agent has its own cursor and (when geometry is provided via `geometry_boxes`) its own start/goal pair derived from the geometry surface. Agents cannot move into geometry or filled cells, but may co-exist on the same cell. Trail mode auto-fills each agent's destination on successful moves.

### Config keys

| Key | Type | Default | Description |
|---|---|---|---|
| `agent_count` | `int` | `2` | Number of concurrent agents |
| `max_steps` | `int` | `200` | Max steps per episode |
| `trail_mode` | `bool` | `False` | Auto-fill destination cell on successful move |
| `geometry_boxes` | `list[tuple[int,int,int,int,int,int]]` | `None` | Axis-aligned boxes `[xmin,ymin,zmin,xmax,ymax,zmax]` defining obstacles; also determines start/goal surface sampling |
| `grid_size` | `int` | `32` | Side length of the cubic grid; coords in [1, grid_size]³ |
| `step_cost` | `float` | `-0.01` | Reward per step |
| `goal_reward` | `float` | `1.0` | Reward for reaching goal |
| `distance_shaping` | `float` | `0.1` | Coefficient for L2 distance shaping |
| `collision_cost` | `float` | `0.0` | Extra penalty for boundary collision |

### Internal helpers

`_fanout_obs()` splits a single Rust `MultiStepResult.observation` into per-agent dicts, normalising coordinates and goal distances.
`_encode_actions()` encodes the PettingZoo `actions: dict` → `list[int]` in `possible_agents` order.

---

## `pettingzoo/surface_env.py` — SurfaceEnv Wrapper

| Property | Value |
|---|---|
| Rust env | `theseo_core.SurfaceEnv` |
| Agent IDs | `["agent_0", "agent_1", ..., "agent_N-1"]` |
| Observation space (per agent) | `Dict(steps_remaining: Box(1,), position: Box(3,), target: Box(3,), reached: Discrete(2))` |
| Action space (per agent) | `Discrete(1)` — single action `StepAll` (all agents advance together) |
| Termination | Agent marked done when `reached=True`; episode ends when all done or `max_steps` exceeded |

### Action space note

`SurfaceEnv` has a single joint action `StepAll` — all agents move simultaneously
per step. The action space is formally `Discrete(1)` per agent. The policy learns
*which agent positions to occupy* through the observation, not through discrete action choices.
A future extension would expose directional actions per agent.

---

## Registration

Environments register themselves with RLlib via class-level `register_with_ray()` calls. `environments/__init__.py` triggers default registrations:

```python
from ray.tune.registry import register_env
from .gymnasium.voxel_env import VoxelEnv
from .pettingzoo.surface_env import SurfaceEnv
from .pettingzoo.multi_voxel_env import MultiVoxelEnv

register_env("voxel_env",       lambda cfg: VoxelEnv(cfg))
register_env("surface_env",     lambda cfg: SurfaceEnv(cfg))
register_env("MultiVoxelEnv-v0", lambda cfg: MultiVoxelEnv(cfg))
```

---

## Config passthrough (`EnvConfig`)

Environment constructors accept a `config: dict` sourced from `AlgorithmConfig.env_config`.
All values originate from `models.EnvConfig` and are passed through without mutation.

### Geometry

| Key | Type | Default | Description |
|---|---|---|---|
| `stl_path` | `Path \| None` | `None` | Single STL geometry file |
| `scale` | `float` | `1.0` | Voxelization scale factor |
| `geometry_boxes` | `list[list[int]] \| None` | `None` | Fixed axis-aligned box obstacles `[[xmin,ymin,zmin,xmax,ymax,zmax], ...]` |
| `grid_size` | `int` | `32` | Side length of the cubic grid |

### Agents / episode

| Key | Type | Default | Description |
|---|---|---|---|
| `agent_count` | `int` | `4` | Number of concurrent agents |
| `max_steps` | `int` | `200` | Maximum steps per episode |
| `seed` | `int` | `42` | RNG seed (overridden per episode by RLlib) |
| `trail_mode` | `bool` | `True` | Auto-fill visited cells |

### Observations

| Key | Type | Default | Description |
|---|---|---|---|
| `obs_mode` | `"scalar" \| "box" \| "radial" \| "hierarchical_box"` | `"scalar"` | Observation modality |
| `box_radius` | `int` | `2` | Half-width of local grid (N = 2r+1) |
| `box_radii` | `list[int] \| None` | `None` | Radii for `hierarchical_box` mode |
| `ray_max_len` | `int` | `16` | Max ray length for `radial` mode |

### Rewards

| Key | Type | Default | Description |
|---|---|---|---|
| `step_cost` | `float` | `-0.01` | Per-step reward penalty |
| `goal_reward` | `float` | `1.0` | Bonus on reaching goal |
| `distance_shaping` | `float` | `0.0` | Potential-based shaping coefficient |
| `collision_cost` | `float` | `0.0` | Extra penalty on blocked moves |
| `distance_metric` | `"euclidean" \| "manhattan"` | `"euclidean"` | Distance metric for shaping |

### Training diversity

| Key | Type | Default | Description |
|---|---|---|---|
| `stl_paths` | `list[Path] \| None` | `None` | Pool of STL maps; one sampled per episode |
| `scale_range` | `list[float] \| None` | `None` | `[min, max]` — voxelization scale sampled per episode |
| `scale_variants_per_map` | `int` | `4` | Re-voxelizations per STL at different scales |
| `geometry_pool_size` | `int` | `0` | If > 0: use this many procedural random-box geometries |

### Observation augmentation

Applied to `local_grid` at every step during rollout collection.

| Key | Type | Default | Description |
|---|---|---|---|
| `obs_noise_prob` | `float` | `0.0` | Bit-flip probability per voxel |
| `obs_cutout_count` | `int` | `0` | Number of random cuboid regions zeroed out |
| `obs_cutout_size` | `int` | `1` | Max side length of each cutout cube |
| `output_dir` | `str` | GIF output directory |

---

## Invariants

1. Environments never hold mutable Python state across `reset()` calls — all state lives in the Rust env
2. `observation_space` and `action_space` are fixed at construction time and do not change per episode
3. Observations are always numpy arrays or dicts of numpy arrays — no raw Python objects cross the boundary
4. `reset(seed=s)` with the same seed and geometry produces an identical episode (guaranteed by Rust)
