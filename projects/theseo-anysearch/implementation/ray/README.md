# Ray implementation

This fixed partition owns contributor guidance for Ray runtime execution: process
initialization and shutdown, actor and worker lifecycle, resource allocation,
placement, task scheduling, concurrency, serialization across process boundaries,
and the execution costs and failure modes of vectorized environments.

## Contained elements

```text
implementation/ray/
├── 1 README.md
└── 0..* Ray implementation documents
```

Each additional document owns one bounded contributor rule or local workflow.
This partition does not create nested implementation categories.

## Boundary

RLlib defines `Algorithm`, `RLModule`, `EnvRunner`, checkpoint, and evaluation
configuration APIs. Their project-specific adaptation belongs in
[RLlib](../rllib/README.md). This partition investigates how those settings
execute on Ray actors/workers and how the repo initializes, schedules, monitors,
and cleans up distributed work. A setting can therefore be referenced in both
partitions for different reasons; neither page owns the training contract.

The [Python](../python/README.md) partition retains general package and
non-Ray multiprocessing conventions. Observable training, evaluation, and
reproducibility guarantees remain with their subsystem contracts.

## Contained guidance

These flat pages are draft implementation investigations; source-declared
configuration is not proof of live Ray execution.

The split preserves the prior `execution.md` audit at product revision
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`. Its pinned Ray tests were
read, not run. Earlier focused unit tests on a different checkout, `ed8982e`,
passed 18 tests across PPO rollout configuration, parallel evaluation, and DQN
runtime helpers; they do not prove live actor scheduling at the pinned revision.
Upstream Ray internals, external CI, and live cluster state were not inspected.

- [Runtime lifecycle](runtime-lifecycle.md): local/external initialization, reuse, and shutdown.
- [Trials and process boundaries](trials-and-process-boundaries.md): trainable serialization, extension loading, and trial cleanup.
- [Resources and placement](resources-and-placement.md): requested CPU/GPU bundles, Learners, EnvRunners, and trial placement.
- [Environment execution](environment-execution.md): runner counts, vectorization, and actual environment instances.
- [Evaluation execution](evaluation-execution.md): remote evaluation runners and local fallback.
- [Measurement and tuning](measurement-and-tuning.md): Ray-specific telemetry and resource sweeps; the benchmark PR remains open.
- [Ray test placement and evidence](testing.md): distributed test owners, markers, fixtures, and coverage limits.
