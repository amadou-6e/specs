# Explain Backend Specification

## Purpose

Define the backend-only implementation shape for policy explanations before a
CLI is added.  The first milestone is to prove that Theseo AnySearch can restore
or mock a policy, collect episode observations, score actions, and produce a
collision-focused explanation report through Python objects.

The backend must be usable from tests and notebooks without depending on Typer,
terminal output, or registry command parsing.

---

## Package Layout

The proposed implementation package is:

```text
theseo_anysearch/rllib/explain/
  __init__.py
  backend.py
  models.py
  features.py
  artifacts.py
  scoring.py
  traces.py
  selectors.py
  explainers.py
  reports.py
```

Each module owns one part of the workflow.  Shared behaviour belongs on the
object that needs it.  Repeated behaviour should move to a base class only when
there are at least two concrete implementations using it.

| File | Owner objects | Responsibility |
|---|---|---|
| `models.py` | `ExplanationRequest`, `ExplanationReport`, `ExplainedStep`, `ActionScoreTable` | Typed backend inputs and outputs. |
| `features.py` | `FeatureSchema`, `FeatureGroupSchema` | Stable flattening, unflattening, names, and group slices for observations. |
| `artifacts.py` | `RunArtifactResolver`, `ResolvedExplainArtifacts` | Resolve run directory, config, checkpoint, trajectory, and output paths. |
| `scoring.py` | `PolicyScorer`, `DQNPolicyScorer`, `PPOPolicyScorer`, `MockPolicyScorer` | Convert observation batches into action scores. |
| `traces.py` | `ObservationTrace`, `EvaluationTraceCollector`, `SavedTrajectoryTraceLoader` | Provide pre-action observations, actions, rewards, cursors, and collision metadata. |
| `selectors.py` | `StepSelector`, `CollisionStepSelector`, `ExplicitStepSelector` | Select which trace steps should be explained. |
| `explainers.py` | `Explainer`, `OcclusionExplainer`, `GroupedShapExplainer` | Compute feature or group attributions for selected action-score targets. |
| `reports.py` | `ExplanationReportBuilder`, `ExplanationReportWriter` | Convert scores and attributions into JSON/CSV artifacts. |
| `backend.py` | `PolicyExplanationBackend`, `explain_policy` | Orchestrate the backend workflow. |

---

## Public Python API

The first public interface is a Python function:

```python
from theseo_anysearch.rllib.explain import ExplanationRequest, explain_policy

request = ExplanationRequest(
    run_ref="dqn-maps-zones:5932954b",
    checkpoint="latest",
    trajectory="iter_000080",
    method="occlusion",
    focus="collisions",
)

report = explain_policy(request)
```

`explain_policy` is a small convenience wrapper.  The real workflow lives on
`PolicyExplanationBackend` so tests can replace individual collaborators:

```python
backend = PolicyExplanationBackend(
    artifacts=RunArtifactResolver(...),
    scorer=DQNPolicyScorer(...),
    trace_source=EvaluationTraceCollector(...),
    explainer=OcclusionExplainer(...),
    report_writer=ExplanationReportWriter(...),
)

report = backend.explain(request)
```

The backend constructor should accept explicit collaborators.  It may also have
a factory constructor later, for example `PolicyExplanationBackend.from_request`,
but the direct constructor is the testable core.

---

## Object Responsibilities

### `ExplanationRequest`

Owns user intent for one explanation run.

Required fields:

- `run_ref`: registry reference such as `dqn-maps-zones:5932954b`;
- `checkpoint`: `latest`, `best`, iteration, or checkpoint path;
- `trajectory`: trajectory selector, path, or `eval`;
- `method`: `occlusion`, `grouped_shap`, `permutation_shap`, or `captum`;
- `focus`: `collisions`, `all`, or explicit step indices.

Optional fields:

- `max_steps`: maximum selected steps;
- `seed`: deterministic evaluation seed;
- `output_dir`: explicit artifact directory;
- `background`: background observation selector for SHAP-compatible methods.

### `FeatureSchema`

Owns all observation flattening behaviour.

Methods:

- `from_observation_space(space) -> FeatureSchema`;
- `flatten(observation) -> np.ndarray`;
- `flatten_batch(observations) -> np.ndarray`;
- `unflatten(row) -> dict[str, np.ndarray]`;
- `feature_names() -> list[str]`;
- `group_slices() -> dict[str, slice]`;
- `action_feature_index(group, action) -> int`.

No other object should know dict iteration order or flat feature offsets.

### `PolicyScorer`

Owns policy action scoring.

Required methods:

- `score_all(observations) -> ActionScoreTable`;
- `score_action(observations, actions) -> np.ndarray`;

`DQNPolicyScorer` returns Q-values for all 26 actions.  `PPOPolicyScorer` is a
later-compatible implementation that returns logits or log probabilities.
`MockPolicyScorer` is required for deterministic unit tests.

### `ObservationTrace`

Owns the episode data used by explainers.

Each trace step includes:

- pre-action observation;
- action;
- reward;
- cursor before and after action;
- done flag;
- optional explicit collision flag;
- optional info dictionary.

Current saved trajectories do not reliably contain observations.  The backend
therefore supports two trace sources:

- `EvaluationTraceCollector` reruns a deterministic evaluation episode and
  captures observations directly.
- `SavedTrajectoryTraceLoader` loads saved trajectory-like data when observations
  are present or reconstructable.

For the first backend proof, prefer `EvaluationTraceCollector` because it avoids
guessing missing observation state from older trajectory files.

### `StepSelector`

Owns focus selection.

`CollisionStepSelector` selects steps with explicit collision metadata when
available.  Without explicit metadata, it may derive collisions from unchanged
cursor position after a non-terminal action.

### `Explainer`

Owns attribution computation.

The first implementation should be `OcclusionExplainer` because it has no
optional dependency and makes backend tests deterministic.  SHAP remains the
target external method, but should be added after the scorer and trace workflow
are proven.

### `ExplanationReportBuilder`

Owns report semantics.

For every selected step, it computes:

- chosen action score;
- safe action mask;
- best safe action and score;
- score margin;
- whether collision was visible in `ray_hits[action]`;
- semantic hit type from `ray_hit_types[action]`;
- top positive and negative feature groups.

---

## Backend Flow

```text
ExplanationRequest
  -> RunArtifactResolver.resolve
  -> PolicyScorer.restore_or_attach
  -> ObservationTrace source
  -> FeatureSchema.from_observation_space
  -> StepSelector.select
  -> PolicyScorer.score_all
  -> Explainer.explain selected targets
  -> ExplanationReportBuilder.build
  -> ExplanationReportWriter.write
```

The first smoke-test flow can skip artifact resolution and checkpoint restore by
injecting a `MockPolicyScorer` and an in-memory `ObservationTrace`.

---

## Prototype Milestones

1. Implement `FeatureSchema` and unit-test flatten/unflatten for radial observations.
2. Implement `MockPolicyScorer`, `ObservationTrace`, and `CollisionStepSelector`.
3. Implement `OcclusionExplainer` with grouped feature masking.
4. Implement `PolicyExplanationBackend` using only injected collaborators.
5. Add a mocked backend smoke test that explains one visible collision action.
6. Add `DQNPolicyScorer` and a checkpoint-backed integration test after the mocked flow is stable.
7. Add SHAP-compatible explainers after the backend can already explain with occlusion.

---

## Test Structure

Backend tests should live under the existing test-prefixed tree:

```text
tests/test_rllib/
  test_unit/
    test_explain/
      test_feature_schema.py
      test_policy_scorer.py
      test_step_selector.py
      test_occlusion_explainer.py
      test_report_builder.py
  test_integration/
    test_explain/
      test_backend_smoke.py
      test_dqn_checkpoint_scoring.py
```

Acceptance criteria:

- mocked backend smoke test produces an `ExplanationReport`;
- radial feature names and action-aligned ray names are stable;
- DQN scorer exposes 26 action scores;
- collision selector identifies visible collision steps;
- occlusion reports include `chosen_ray_hit` and `chosen_ray_type`;
- missing checkpoint, trajectory, or optional dependency errors are explicit and user-facing.

---

## Test Plan

Testing should prove the backend in layers.  Each layer should isolate one owner
object before the full backend is exercised.

### Layer 1: Feature Schema Unit Tests

Target file:

```text
tests/test_rllib/test_unit/test_explain/test_feature_schema.py
```

Test cases:

- radial observation dictionaries flatten into a deterministic vector;
- unflattening restores each observation group with the original dtype and shape;
- feature names are stable and do not depend on dictionary iteration order;
- ray feature names include action index and direction;
- `action_feature_index("ray_hits", action)` and
  `action_feature_index("ray_hit_types", action)` point to the expected values;
- invalid observation shapes fail with a clear schema error.

### Layer 2: Trace And Step Selection Unit Tests

Target files:

```text
tests/test_rllib/test_unit/test_explain/test_observation_trace.py
tests/test_rllib/test_unit/test_explain/test_step_selector.py
```

Test cases:

- `ObservationTrace` preserves pre-action observation, action, reward, cursor
  before, cursor after, done flag, and info per step;
- explicit collision metadata is preferred when present;
- unchanged cursor after a non-terminal action is treated as a derived collision
  when explicit metadata is absent;
- terminal success steps are not mislabeled as collisions only because the cursor
  no longer changes after termination;
- explicit step selection rejects indices outside the trace length with a
  user-facing error.

### Layer 3: Policy Scorer Unit Tests

Target file:

```text
tests/test_rllib/test_unit/test_explain/test_policy_scorer.py
```

Test cases:

- `MockPolicyScorer.score_all` returns one score per action for each observation;
- `MockPolicyScorer.score_action` returns the selected action scores from the
  same table as `score_all`;
- DQN scorer contract requires exactly 26 action scores for radial movement;
- scorer output includes an explicit score type such as `q_value`, `logit`, or
  `log_probability`;
- unsupported algorithms fail before attribution starts.

### Layer 4: Occlusion Explainer Unit Tests

Target file:

```text
tests/test_rllib/test_unit/test_explain/test_occlusion_explainer.py
```

Test cases:

- feature masking changes only the requested feature group;
- grouped occlusion returns one attribution value per configured group;
- chosen-action target explanations and action-margin target explanations are
  both supported;
- background observations are used as mask values instead of all-zero defaults;
- reports include `chosen_ray_hit` and `chosen_ray_type` groups for collision
  explanations.

### Layer 5: Report Builder Unit Tests

Target file:

```text
tests/test_rllib/test_unit/test_explain/test_report_builder.py
```

Test cases:

- collision visibility is computed from pre-action `ray_hits[action]`;
- collision type is read from pre-action `ray_hit_types[action]`;
- best safe action excludes actions whose ray type is occupied, boundary, or
  filled;
- score margin is `chosen_score - best_safe_score`;
- report JSON preserves enough data to compare a collision action against the
  best safe action in the replay viewer.

### Layer 6: Backend Smoke Test With Mocked Collaborators

Target file:

```text
tests/test_rllib/test_integration/test_explain/test_backend_smoke.py
```

Test case:

- construct `PolicyExplanationBackend` with an in-memory `ObservationTrace`,
  `MockPolicyScorer`, `CollisionStepSelector`, `OcclusionExplainer`, and a temp
  output directory;
- explain one visible collision where `ray_hits[action] == 1.0` and
  `ray_hit_types[action]` is filled or boundary;
- assert the backend returns an `ExplanationReport`;
- assert the report writer creates `report.json`;
- assert no CLI, checkpoint restore, Ray cluster, or optional SHAP dependency is
  required.

### Layer 7: Real DQN Checkpoint Integration Test

Target file:

```text
tests/test_rllib/test_integration/test_explain/test_dqn_checkpoint_scoring.py
```

This test should be added after the mocked backend is stable.

Test case:

- restore a small deterministic DQN checkpoint fixture;
- collect or load a short deterministic evaluation trace;
- call `DQNPolicyScorer.score_all`;
- assert every selected observation receives 26 Q-values;
- assert backend output names the score type as `q_value`;
- mark or skip the test clearly when the checkpoint fixture is unavailable.

### Layer 8: Optional Dependency Tests

Target files:

```text
tests/test_rllib/test_unit/test_explain/test_optional_dependencies.py
tests/test_rllib/test_integration/test_explain/test_shap_backend.py
```

Test cases:

- requesting SHAP without the dependency fails with an actionable install hint;
- requesting Captum without the dependency fails with an actionable install hint;
- when SHAP is installed, grouped SHAP can run on the same mocked backend fixture
  used by the occlusion smoke test.

### Execution Order

Recommended local validation order:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_rllib\test_unit\test_explain -q
.venv\Scripts\python.exe -m pytest tests\test_rllib\test_integration\test_explain\test_backend_smoke.py -q
.venv\Scripts\python.exe -m pytest tests\test_rllib\test_integration\test_explain\test_dqn_checkpoint_scoring.py -q
```

The first implementation is accepted when layer 1 through layer 6 pass.  Layer 7
is the checkpoint-backed confidence test, and layer 8 is optional dependency
coverage for later explainer backends.
