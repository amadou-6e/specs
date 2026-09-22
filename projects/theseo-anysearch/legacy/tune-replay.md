# Tune Trial Replay

## Overview

Extends the `voxel_replay` viewer and tune training pipeline to support
navigating between trials in a hyperparameter search run, in addition to
the existing iteration and step navigation.

---

## Python: Trajectory Recording per Trial

### Problem
`_real_trainable` builds `TrainingConfig` but does not pass `trajectory_every`
or `best_trajectory`, so tune trials produce no trajectory files.

### Fix
Read `trajectory_every` and `best_trajectory` from the YAML `training:` section
and pass them through to `_real_trainable`. In the training loop, call
`TrajectoryWriter.on_iteration_end` after each iteration, exactly as the
experiment runner does.

### YAML fields (under `training:`)
```yaml
training:
  trajectory_every: 10   # save every N iterations; 0 = disabled
  best_trajectory: true  # always save best-so-far as best.json
```

### Output per trial
```
runtime/tune/{run_tag}/
└── trial_{id}/
    ├── params.json
    ├── result.json           # JSONL metrics per iteration
    └── trajectories/
        ├── best.json         # best trajectory seen so far
        ├── best_meta.json    # {"iteration": N, "episode_reward_mean": X}
        └── iter_000010.json  # periodic saves
```

---

## Rust: Trial Navigation in voxel_replay

### New CLI flag
```
theseo-viewer --tune-dir <path>   # path to a tune run tag dir, e.g. runtime/tune/v2
theseo-viewer <file1> <file2> ... # existing: load specific trajectory files
```

When `--tune-dir` is given, the viewer:
1. Scans all `trial_*/trajectories/best.json` files under the dir
2. Sorts trials by `episode_reward_mean` descending (best first)
3. Loads trial params from `trial_*/params.json`

### Navigation levels (three-level)
```
[Trial]  →  [Iteration]  →  [Step]
  T/Y          [/]           ←/→
```

| Key | Action |
|-----|--------|
| `T` | Next trial |
| `Y` | Previous trial |
| `[` | Next iteration (within current trial) |
| `]` | Previous iteration (within current trial) |
| `←` / `→` | Step forward / backward |
| `Space` | Play/pause step auto-advance |

### UI additions
- **Trial header**: `Trial 3 / 30 — trial_abc123  (reward: -1.42)`
- **Params panel** (bottom-left): key-value list from `params.json`
- **Reward ranking**: trials sorted best→worst; current rank shown

### State struct additions
```rust
struct AppState {
    // existing
    trajectories: Vec<TrajectoryFile>,  // one per iteration in current trial
    current_iter: usize,
    current_step: usize,

    // new
    tune_trials: Vec<TrialEntry>,       // sorted by best reward
    current_trial: usize,
}

struct TrialEntry {
    trial_id: String,
    params: serde_json::Value,
    best_reward: f32,
    trajectory_dir: PathBuf,
}
```

### Loading flow
```
on startup (tune-dir mode):
  scan trial_* dirs → collect TrialEntry list → sort by best_reward desc
  load_trial(0)

load_trial(idx):
  scan trajectories/ in trial dir → collect sorted iter_*.json + best.json
  load iteration files into self.trajectories
  reset current_iter = 0, current_step = 0
```

---

## Replay command

```bash
# replay best trial from a tune run
theseo-viewer --tune-dir runtime/tune/v2

# replay specific trajectory files (existing behaviour unchanged)
theseo-viewer runtime/experiments/goal-nav-demo/043f3999/trajectories/best.json
```
