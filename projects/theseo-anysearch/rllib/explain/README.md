# RLlib Explainability

## Purpose

Explain trained RLlib policies on saved or deterministic evaluation episodes.
The first use case is debugging why agents repeatedly choose collision actions
even when radial observations expose the obstruction.

This feature explains the deployed policy behaviour, not the neural network in
isolation.  The explained function always includes the trained checkpoint,
RLlib policy inference path, project observation preprocessing, and the selected
action score.

---

## Goals

| Goal | Description |
|---|---|
| **Policy-level explanation** | Explain action scores produced by a restored RLlib policy checkpoint. |
| **Episode-grounded analysis** | Explain observations from saved trajectories or deterministic eval episodes. |
| **Collision focus** | Prioritise failure states where the chosen action collides. |
| **Observation attribution** | Attribute chosen-action scores to named observation features and feature groups. |
| **Action comparison** | Compare chosen collision action scores against best safe action scores. |

---

## V1 Workflow

V1 is backend-first.  The first implementation should expose a Python API and
testable backend objects before adding `anysearch explain`.

```text
1. Train an RLlib policy and save checkpoints.
2. Save or collect a deterministic evaluation trajectory.
3. Restore the checkpoint.
4. Reconstruct or load the observation stream for the trajectory.
5. Score all 26 actions for each selected observation.
6. Run attribution for collision states first.
7. Write explanation artifacts next to the run output.
```

V1 targets DQN first because Q-values are directly interpretable:

```text
f(obs) -> Q(obs)[action]
```

PPO support uses the same high-level workflow, but explains action logits or
log probabilities instead:

```text
f(obs) -> policy_logits(obs)[action]
```

The backend package and object structure are specified in `backend.md`.

---

## Terminology

| Term | Meaning |
|---|---|
| **Checkpoint** | RLlib checkpoint containing trained policy state. |
| **Trajectory** | Saved eval episode under `trajectories/`, e.g. `iter_000080.json`. |
| **Explained state** | Observation selected for attribution, usually before a collision action. |
| **Chosen action** | Action taken by the policy or recorded in the trajectory. |
| **Safe action** | Action whose immediate ray does not indicate a collision. |
| **Background observations** | Real rollout observations used as SHAP background distribution. |
| **Feature group** | Named collection of flat observation features, e.g. all `ray_hits`. |

---

## Recommended Methods

| Method | Role |
|---|---|
| **SHAP** | Primary V1 method. Use black-box policy scoring adapters. |
| **Permutation SHAP** | Practical default when full KernelSHAP is too slow. |
| **Grouped SHAP** | Preferred first report format for readable policy diagnostics. |
| **Captum** | Optional faster backend for PyTorch gradient attributions. |
| **Occlusion** | Baseline sanity check and fallback when optional dependencies are missing. |

SHAP background data must come from real rollout observations.  All-zero
baselines are not valid for the primary workflow because they can produce
out-of-distribution explanations.

---

## Output Location

Explanation artifacts are written under the run directory:

```text
{run_dir}/
└── explanations/
    └── {trajectory_stem}/
        ├── report.json
        ├── collision_steps.csv
        ├── feature_groups.csv
        └── plots/
```

The exact schema is defined in `policy-attribution.md`.

---

## Non-Goals

- Explaining untrained models without a checkpoint.
- Shipping a CLI before the backend is proven through Python tests.
- Exact Shapley values over every feature for every episode step.
- Replacing TensorBoard or replay inspection.
- Training a separate counterfactual generator in V1.
