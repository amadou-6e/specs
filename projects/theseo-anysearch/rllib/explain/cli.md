# Explain CLI Specification

## Purpose

Add a future CLI command for policy explanations:

```text
anysearch explain <name:run_id>
```

The command explains a trained RLlib policy on a saved trajectory or freshly
collected deterministic evaluation episode.

The CLI is phase two.  The first implementation should build and test the
backend described in `backend.md`, then wrap that backend with this command.

---

## Command Shape

```text
anysearch explain <name:run_id>
  --checkpoint latest
  --trajectory iter_000080
  --method grouped_shap
  --focus collisions
  --background auto
  --output auto
```

Example:

```powershell
anysearch explain dqn-maps-zones:5932954b `
  --checkpoint latest `
  --trajectory iter_000080 `
  --method grouped_shap `
  --focus collisions
```

---

## Arguments

| Argument | Default | Description |
|---|---|---|
| `<name:run_id>` | required | Registry reference for the run to explain. |
| `--checkpoint` | `latest` | Checkpoint selector: `latest`, `best`, iteration number, or path. |
| `--trajectory` | `best` | Trajectory selector: `best`, `iter_000080`, or path. |
| `--method` | `grouped_shap` | Attribution method. |
| `--focus` | `collisions` | Step selector: `collisions`, `all`, or comma-separated step indices. |
| `--background` | `auto` | Background observation source for SHAP methods. |
| `--output` | `auto` | Output directory. Defaults to `{run_dir}/explanations/{trajectory_stem}`. |
| `--max-steps` | `50` | Maximum selected steps to explain in one invocation. |
| `--seed` | `42` | Seed used when collecting a fresh deterministic eval episode. |

---

## Supported Methods

| Method | Dependency | Notes |
|---|---|---|
| `grouped_shap` | `shap` | Preferred readable V1 report. |
| `permutation_shap` | `shap` | Runtime-friendly approximation. |
| `kernel_shap` | `shap` | More expensive black-box SHAP mode. |
| `captum_ig` | `captum` | Optional PyTorch Integrated Gradients backend. |
| `occlusion` | none | Built-in fallback and debugging baseline. |

If an optional dependency is missing, the command must tell the user which
package or optional extra to install.

---

## Output

On success, print a concise summary:

```text
Explained dqn-maps-zones:5932954b
checkpoint: latest
trajectory: iter_000080
selected steps: 8 collision steps
output: runtime/experiments/dqn-maps-zones/5932954b/explanations/iter_000080
```

Write artifacts:

```text
report.json
collision_steps.csv
feature_groups.csv
plots/
```

The command should also print a follow-up hint:

```text
Open report: code <output>/report.json
Replay source: anysearch replay dqn-maps-zones:5932954b --iter 80
```

---

## Failure Behaviour

The command must fail before expensive work when:

- the run reference cannot be resolved;
- the checkpoint selector does not resolve to a checkpoint;
- the trajectory selector does not resolve to a trajectory;
- no selected steps match `--focus`;
- the algorithm does not expose a supported scoring adapter;
- the requested method dependency is missing.

Errors should be user-facing and include the next action, for example:

```text
SHAP is not installed. Install the explain optional dependencies:
  pip install -e ".[explain]"
```

---

## Acceptance Criteria

- `anysearch explain --help` documents all arguments and examples.
- A DQN run with a saved trajectory produces `report.json`.
- `--focus collisions` selects only collision states.
- Reports include chosen action, best safe action, score margin, and top feature groups.
- Missing optional dependencies produce actionable errors.
- Tests cover CLI argument parsing with mocked adapters and fixture trajectories.
