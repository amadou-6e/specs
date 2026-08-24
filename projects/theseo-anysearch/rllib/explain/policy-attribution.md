# Policy Attribution Specification

## Purpose

Define how to compute feature attributions for trained RLlib policies using
saved or deterministic evaluation episodes.

The first implementation targets collision-heavy DQN runs with radial
observations.  The design remains compatible with PPO by changing the action
score target from Q-values to policy logits.

---

## Inputs

| Input | Required | Description |
|---|---:|---|
| `run_ref` | yes | Registry reference such as `dqn-maps-zones:5932954b`. |
| `checkpoint` | yes | Checkpoint selector: `latest`, `best`, explicit iteration, or path. |
| `trajectory` | yes | Saved trajectory file or selector such as `iter_000080`. |
| `method` | yes | Attribution method: `shap`, `permutation_shap`, `grouped_shap`, `captum`, or `occlusion`. |
| `focus` | yes | Step selector: `collisions`, `all`, or explicit step indices. |
| `background` | no | Real rollout observations used as SHAP background. Defaults to non-collision states from the same trajectory plus nearby saved trajectories. |

The implementation must fail clearly when the checkpoint, trajectory, or
optional explainer dependency is missing.

---

## Observation Flattening

Explainability code operates on a stable flat feature vector, but reports must
preserve human-readable feature names.

For current single-agent radial observations, the flat order is:

| Group | Features |
|---|---|
| `steps_remaining` | `steps_remaining[0]` |
| `goal_distance` | `goal_distance[0]` |
| `goal_direction` | `goal_direction[0..2]` |
| `cursor_pos` | `cursor_pos[0..2]` |
| `ray_hits` | `ray_hits[0..25]` |
| `ray_hit_types` | `ray_hit_types[0..25]` |

Feature names must include action-aligned ray indices:

```text
ray_hits[21](dx=1,dy=0,dz=0)
ray_hit_types[21](dx=1,dy=0,dz=0)
```

Flatten and unflatten must be deterministic and covered by tests.  Dict key
iteration order must not define the feature order.

---

## Policy Scoring Adapter

The explainer receives a pure scoring interface owned by a `PolicyScorer`
object:

```python
score_all(observations) -> ActionScoreTable
score_action(observations, actions) -> np.ndarray
```

The adapter owns:

- unflattening flat features back into RLlib observation dictionaries;
- applying the same observation preprocessing used during policy inference;
- restoring the trained checkpoint;
- returning deterministic, exploration-free scores.

The backend-only implementation details for scorer construction and injection
are defined in `backend.md`.

### DQN Target

DQN is the first-class V1 target:

```text
score(obs, action) = Q(obs)[action]
```

The adapter must expose all 26 action scores so reports can compare the chosen
action against safe alternatives.

### PPO Target

PPO is supported later through policy distribution inputs:

```text
score(obs, action) = policy_logits(obs)[action]
```

If logits are not available through the active RLlib stack, the adapter may use
log probabilities, but the report must name the score type explicitly.

---

## Collision Step Selection

For `--focus collisions`, a step is selected when the executed action produced a
collision.  The implementation should prefer explicit collision metadata if the
trajectory schema provides it.  Until that field exists, collision detection may
derive from unchanged cursor position after a non-terminal step.

For every selected collision state, the report must include:

- step index;
- chosen action and direction;
- pre-action `ray_hits[action]`;
- pre-action `ray_hit_types[action]`;
- chosen action score;
- best safe action and score;
- score margin: `chosen_score - best_safe_score`;
- top positive and negative contributing feature groups.

Safe actions are actions whose pre-action ray does not indicate an immediate
collision.  For radial observations, immediate collision evidence is:

```text
ray_hits[action] == 1.0
ray_hit_types[action] in {occupied, boundary, filled}
```

---

## Attribution Methods

### SHAP

`shap` explains a black-box scoring function.  The default target for collision
diagnostics is:

```text
Q(obs)[chosen_collision_action] - Q(obs)[best_safe_action]
```

This answers why the policy ranked the collision action above the best safe
alternative.

### Grouped SHAP

Grouped attribution is the preferred first report.  Required groups:

| Group | Contents |
|---|---|
| `progress` | `steps_remaining` |
| `goal` | `goal_distance`, `goal_direction` |
| `position` | `cursor_pos` |
| `ray_hits_all` | all ray proximity features |
| `ray_hit_types_all` | all ray semantic features |
| `chosen_ray_hit` | `ray_hits[chosen_action]` |
| `chosen_ray_type` | `ray_hit_types[chosen_action]` |
| `safe_action_rays` | ray features for candidate safe actions |

### Captum

Captum is optional and only valid when the implementation can access a PyTorch
forward path with gradients.  Captum reports must state that they are gradient
attributions, not Shapley values.

### Occlusion

Occlusion is the fallback and test oracle:

```text
importance(feature) = score(original) - score(masked_feature)
```

Masks must use realistic baselines from background observations where possible.

The backend prototype should implement occlusion before SHAP.  This gives the
team a dependency-free proof that observation capture, action scoring, collision
selection, and reporting all work.

---

## Artifacts

`report.json` is the canonical output:

```json
{
  "run_ref": "dqn-maps-zones:5932954b",
  "checkpoint": "latest",
  "trajectory": "iter_000080",
  "algorithm": "dqn",
  "score_type": "q_value",
  "method": "grouped_shap",
  "feature_schema_version": 1,
  "steps": [
    {
      "step": 42,
      "chosen_action": 21,
      "chosen_direction": [1, 0, 0],
      "collision_visible": true,
      "chosen_score": -2.4,
      "best_safe_action": 15,
      "best_safe_score": -1.1,
      "score_margin": -1.3,
      "top_groups": [
        {"name": "chosen_ray_type", "value": -0.8},
        {"name": "goal", "value": 0.3}
      ]
    }
  ]
}
```

CSV outputs are derived convenience artifacts.  JSON is the source of truth.

---

## Tests

Required tests:

- flatten/unflatten preserves feature names and values;
- DQN adapter returns 26 action scores for mocked and restored policies;
- collision report works on saved trajectory-like fixtures;
- missing checkpoint, trajectory, or dependency raises a clear user-facing error;
- grouped reports include `chosen_ray_hit` and `chosen_ray_type` for collision states.
- backend smoke test works without CLI by injecting a mock scorer and in-memory trace.
