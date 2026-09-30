---
title: RLlib checkpoint integration
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib checkpoint integration

This guide describes AnySearch's checkpoint calls at product revision
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`, inspected on 2026-09-28.
It distinguishes the full-`Algorithm` training path from the module-only
explanation path. It does **not** certify portability, arbitrary configuration
changes, or inference equivalence after restore. The
[training-and-tuning contract](../../subsystems/training-and-tuning/contract/README.md)
owns checkpoint lifecycle and compatibility behavior; the
[policy-explainability contract](../../subsystems/policy-explainability/contract/README.md)
owns explanation provenance and score meaning.

## Full-Algorithm save and restore

`Trainer` constructs `CheckpointManager` with the environment's world contract
and the configured task contract. `Trainer.checkpoint()` passes the built
algorithm, iteration, and episode counters to the manager. `restore()` builds
an algorithm if needed, delegates restoration, and updates its counters;
`resume()` resolves the latest checkpoint first. [Trainer][trainer]

The manager creates `checkpoints/iter_%06d` beneath the run output, calls
`Algorithm.save()` with that directory, and records the nonempty path returned
by RLlib. Its `state.json` records iteration, episode count, `rllib_path`,
world and geometry/task contracts, and fingerprints. It also copies
`curriculum/state.json` and `early_stop_state.json`, when present, into
checkpoint-local `anysearch_state`; `latest.json` points to the latest
checkpoint. On restore it compares the expected world and geometry/task
contracts **before** calling `Algorithm.restore(state.rllib_path)`.
If `state.json` is absent, the fallback treats the directory as the RLlib path
and iteration as zero, but expected contracts make that fallback fail rather
than silently bypassing validation. [Checkpoint manager][manager] ·
[Task identity][task-identity] · [World manifest][world-manifest]

This is the AnySearch wrapper around RLlib's checkpoint API, not a description
of RLlib's own internal serialization. The recorded `rllib_path` and
`latest.json` path are used as stored; the inspected manager does not rewrite
them for relocation or hash the checkpoint tree. A moved bundle may therefore
need further handling, but relocation failure is **inferred, not tested** in
this audit. [Checkpoint manager][manager]

## Module-only explanation load

The explanation scorer has a separate path for DQN/PPO: it looks for
`metadata.json` beneath
`<project checkpoint>/learner_group/learner/rl_module/<policy_id>` and calls
`RLModule.from_checkpoint()` there. `from_run_dir()` reads `experiment.yaml`
and reconstructs a voxel environment and observation space using run geometry,
native-extension, reward, and scenario inputs. This path does **not** consume
the manager's `state.json.rllib_path`. Another DQN constructor builds an
`Algorithm` and restores from that recorded RLlib path; the explanation
service selects the module-only run-directory constructor for DQN/PPO.
[Scorer][scorer] · [Explanation service][explain-service]

The scorer accepts an explicit existing path, a named checkpoint, a numeric
`iter_%06d` selector, or `latest` via `latest.json`. Numeric selection does not
establish that the checkpoint exists until loading. The literal learner/module
subtree is a **version-sensitive assumption**: neither upstream RLlib layout
nor a real `RLModule.from_checkpoint()` round trip was verified in this audit.
[Scorer][scorer]

## Compatibility boundary

The inspected manager explicitly compares world and geometry/task contracts.
The task contract includes geometry identity, validation, waypoints, task, and
action mode; the world contract includes world coordinates and extent.
This does **not** establish full repeatability. No explicit model-architecture,
observation-space, RLlib-version, or extension-identity comparison was found
in the inspected manager. Other layers were not exhaustively inspected, so
this is a **manager-level finding**, not a system-wide absence claim.
[Checkpoint manager][manager] · [Task identity][task-identity] ·
[World manifest][world-manifest]

The project dependency declaration allows `ray[default,rllib]>=2.9` with no
upper pin; the current checkout used for focused tests had Ray 2.58, but it is
not the pinned product source. This audit did not inspect upstream RLlib
checkpoint formats. Do not infer cross-version compatibility from the broad
dependency range. [Dependency declaration][pyproject]

## What the tests establish

At the pinned revision, the inspected `TestRestore` unit test uses a fake
algorithm to check counters, restore calls, and contracts. Explanation scorer
unit tests use fake algorithms/modules and selector fixtures; they do not load
a real learner-module checkpoint. A real-Ray PPO resume test trains for two
iterations, saves, constructs a fresh trainer, resumes, and checks the restored
iteration. SAC has a real resume test; inspected DQN integration tests save
artifacts but do not restore. These tests were **read, not run on the pinned
revision**. [Trainer tests][trainer-tests] · [Scorer tests][scorer-tests] ·
[PPO resume test][ppo-resume-test] · [SAC resume test][sac-resume-test] ·
[DQN integration tests][dqn-integration-tests]

On a materially different working checkout (`ed8982e`),
`.venv/Scripts/python.exe -m pytest
tests/test_rllib/test_unit/test_trainer.py::TestRestore
tests/test_rllib/test_unit/test_explain/test_policy_scorer.py -q` returned
**12 passed**. The focused real PPO command,
`.venv/Scripts/python.exe -m pytest
tests/test_rllib/test_integration/test_ppo_trainer_ray.py::TestPPOTrainerRayResume::test_iteration_matches_trained_count
-m ray -q`, returned **1 passed in 27.49 seconds** outside the sandbox: it
established a two-iteration save and fresh-trainer resume, checking
**iteration only**, not action or score equality. An earlier sandbox
attempt failed at Ray GCS startup *before checkpointing*; it is not evidence
of a checkpoint defect. None of these runs verifies the pinned baseline.

## Before treating a checkpoint path as supported

For an implementation change, inspect both `state.json.rllib_path` and the
actual RLlib tree produced by the target dependency version. Preserve the
project contract checks, then test on a clean checkout with locked versions:

1. Save and restore real PPO and DQN algorithms; compare representative
   inference outputs before and after restore, not just iteration counters.
2. Load a DQN/PPO `RLModule` through the explanation scorer's literal path
   and compare its scores with the full-algorithm path where applicable.
3. Change world, task/action mode, observation space, model architecture, and
   extension identity independently; record which layer rejects each mismatch.
4. Move and tamper with a checkpoint tree to measure actual selector,
   `latest.json`, and `rllib_path` behavior.
5. Repeat against each RLlib version claimed as supported, because the
   learner/module subtree and restore API are version-sensitive.

These are **required investigation cases before broader claims**, not tests
reported as passing. Keep training compatibility decisions in the training
subsystem and explanation validity decisions in policy explainability.

[trainer]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/trainer.py
[manager]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/checkpointing.py
[task-identity]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/environments/task_identity.py
[world-manifest]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/worlds/manifest.py
[scorer]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/explain/scoring.py
[explain-service]: https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/explain
[pyproject]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/pyproject.toml
[trainer-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_trainer.py
[scorer-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_explain/test_policy_scorer.py
[ppo-resume-test]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_ppo_trainer_ray.py
[sac-resume-test]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_sac_trainer_ray.py
[dqn-integration-tests]: https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_integration/test_dqn_trainer_ray.py
