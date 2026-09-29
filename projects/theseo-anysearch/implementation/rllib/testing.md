---
title: RLlib testing
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib testing

This page owns placement and evidence for tests of our RLlib API adaptation.
[Python testing](../python/testing.md) owns the general pytest conventions;
[Ray testing](../ray/testing.md) owns proof of actual distributed execution.
The inventory is pinned to product revision
[`fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec).
The tests were inspected, not run at that revision. A declared test is not a
passing or supported configuration.

## Placement by contract

Keep an RLlib adapter test under `tests/test_rllib/` even when it needs real
Ray. Choose `test_unit/` for isolated configuration, conversion, and callback
logic with doubles; choose `test_integration/` when the assertion needs a real
RLlib `Algorithm`, training iteration, checkpoint, or Tune trial. Put generic
run orchestration in `test_experiments/`, CLI invocation in `test_cli/`, and
environment semantics in `test_environments/`. A mocked EnvRunner or placement
group does not prove live actors or resource use.

The annotated tree lists existing files at the pinned revision. Omitted
siblings remain where they are; it is a placement map, not a move request.

```text
tests/test_rllib/
├── test_unit/                                  # isolated RLlib adaptation
│   ├── test_settings.py                        # RLlib-facing settings conversion
│   ├── test_models.py                          # model selection/configuration
│   ├── test_cnn_models.py                      # CNN adapter configuration
│   ├── test_dqn_runtime.py                     # DQN learner/update logic
│   ├── test_ppo_rollout_config.py              # EnvRunner configuration API
│   ├── test_trainer.py                         # trainer build/orchestration logic
│   ├── test_parallel_evaluation.py             # evaluation adapter with doubles
│   ├── test_checkpoint_identity.py             # checkpoint identity handling
│   ├── test_rewards.py                         # RLlib reward adaptation
│   ├── test_canonical_metrics.py               # metric normalization
│   ├── test_tune_runner_resources.py           # requested Tune resources; not placement proof
│   ├── test_tune_lifecycle.py                  # Tune orchestration with doubles
│   ├── _tune_runner_support.py                 # helper, not a test
│   └── test_explain/                           # RLlib-facing explanation adapters
│       ├── test_policy_scorer.py               # module/checkpoint scoring path
│       └── test_feature_schema.py              # policy feature schema
└── test_integration/                           # real RLlib/Ray boundary
    ├── test_algorithm_coverage.py              # build/train trial declarations
    ├── test_ppo_trainer_ray.py                  # PPO train/save/resume
    ├── test_dqn_trainer_ray.py                  # DQN and Rainbow train/checkpoint
    ├── test_sac_trainer_ray.py                  # SAC train/save/resume
    ├── test_cnn_models_ray.py                   # CNN variants and restore
    ├── test_ray_ppo_real.py                     # PPO with real environment/evaluation
    └── test_tune_runner_ray.py                 # real Tune/placement/trial paths
```

Add cases to the file owning the assertion before creating another file.
RLlib checkpoint restore belongs in the relevant algorithm/model integration
test; explanation's module-only restore belongs in `test_explain/` unless a
real-checkpoint boundary requires a new integration test. Keep one clear
assertion for each supported API-stack combination, especially modern
RLModule/Learner versus legacy `Policy`/`TorchModelV2`. Registry membership
and configuration construction must be tested separately from trainability.
See [compatibility and testing](compatibility-and-testing.md) for the
unverified combination matrix and upgrade hazards.

## Selection and evidence

From the product root, after installing the project's test prerequisites:

```powershell
python -m pytest tests/test_rllib/test_unit -q
python -m pytest tests/test_rllib/test_integration -m ray -q
```

The second selection may start Ray, build algorithms, and take substantial
time. Inspect skips and exact dependency versions. The `ray` marker denotes
intended real-runtime selection; it does not itself prove remote actor
creation, successful training, or checkpoint fidelity. For a support claim,
record source SHA, Python/Ray/RLlib/Torch versions, test IDs, result and skips,
then verify the specific build, train, evaluation, and restore assertions.
