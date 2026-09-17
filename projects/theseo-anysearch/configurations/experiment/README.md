# Experiment configuration boundary

Status: draft. Parent: [configuration architecture](../overview.md).

## Owns

- experiment name, seed, output, and reproducibility controls;
- environment runtime settings: episode limit, observations, actions, rewards,
  lifecycle, scenarios, agents, and residency budgets;
- references to inline or external geometry generation and task definitions;
- training, validation, evaluation, tuning, staging, algorithm, and model settings;
- phase-specific task eligibility and sampling/execution behavior.

## Does not own

- generated source/world/task identities except an optional expected-identity pin;
- derivation prose or verification evidence;
- third-party rights evidence;
- procedural geometry implementation details embedded into unrelated runtime blocks;
- an intrinsic train/validation/test classification of a world.

## Composition rules

- Inline and file-backed forms of one definition are mutually exclusive.
- Relative paths in the main YAML resolve from the main YAML's directory.
- Relative paths inside a supporting file resolve from that file's directory.
- Supporting files are validated independently, then composed into one normalized
  configuration before semantic cross-checks.
- No implicit deep-merge or silent override occurs between the main YAML and a
  supporting file.
- The normalized resolved configuration and artifact identities are written to the run
  manifest.

## Phase terminology

- `training`: experience may update the learner.
- `validation`: held-out use for checkpoint, threshold, or hyperparameter decisions.
- `evaluation`: final or reported assessment under an explicitly stated protocol.

The names describe use, not immutable world properties.
