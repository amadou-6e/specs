# CLI Specification

> **Status**: Living document. The design direction is simplification — fewer words to get to
> the common case, consistent addressing, one canonical workflow. Legacy commands are retained
> for compatibility but deprecated in favour of the modern path.

---

## Design Goals

1. **The hot path is short.** Starting a run, listing what exists, and replaying the best
   result should each take one command with no flags memorised.

2. **CWD is the workspace.** Every command resolves paths relative to the project root.
   `--output-dir` is an escape hatch, not a required flag.

3. **Name and tag are the address.** Any run or sweep is reachable as `name:tag` or
   `name:run_id`. Register once, use the short name everywhere. Direct path addressing
   also works without registration.

4. **YAML is the source of truth.** Config lives in files. The CLI is a thin dispatch layer
   that reads YAML, validates it, and delegates all logic.

5. **One system.** `anysearch run` is the single entry point for training runs, sweeps, and
   tune searches. The legacy `train` and `tune` commands are deprecated.

---

## Command Tree

```
anysearch
│
├── run <name:tag | dir> [--tag]     Hot path — start any experiment
├── list [<name | dir>]              Hot path — see everything that has been run
├── add <dir> [<name>]               Register an experiment directory under a short name
│
├── inspect <ref>                    Print resolved config, metrics, and artifact paths
├── resume <ref>                     Continue training from the latest checkpoint
├── repeat <ref>                     Re-run from scratch with the same config
├── delete <ref> [-f] [--cached]     Delete run output directories and/or deregister
│
├── replay                           Open trajectories in the eframe viewer
│   ├── <ref>                        Sweep: T/Y trial navigation  |  Single run: all snapshots
│   ├── <ref> --best                 Best episode only
│   ├── <ref> --iter N               Specific iteration snapshot
│   ├── tune <ref>                   Explicit tune-sweep entry point (same as default for sweeps)
│   ├── file <path>                  Open any trajectory JSON by path
│   └── list <ref>                   Show available snapshots for a run or trial
│
├── mlflow [<name>] [options]        Launch MLflow UI (scoped to name, or global)
├── tensorboard [<ref>] [options]    Launch TensorBoard (scoped to run/sweep, or global)
│
├── ray                              Ray cluster management
│   ├── ps                           List active sessions and workers
│   └── stop                         Stop all sessions
│
├── train [<dir>]                    [deprecated → use `anysearch run`]
└── tune [<dir>]                     [deprecated → use `anysearch run`]
```

---

## Registry

The registry is **global** — like Docker's image registry, `anysearch list` returns the
same result regardless of which directory you run the command from.

The registry lives at `~/.anysearch/registry.yaml` (user home directory).

```yaml
# ~/.anysearch/registry.yaml — auto-updated by `add` and `run <dir/yaml>`
experiments:
  multi_agent_ppo_asha:  /abs/path/to/usage/experiments/tune/multi_agent_ppo_asha.yaml
  ppo_baseline:          /abs/path/to/usage/experiments/ppo_baseline
```

Paths stored in the registry are **absolute**, so the file is unambiguous from any CWD.

**Name derivation** (in priority order):
1. Explicit `<name>` argument: `anysearch add multi_agent_ppo_asha.yaml my-name`
2. YAML file stem when adding a `.yaml` file directly: `multi_agent_ppo_asha.yaml` → `multi_agent_ppo_asha`
3. Directory basename when adding a directory: `ppo_baseline/` → `ppo_baseline`

> The `experiment.name` field inside the YAML is used only as a human label for runs and
> MLflow experiments — it is **not** used as the registry key.

**Auto-registration:** `anysearch run <dir>`, `anysearch train <dir>`, and
`anysearch tune <dir>` all register automatically on first use.
Use `anysearch add <dir> [<name>]` to register explicitly or rename.

### Reference resolution

A `<ref>` is resolved in this order:

| Input form | Resolution |
|---|---|
| `name:tag` or `name:run_id` | Look up `name` in global registry → get dir → resolve `tag` or `run_id` inside it |
| `name` (no colon) | Look up in global registry → resolves to the experiment dir |
| `dir:tag` or `dir:run_id` | Use `dir` directly as the experiment directory (no registry lookup) |
| `dir` (contains `/` or starts with `.`) | Use directly as a filesystem path |

Commands that print references always emit both forms:
```
multi_agent_ppo_asha:v12  (usage/experiments/tune/multi_agent_ppo_asha/v12)
```

### Output directory resolution

When `output_dir` is specified in a YAML config, it is resolved **relative to the YAML
file's parent directory**, not relative to CWD. This makes configs portable — you can run
them from any working directory and results always land in the same place.

```yaml
# usage/experiments/tune/multi_agent_ppo_asha.yaml
experiment:
  output_dir: ../../../runtime/experiments   # → <project_root>/runtime/experiments
```

If `output_dir` is absent, the default is the experiment directory itself (the YAML's
parent for file-based configs, or the directory for directory-based configs).

Absolute paths in `output_dir` are used unchanged.

---

## Experiment Directory

An experiment is a directory. It contains the config and owns all output from runs against
that config. There is no separate `runtime/` tree — results live next to the config that
produced them.

All output lives under `{output_dir}/{experiment.name}/` — scoped to the experiment name so
multiple experiments sharing the same `output_dir` don't collide.

**Tune sweep** (config has `tune_config:`):

```
runtime/experiments/
└── multi_agent_ppo_asha/            ← experiment.name
    ├── latest/                      ← tag (default when --tag omitted)
    │   └── {trial_hash}_{num}/      ← Ray Tune trial dir (contains ray_runtime.json)
    │       ├── ray_runtime.json
    │       ├── experiment.yaml
    │       ├── params.json
    │       ├── checkpoints/
    │       └── trajectories/
    │           ├── iter_000020.json
    │           └── best.json
    └── v11/                         ← explicit --tag v11
        └── {trial_hash}_{num}/
            └── ...
```

**Single training run** (no `tune_config`):

```
runtime/experiments/
└── ppo_baseline/                    ← experiment.name
    └── {run_id}/                    ← 8-char hex
        ├── run.json
        ├── experiment.yaml
        ├── checkpoints/
        ├── trajectories/
        │   ├── iter_000020.json
        │   └── best.json
        └── renders/
```

### Config file lookup

`anysearch run <dir>` finds the config by searching the directory for:
1. `config.yaml`
2. `experiment.yaml`
3. A single `*.yaml` file — used directly if only one exists, error if multiple

---

## `anysearch add`

```bash
anysearch add <dir-or-yaml> [<name>]
```

Registers an experiment under a short name in the global registry (`~/.anysearch/registry.yaml`).
Accepts either a directory or a `.yaml` file directly.

If `<name>` is omitted:
- For a `.yaml` file → uses the filename stem (`multi_agent_ppo_asha.yaml` → `multi_agent_ppo_asha`)
- For a directory → uses the directory basename

```bash
anysearch add usage/experiments/tune/multi_agent_ppo_asha.yaml   # name: multi_agent_ppo_asha
anysearch add usage/experiments/ppo_baseline/                    # name: ppo_baseline
anysearch add usage/experiments/ppo_baseline/ my-ppo             # explicit name
```

Paths are stored as **absolute** paths. Prints confirmation and the full registry:

```
Registered: multi_agent_ppo_asha -> /abs/.../usage/experiments/tune/multi_agent_ppo_asha.yaml

Registry (~/.anysearch/registry.yaml):
  multi_agent_ppo_asha   /abs/.../usage/experiments/tune/multi_agent_ppo_asha.yaml
  ppo_baseline           /abs/.../usage/experiments/ppo_baseline
```

---

## `anysearch run`

```bash
anysearch run <name:tag | dir> [--tag|-t <tag>] [--output-dir <path>]
```

The single entry point for all experiment kinds. Accepts either a registered name
(optionally with `:tag`) or a filesystem directory path. When a directory path is given,
auto-registers it if not already known.

Dispatches based on config content:

| Config content | Behaviour |
|---|---|
| No `tune_config` | Single training run → `{output_dir}/{experiment.name}/{run_id}/` |
| `tune_config:` present | Ray Tune sweep → `{output_dir}/{experiment.name}/{tag}/{trial_id}/` |
| Top-level `sweep:` key | Sequential fixed-config sweep → `{output_dir}/{experiment.name}/{run_id}/` per entry |

**Options**

| Flag | Default | Description |
|---|---|---|
| `<ref>` | required | Registered name (with optional `:tag`) or experiment directory |
| `--tag` / `-t` | `latest` | Subdirectory name for this sweep (tune sweeps only) |
| `--output-dir` | from YAML | Override output location if results should go elsewhere |

**On start — single run:** prints a Rich panel with name, algorithm, iterations, output
dir, and config path. While torch/ray are loading, a throbber cycles through synonyms of
"loading" on stderr at 4-second intervals until the trainer is ready.

**On start — tune sweep:** prints a Rich panel with algorithm, scheduler, trial count,
concurrency, iterations, GPU requirement, search space, output dir, MLflow URI, and
TensorBoard command.

**On end or interrupt:** prints a Rich panel with replay instructions using the registered
name:

```
╭─ Run complete  ppo_baseline:a1b2c3d4 ──────────────────────╮
│   Best episode     anysearch replay ppo_baseline:a1b2c3d4 --best  │
│   All snapshots    anysearch replay ppo_baseline:a1b2c3d4         │
│   List available   anysearch replay ppo_baseline:a1b2c3d4 list    │
│   Metrics UI       anysearch mlflow ppo_baseline                  │
╰────────────────────────────────────────────────────────────╯
```

---

## `anysearch list`

```bash
anysearch list [<name | dir>] [--short|-s]
```

Shows all runs and sweeps using Rich panels. With no argument, lists all registered
experiments (compact — no YAML). With a name or directory, scopes to that experiment
and shows the config path, output dir, YAML contents, and run table.

Runs are scanned from `output_dir/experiment.name/` (resolved from the YAML) so each
experiment only shows its own runs, even when multiple experiments share the same
`output_dir` base.

**Global listing** (`anysearch list`): one panel per registered experiment, run table
only — no YAML displayed.

**Scoped listing** (`anysearch list <name>`): additionally shows `config` path,
`output_dir`, and the full YAML with syntax highlighting. Pass `--short` / `-s` to
suppress the YAML.

```
╭─ ppo_baseline ─────────────────────────────────────────────╮
│  config      /abs/.../usage/experiments/ppo_baseline/config.yaml  │
│  output_dir  /abs/.../runtime/experiments/ppo-baseline            │
│                                                                   │
│  TAG / RUN ID    STATUS      STARTED                              │
│  a1b2c3d4        COMPLETED   2026-03-14                           │
│                                                                   │
│  experiment:                                                      │
│    name: ppo-baseline                                             │
│    ...                                                            │
╰────────────────────────────────────────────────────────────╯
```

| Flag | Description |
|---|---|
| `<name>` | Registered name or directory to scope to |
| `--short` / `-s` | Omit YAML contents (scoped mode only) |

---

## `anysearch inspect`

```bash
anysearch inspect <ref>
```

Prints JSON to stdout: resolved config, status, timing, checkpoint iterations, trajectory
iterations, render files, MLflow run URL.

```bash
anysearch inspect ppo-baseline:a1b2c3d4
anysearch inspect multi-agent-ppo:v12
```

> **Current implementation:** `anysearch experiment inspect --run-id <hex>` (named flag,
> hex only). Proposed change: top-level positional `<ref>` once the resolver is
> implemented.

---

## `anysearch resume`

```bash
anysearch resume <ref> [--output-dir <path>]
```

Restores from the latest checkpoint and continues training. Appends to the same output
directory and MLflow run. Config is read from inside the run directory.

```bash
anysearch resume ppo-baseline:a1b2c3d4
```

> Tune sweep resume is not yet supported.

> **Current implementation:** `anysearch experiment resume --run-id <hex>`.

---

## `anysearch repeat`

```bash
anysearch repeat <ref> [--output-dir <path>]
```

Reads the config from the referenced run and starts a fresh run from scratch: new run_id,
new output directory, same config and seed.

```bash
anysearch repeat ppo-baseline:a1b2c3d4
```

> **Current implementation:** `anysearch experiment repeat --run-id <hex>`.

---

## `anysearch replay`

Locates and opens trajectory files in the eframe `voxel-replay` viewer.

Build the viewer once with:
```bash
cd theseo_anysearch/core && cargo build --release --bin voxel-replay
```

### Default — single run or sweep

```bash
anysearch replay <ref> [--best] [--iter N]
```

The resolver detects whether `<ref>` points to a sweep or single run by inspecting the
directory structure and opens the appropriate viewer mode automatically. Path resolution
uses `output_dir` from the YAML (not the source directory), so `name:tag` correctly
finds sweep trials under `output_dir/experiment.name/tag/`.

| Form | Opens |
|---|---|
| `anysearch replay multi_agent_ppo_asha:v12` | Tune viewer — all trials, T/Y navigation |
| `anysearch replay multi_agent_ppo_asha` | Auto: opens `latest/` if unique; lists tags if multiple |
| `anysearch replay ppo_baseline:a1b2c3d4` | Single-run viewer — all iteration snapshots |
| `anysearch replay multi_agent_ppo_asha:v12 --best` | Best trial's `best.json` only |
| `anysearch replay ppo_baseline:a1b2c3d4 --best` | Run's `best.json` only |
| `anysearch replay ppo_baseline:a1b2c3d4 --iter 80` | Specific iteration snapshot |

When no tag or run_id is given (`anysearch replay <name>`):
- If exactly one tag directory exists under the experiment → opens it automatically.
- If multiple tags exist → prints the available tags and exits:
  ```
  Available tags — specify one:
    anysearch replay multi_agent_ppo_asha:latest
    anysearch replay multi_agent_ppo_asha:v11
  ```
- For single-run experiments → lists run IDs the same way.

Direct path addressing also works without registration:
```bash
anysearch replay usage/experiments/tune/multi_agent_ppo_asha:latest
```

### Viewer keyboard shortcuts (tune sweep mode)

| Key | Action |
|---|---|
| `T` / `Y` | Next / prev trial (sorted best-first by reward) |
| `[` / `]` | Next / prev iteration within current trial |
| `←` / `→` | Step forward / backward |
| `Space` | Play / pause |
| Left-drag | Orbit camera |
| Scroll | Zoom |
| `R` | Reset camera |

### `tune` (explicit subcommand)

```bash
anysearch replay tune <ref>
```

Same as the default when `<ref>` is a sweep, but explicit. Useful for scripting.

### `file`

```bash
anysearch replay file <path>
```

Opens an arbitrary trajectory JSON file by filesystem path.

### `list`

```bash
anysearch replay list <ref>
```

Prints available snapshots for a run or trial:

```
ppo-baseline:a1b2c3d4  (usage/experiments/ppo_baseline/a1b2c3d4)
  Periodic snapshots (5): iter_000020, iter_000040, iter_000060, iter_000080, iter_000100
  Best: best.json  (iter 87, reward 0.923)

  Replay best:  anysearch replay ppo-baseline:a1b2c3d4 --best
  Replay all:   anysearch replay ppo-baseline:a1b2c3d4
```

---

## `anysearch delete`

```bash
anysearch delete <ref> [-f] [--cached]
```

Delete run output directories and optionally deregister the experiment.

```bash
anysearch delete ppo_baseline            # delete all runs + deregister
anysearch delete ppo_baseline:a1b2c3d4  # delete one run directory
anysearch delete ppo_baseline --cached  # deregister only, keep files
```

Shows a table of what will be deleted (directories, contents, size) and prompts for
confirmation before proceeding. Pass `-f` / `--force` to skip the prompt.

`--cached` removes the registry entry only — no files are touched. Useful after
manually moving or archiving an experiment directory.

| Flag | Default | Description |
|---|---|---|
| `<ref>` | required | Experiment name (all runs) or `name:run_id` (one run) |
| `--force` / `-f` | false | Skip confirmation prompt |
| `--cached` | false | Only deregister — do not delete any files |

---

## `anysearch mlflow`

```bash
anysearch mlflow [<name>] [--port 5000] [--host 127.0.0.1] [--tracking-uri <uri>]
```

Launches `mlflow ui`. When a registered experiment name is given, points at that
experiment's local `mlflow.db`. With no name, falls back to the project-wide
`runtime/mlflow.db`.

| Usage | Tracking DB |
|---|---|
| `anysearch mlflow` | `runtime/mlflow.db` (project-wide fallback) |
| `anysearch mlflow ppo-baseline` | `usage/experiments/ppo_baseline/mlflow.db` |
| `anysearch mlflow multi-agent-ppo` | `usage/experiments/tune/multi_agent_ppo_asha/mlflow.db` |
| `anysearch mlflow --tracking-uri <uri>` | Explicit override |

| Flag | Default | Description |
|---|---|---|
| `<name>` | — | Registered experiment name (optional) |
| `--port` | `5000` | Serving port |
| `--host` | `127.0.0.1` | Bind address |
| `--tracking-uri` | auto | Override full URI (ignores `<name>`) |

---

## `anysearch tensorboard`

```bash
anysearch tensorboard [<ref>] [--port 6006] [--host 127.0.0.1]
```

Launches TensorBoard. Resolves the logdir from the YAML's `output_dir` (not the source
directory), so it correctly points at where runs and trials are actually written.
Uses `shutil.which("tensorboard")` to find the venv's `tensorboard` script.

| Usage | Logdir |
|---|---|
| `anysearch tensorboard` | Current directory |
| `anysearch tensorboard ppo_baseline` | `output_dir/ppo-baseline/` |
| `anysearch tensorboard ppo_baseline:a1b2c3d4` | `output_dir/ppo-baseline/a1b2c3d4/` if it exists, else `output_dir/ppo-baseline/` |
| `anysearch tensorboard multi_agent_ppo_asha:v1` | `output_dir/multi-agent-ppo-asha/v1/` |

| Flag | Default | Description |
|---|---|---|
| `<ref>` | — | Registered name, name:tag, or path (optional) |
| `--port` | `6006` | Serving port |
| `--host` | `127.0.0.1` | Bind address |

---

## `anysearch ray`

### `ps`

```bash
anysearch ray ps
```

Lists active Ray sessions, worker PIDs, GPU workers, and GCS addresses.
Reads `%TEMP%/anysearch_*` temp directories and running process list. Requires `psutil`.

### `stop`

```bash
anysearch ray stop [--force]
```

Calls `ray stop --force`. With `--force`, kills Ray processes directly via `psutil`
if `ray stop` fails. Use after a crashed sweep to release GPU memory and orphaned workers.

---

## Legacy Commands (deprecated)

Both commands print a deprecation notice pointing to `anysearch run`.
Both still accept a directory path and will auto-register it when used.

### `anysearch train`

Direct wrapper around `theseo_core.py_train_videos`. Flag-based, no YAML, no MLflow,
no trajectory recording. Kept for scripted workflows that haven't migrated.

```
[deprecated] Use: anysearch run <dir>
             Or:  anysearch run ppo-baseline
```

### `anysearch tune`

Flag-based hyperparameter sweep. PPO-only, requires `--stl`. Predates `ExperimentConfig`
and `TuneRunner`. `apply_win_atomic_save_patch` is now shared with the modern path.

```
[deprecated] Use: anysearch run <dir> --tag <tag>
             Or:  anysearch run multi-agent-ppo --tag v13
```

---

## Implementation Status

| Feature | Status |
|---|---|
| `anysearch replay` default, `file`, `list`, `tune` subcommands | ✅ Implemented |
| `anysearch delete <ref> [-f] [--cached]` | ✅ Implemented |
| `anysearch mlflow [<name>]` (experiment-scoped MLflow DB) | ✅ Implemented |
| `anysearch tensorboard [<ref>]` — logdir from YAML `output_dir`, venv script | ✅ Implemented |
| `anysearch ray ps/stop` | ✅ Implemented |
| Replay hints use registered `name:run_id` (Rich panel) | ✅ Implemented |
| Smart `replay` dispatch — resolves `output_dir` from YAML, auto-detects sweep vs run | ✅ Implemented |
| `replay <name>` (no tag) — auto-open single tag; list available tags if multiple | ✅ Implemented |
| ASHA grace period configurable via `asha_config` in YAML | ✅ Implemented |
| `anysearch experiment run/resume/repeat/inspect/list` (legacy group, deprecated) | ✅ Implemented |
| `anysearch add/run/list/inspect/resume/repeat` top-level commands | ✅ Implemented |
| Deprecation notices on `experiment`, `train`, `tune` | ✅ Implemented |
| **Global registry** (`~/.anysearch/registry.yaml`, absolute paths) | ✅ Implemented |
| **Name from YAML stem** (not `experiment.name`) | ✅ Implemented |
| **`output_dir` resolved relative to YAML parent** | ✅ Implemented |
| **`--tag` / `-t` alias** (`latest` default) | ✅ Implemented |
| **`list` YAML display** — shown by default when scoped, `-s` to suppress, hidden in global listing | ✅ Implemented |
| **`list` run scoping** — searches `output_dir/experiment.name/` not shared `output_dir` | ✅ Implemented |
| **Rich panels** — `run` pre-start summary, sweep overview, end-of-run replay hint | ✅ Implemented |
| **Loading throbber** — cycles synonyms at 4 s/word on stderr while torch/ray import | ✅ Implemented |
| **Sweep storage at `{output_dir}/{experiment.name}/{tag}/`** (`latest` default tag) | ✅ Implemented |
| **Trajectory collection in `Trainer.train()`** — automatic for all run types | ✅ Implemented |
| **`experiment.yaml` written per trial** in tune sweeps | ✅ Implemented |
| **Trial dirs detected by `ray_runtime.json`** (not `trial_*` prefix) | ✅ Implemented |
| MLflow DB written into experiment dir | 🔲 Pending |
