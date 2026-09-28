---
title: Ray measurement and tuning
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# Ray measurement and tuning

The adaptive resource benchmark in [AnySearch PR #57](https://github.com/amadou-6e/theseo-anysearch/pull/57), associated with [issue #61](https://github.com/amadou-6e/theseo-anysearch/issues/61), was **open on 2026-09-28**. The proposed behavior below is pinned to [PR head `feb62246`](https://github.com/amadou-6e/theseo-anysearch/tree/feb622462416cd2655d64b55114debd33b21b62a); it is **not current behavior** on the [product baseline `fd94554c`](https://github.com/amadou-6e/theseo-anysearch/tree/fd94554c9620096f94aaed95ffda6a1bbd4711ec). This page owns measurement mechanics and Ray-process costs. Benchmark validity and whether a recommendation is suitable for training belong to [training and tuning](../../subsystems/training-and-tuning/README.md).

## Proposed search and execution

The PR implements a PPO-only benchmark. Its defaults are one warm-up iteration, three timed iterations, three repeats, at most 16 environments per runner and 20 runners, a 95% GPU-utilization target, and a soft 30-minute limit. It first sweeps environments per runner with one EnvRunner, then sweeps EnvRunner count while holding the chosen environment count fixed. The worker limit is additionally capped at reported cluster CPUs minus one. It reuses an already initialized Ray runtime and shuts Ray down only when it initialized Ray itself. See [runner initialization](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L121-L177) and [sweep orchestration](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L266-L357).

Each repeat builds a normal Trainer/Algorithm, disables remote evaluation and per-EnvRunner GPU requests, warms up, then times `algo.train()` calls; it stops the Algorithm in `finally`. Build and warm-up time are excluded from measured throughput, although they contribute to overall benchmark duration. The soft time limit is checked before the **next candidate**, not during an active candidate. See [repeat measurement](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L451-L551) and [search stop checks](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/search.py#L14-L145).

## What the telemetry measures

The proposed throughput numerator is the delta of RLlib's lifetime sampled-step counter across timed iterations. **If that delta is zero, the code substitutes** `train_batch_size × measure_iterations`; that result is an estimate, not observed environment steps. See [step accounting](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L499-L531).

CPU time and resident memory are aggregated from remote EnvRunner PIDs discovered through `foreach_env_runner(local_env_runner=False)`; they are not whole-host or Learner measurements. GPU utilization, used memory, and power come from optional `nvidia-smi` polling; absent telemetry yields missing values rather than a measured zero. Consequently, these metrics cannot by themselves establish Learner efficiency or memory safety. See [process and GPU collection](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/telemetry.py#L74-L140) and [measurement window](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L492-L542). No explicit RAM or GPU-memory safety stop was found in the inspected search path; that is not a claim about all possible external resource limits.

## Stopping rule and recommendation boundary

The environment sweep stops after a configured number of throughput declines relative to the running best, beyond a tolerance. The worker sweep instead stops at a GPU-utilization threshold, candidate limit, or soft time limit; it chooses the highest-throughput worker candidate **among those visited**. Thus the worker sweep may stop before the true throughput peak or continue past a decline when utilization stays below target. This differs from [issue #61](https://github.com/amadou-6e/theseo-anysearch/issues/61)'s requested phase-two sustained-throughput-decline/resource-limit criterion. GPU utilization is a stop signal in the PR, not the optimization objective. See [worker search](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/search.py#L14-L70), [environment search](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/search.py#L73-L145), and [recommendation construction](https://github.com/amadou-6e/theseo-anysearch/blob/feb622462416cd2655d64b55114debd33b21b62a/theseo_anysearch/benchmarking/runner.py#L294-L337).

The PR includes [search, runner, telemetry, and report tests](https://github.com/amadou-6e/theseo-anysearch/tree/feb622462416cd2655d64b55114debd33b21b62a/tests/test_benchmarking), but they were **read, not run** in this investigation. Its author reports 68 tests and a real sweep in the PR description; those results and artifacts were not independently verified here. Before adopting the recommendation, verify the merged revision, test output, measured-step validity, stopping criterion, representative workload, and whether CPU/RAM/GPU limits were actually respected. Resource requests and placement are documented separately in [resources and placement](resources-and-placement.md).
