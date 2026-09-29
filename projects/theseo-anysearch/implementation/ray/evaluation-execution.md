---
title: Ray evaluation execution
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray evaluation execution

Source baseline: [`theseo-anysearch` fd94554c](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec), inspected 2026-09-28. Pinned-revision Ray integration tests were read, not run. Evaluation semantics belong to [training and tuning](../../subsystems/training-and-tuning/README.md); this page concerns execution location.

## Where episodes execute

Regular evaluation defaults to enabled every training iteration with one episode, base seed 42, and **zero** dedicated evaluation runners. `parallel_to_training` defaults off and validation requires it to be enabled with at least one dedicated runner before it can be requested. Thus the default configuration is a local evaluation path, subject to the collector's runtime branch below. [Evaluation settings](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/settings/evaluation.py#L24-L60).

The custom collector selects its execution path by inspecting `algorithm.eval_env_runner_group` and `healthy_env_runner_ids()`, **not** merely by reading a configured parallel-evaluation flag. With no healthy remote ID, multi-agent episodes run sequentially through the local algorithm; single-agent episodes run locally through a policy adapter, either sequentially or in vectorized seed batches. A configured runner pool therefore does not by itself prove that an episode ran on a remote actor. [Collection branch](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L276-L329).

When healthy remote IDs exist, the collector uses at most one runner per requested episode, assigns consecutive seeds round-robin, and calls `foreach_env_runner` for those IDs with `local_env_runner=False`. The worker collects its assigned episodes, batching by `num_envs_per_env_runner` only for single-agent execution. The driver checks the returned episode count, sorts results by seed, and restores request order. These are source-level dispatch and ordering rules, not measured actor concurrency or episode parity. [Worker collection](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L244-L273), [dispatch and validation](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L331-L364).

## Policy state and callback lifetime

A direct remote collection call synchronizes evaluation weights by default, sourcing them from the Learner group on the new stack or the local EnvRunner on the legacy stack. The configured regular-evaluation callback deliberately invokes the same collector with `sync_weights=False`; its effective weight freshness therefore depends on RLlib's scheduling/synchronization outside this helper and is unverified here. [Callback invocation](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L43-L59), [sync branch and source](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L331-L384).

The callback stores its configuration but strips its weak `Algorithm` reference from serialized state; the built algorithm is bound afterward. Source shows this lifecycle but not a checkpoint round-trip for the callback. It returns episode reward, length, and count metrics and attaches the episodes to the algorithm for the trainer to consume. [Callback](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L10-L69), [configuration and binding](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L387-L430), [trainer consumption](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/trainer.py#L304-L334).

`evaluation_parallel_to_training` is forwarded to RLlib configuration; this code does not implement its own training/evaluation overlap. A configured value, reserved evaluation CPU bundle, or a test that returns the requested episode count does not establish actual overlap or actor placement. [Configuration](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/parallel.py#L387-L422), [Tune bundles](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/tune_runner.py#L1328-L1373).

The evaluation report's `max_evaluation_concurrency` is calculated as `min(episodes, max(num_env_runners, 1) * num_envs_per_env_runner)`. It is a configured upper-bound estimate, not a measured concurrent-episode count. [Coordinator report](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/rllib/trainer/evaluation/coordinator.py#L341-L386). The separate checkpoint-evaluation executor explicitly disables regular evaluation and its dedicated runners when reconstructing settings; its execution must not be conflated with this training-time callback. [Checkpoint executor](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/theseo_anysearch/experiments/execution_evaluate.py#L163-L170).

## Verification boundary

Pinned-revision tests were read, not run. The focused unit tests exercise fake runner groups, seed ordering, synchronization, and configuration; one same-named test definition is repeated, so the earlier definition is overwritten by the later one in Python and should not be counted independently. [Focused tests](https://github.com/amadou-6e/theseo-anysearch/blob/fd94554c9620096f94aaed95ffda6a1bbd4711ec/tests/test_rllib/test_unit/test_parallel_evaluation.py#L1-L310). Verify real-policy remote and fallback paths with actor identity, seed-to-episode identity, weight version, and timing traces before claiming execution parity or overlap. The RLlib evaluation settings/API belong in [environment integration](../rllib/environment-integration.md); requested runner resources belong in [resources and placement](resources-and-placement.md). No upstream Ray internals, external CI, or live cluster state were inspected for this page.
