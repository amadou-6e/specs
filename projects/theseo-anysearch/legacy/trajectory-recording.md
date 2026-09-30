---
title: Historical Trajectory recording
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

> Historical source; not an authoritative current specification.

# Trajectory Recording

Trajectory recording serialises the per-step state of VoxelEnv eval episodes to
JSON so that any recorded iteration can be inspected and replayed.

---

## Goals

| Goal | Description |
|---|---|
| **Best-epoch save** | After every iteration keep a single `best.json` for the best-performing iteration seen so far (highest `episode_reward_mean`). |
| **Periodic save** | Also save every i-th iteration unconditionally (controlled by `trajectory_every`). |
| **Replay** | Any saved `.json` file encodes full cursor + action + reward per step, readable by inspection tooling or the `theseo-viewer` eframe app. |
| **VoxelEnv support** | Captures trajectories from `VoxelEnv` via `collect_eval_episode()` run in the main process after each training iteration. |

---

## Configuration

```yaml
training:
  trajectory_every: 10      # save every N-th iteration; 0 = disabled
  best_trajectory: true     # also save best-so-far; default true
```

| `trajectory_every` | `best_trajectory` | Effect |
|---|---|---|
| `0` | `false` | No trajectory files written |
| `0` | `true` | Only `best.json` updated when a new best is seen |
| `10` | `false` | Periodic saves only (`iter_000010.json`, …) |
| `10` | `true` | Periodic saves + `best.json` (default behaviour) |

---

## Output Files

```
{run_dir}/
└── trajectories/
    ├── iter_000001.json      # saved when iteration % trajectory_every == 0
    ├── iter_000002.json
    ├── best.json             # copy of the best iteration so far (by episode_reward_mean)
    └── best_meta.json        # {"iteration": 4, "episode_reward_mean": -0.40}
```

`best.json` is overwritten in-place whenever `episode_reward_mean` improves.
`best_meta.json` is updated at the same time so tooling can display which
iteration it came from without parsing the full trajectory.

---

## JSON Schema

Each trajectory file is a JSON object with the following structure:

```json
{
  "experiment_name": "quick-demo",
  "run_id": "ffb23f26",
  "iteration": 4,
  "episode_reward_mean": -0.404,
  "grid_size": 32,
  "agent_count": 1,
  "max_steps": 50,
  "obs_mode": "scalar",
  "episode": {
    "total_reward": 2.76,
    "steps_taken": 20,
    "success": true,
    "init_filled": [[1, 1, 1], ...],
    "steps": [
      {
        "step": 0,
        "action": 2,
        "reward": -0.11,
        "done": false,
        "cursor_x": 1,
        "cursor_y": 1,
        "cursor_z": 1,
        "voxel_count": 0,
        "placed": false
      },
      ...
    ]
  }
}
```

### Field notes

- `init_filled`: list of `[x, y, z]` voxel coordinates filled at episode start (from `PyVoxelEnv.filled_voxels()`)
- `action`: `0=+X`, `1=-X`, `2=+Y`, `3=-Y`, `4=+Z`, `5=-Z`
- `voxel_count`: total filled voxels **after** this step
- `placed`: `true` if a new voxel was filled this step (trail mode auto-fills destination on successful move)
- `success`: `true` if the episode ended before `max_steps` (agent reached the goal)

---

## `collect_eval_episode`

Module: `theseo_anysearch/experiments/trajectory.py`

```python
def collect_eval_episode(algo, env_config: dict) -> VoxelEpisodeData:
    """
    Run one evaluation episode in the main process using the trained policy.
    Creates a fresh VoxelEnv directly (not through Ray workers).
    Falls back to action=0 (+X) if compute_single_action is unavailable.
    """
```

This function is called from the `on_iteration_end` hook in `ExperimentRunner`
after each training iteration. It runs synchronously in the main process, so it
adds a small overhead (~one episode length) to each iteration. For short episodes
(`max_steps=50`) this is negligible.

---

## `TrajectoryWriter` Class

Module: `theseo_anysearch/experiments/trajectory.py`

```python
class TrajectoryWriter:
    def __init__(
        self,
        store: OutputStore,
        trajectory_every: int,
        best_trajectory: bool = True,
    ) -> None: ...

    def record(self, episode: VoxelEpisodeData) -> None:
        """Buffer one episode for the current iteration."""

    def on_iteration_end(
        self,
        iteration: int,
        episode_reward_mean: float,
        experiment_name: str,
        run_id: str,
    ) -> list[str]:
        """
        Select the best episode from the buffer, serialise to JSON, clear buffer.
        Returns list of relative paths written (may be empty).
        """

    @staticmethod
    def load(store: OutputStore, rel_path: str) -> dict:
        """Deserialise a trajectory JSON file to a plain dict."""
```

---

## Integration with `ExperimentRunner`

Wired in `ExperimentRunner.run()` via the `on_iteration_end` hook:

```python
traj_writer = TrajectoryWriter(
    store,
    trajectory_every=config.training.trajectory_every,
    best_trajectory=config.training.best_trajectory,
)

def _combined_hook(result: TrainResult) -> None:
    _orig_hook(result)
    tracker.log_metrics({...}, step=result.iteration)
    try:
        episode = collect_eval_episode(trainer._algo, env_config_dict)
        traj_writer.record(episode)
        traj_writer.on_iteration_end(
            result.iteration,
            result.episode_reward_mean,
            experiment_name,
            run_id,
        )
    except Exception as exc:
        warnings.warn(f"trajectory collection failed at iter {result.iteration}: {exc}")

trainer.on_iteration_end = _combined_hook
```

`_finalise()` scans for `trajectories/iter_*.json` and populates
`RunInfo.trajectory_iterations` in the final `run.json`.

---

## Rust dependency

`collect_eval_episode` calls `PyVoxelEnv.filled_voxels()` to capture the initial
world state at episode start. This method must be present in the wheel:

```bash
# Rebuild after any Rust change:
cd theseo_anysearch/core
VIRTUAL_ENV=../../.venv ../../.venv/Scripts/maturin.exe develop
```

If `filled_voxels` is absent (stale wheel), trajectory collection fails per-iteration
with a warning and `trajectory_iterations` remains `[]` in `run.json`. Training
continues normally.

---

## File Size Estimates

| Scenario | Per-episode size |
|---|---|
| 1 agent, 50 steps, scalar obs | ~3 KB |
| 1 agent, 200 steps, scalar obs | ~10 KB |
| 4 agents, 200 steps, scalar obs | ~40 KB |

With `trajectory_every: 10` over 500 iterations → ~50 MB total. `best.json`
adds one more file of similar size.

---

## Testing

### Unit tests (`tests/unit/test_trajectory.py`)

| Test | What it covers |
|---|---|
| `test_no_write_when_disabled` | `trajectory_every=0`, `best_trajectory=False` → empty list |
| `test_periodic_write` | File written at matching iterations, not others |
| `test_best_write_on_improvement` | `best.json` updated when reward improves |
| `test_best_not_updated_on_regression` | `best.json` not overwritten when reward drops |
| `test_best_meta_written` | `best_meta.json` contains correct iteration and reward |
| `test_selects_highest_reward_episode` | With multiple episodes in buffer, best is selected |

### Integration tests (`tests/integration/test_trajectory_integration.py`)

| Test | What it covers |
|---|---|
| `TestCollectEvalEpisode` | 11 tests: obs structure, step count, reward accumulation, `filled_voxels`, action variety |
| `TestTrajectoryWriterWithRealEpisode` | 3 tests: JSON written, parseable, `best.json` updated |
| `TestTrajectoryOutput` (in `test_experiment_runner_ray.py`) | 5 tests: files exist, JSON valid, meta correct — skipped if wheel missing `filled_voxels` |
