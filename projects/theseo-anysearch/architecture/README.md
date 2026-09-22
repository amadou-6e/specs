---
title: Theseo AnySearch architecture
status: active
kind: architecture
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
supersedes: null
related: [../README.md, ../subsystems/README.md]
---

# Theseo AnySearch architecture

Theseo AnySearch is a local-first reinforcement-learning system for routing agents
through voxel worlds. Python owns configuration, orchestration, framework adapters,
training, evaluation, and artifact publication. Rust owns performance-sensitive world
state, environment transitions, extension execution, and native replay rendering.
RLlib and Ray supply the learning and distributed-execution runtime; they are external
frameworks, not owners of Theseo's environment semantics.

This map was checked against implementation revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`. Subsystem contracts remain authoritative
for observable behavior; this page owns only their relationships and shared flows.

## Contained elements

```text
architecture/
├── 1 README.md
├── 1 template.md
├── 0..* focused architecture documents
└── 0..* editable diagrams
```

Use [template.md](template.md) for a focused document when a relationship spans
multiple subsystems or establishes a system-wide invariant. Decisions own durable
rationale, and subsystem contracts own public behavior.

Current focused views:

- [Command-line architecture](cli.md) maps commands across configuration,
  orchestration, artifacts, tracking, and native-tool boundaries.
- [Configuration architecture](configuration.md) maps configuration ownership,
  resolution, translation, and identity boundaries.

## System context

```text
experiment author / operator
          |
          | YAML, CLI commands, checkpoints, trajectories
          v
+----------------------- Theseo AnySearch ------------------------+
| Python CLI -> typed configuration -> experiment orchestration   |
|                                  |                              |
|                    RLlib / Ray training loop                    |
|                                  | PyO3                         |
|                                  v                              |
|                    Rust environment + world                     |
|                                  |                              |
|                    artifacts -> native replay UI                |
+-----------------------------------------------------------------+
       |                    |                         |
       v                    v                         v
 optional world       MLflow/TensorBoard       filesystem/object
 provider packages      derived views               storage
```

External actors are experiment authors and operators. External systems are RLlib/Ray,
optional world-provider and Model Garden packages, tracking services, and configured
artifact storage. The project boundary includes the Python package, Rust/PyO3 module,
extension SDK, and native replay binaries. Provider packages and Model Garden publish
inputs through compatibility boundaries; they are not internal subsystems.

## Components and ownership

| Component | Responsibility and state | Principal boundary |
| --- | --- | --- |
| CLI and experiment loader | Resolve commands and YAML into typed experiment models; locate runs and tools. | Python API and filesystem; see [CLI](cli.md) and [configuration](configuration.md). |
| [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) | Immutable occupancy, compiled packs, bounded reads, and per-episode overlays. | Python geometry inputs and Rust world interfaces. |
| [Environment runtime](../subsystems/environment-runtime/README.md) | Authoritative reset/step transitions, actions, rewards, masks, lifecycle outcomes, and diagnostics. | Gymnasium/PettingZoo in Python over PyO3/native state. |
| [Observations and policy models](../subsystems/observations-and-models/README.md) | Policy-facing schemas, normalization, model compatibility, logits, and value outputs. | Environment observations to RLlib modules. |
| [Training and tuning](../subsystems/training-and-tuning/README.md) | Trainer construction, staged execution, evaluation, pretraining handoff, Tune trials, checkpoints, and stopping. | Typed settings to RLlib/Ray and run artifacts. |
| [Experiment tracking](../subsystems/experiment-tracking/README.md) | Publish normalized run facts to local metadata, TensorBoard, and optional MLflow. | Local artifacts are authoritative; services are derived views. |
| [Trajectory and replay](../subsystems/trajectory-and-replay/README.md) | Trajectory capture, replay schemas, artifact lookup, and native visualization. | Python writers/filesystem to Rust replay process. |
| [Policy explainability](../subsystems/policy-explainability/README.md) | Restore an identified policy decision and produce bounded diagnostic reports. | Checkpoint, observation/trajectory, RLlib module, report artifacts. |
| Environment-rule extensions | Discover, validate, build, and execute optional native predicates, rewards, outcomes, and scenarios. Extension instances may own episode-local state but not the world or trainer. | Python discovery/build preflight to the Rust extension ABI; the [environment runtime](../subsystems/environment-runtime/README.md) owns execution semantics. |

Python process state includes resolved experiments, trainers, evaluation controllers,
tracking clients, and artifact writers. Native environment instances own live world and
episode state. Run directories own durable execution facts; tracking databases and UIs
must not become their only copy.

## Dependency relationships

The major dependency direction is intentionally one-way at the system boundaries:

```text
experiment configuration
    |-- selects world/task inputs --------------------+
    |-- selects environment and extensions --------+ |
    `-- selects observation/model/algorithm ------+ | |
                                                   v v v
worlds and geometry --> environment runtime --> observations/models --> RLlib/Ray
                              |                           |
                              +--> trajectory capture    +--> checkpoints/results
                                       |                           |
                                       v                           v
                                native replay              tracking/explanation
```

- Worlds and geometry supply resolved occupancy; they do not own route feasibility,
  episode lifecycle, or reward semantics.
- The environment runtime owns transitions and consumes geometry, task, action, and
  extension contracts. Observation adapters expose its results but do not replay its
  mutations independently.
- Training and tuning consume the environment and policy contracts. They own learner,
  evaluation, curriculum, checkpoint, and trial lifecycle, but not simulation truth.
- Tracking, replay, and explanation consume identified run artifacts. They must not
  become alternate writers of environment or learner state.
- Optional provider projects may publish compatible world/task artifacts. Their
  download, licensing, and source-specific derivation behavior remains outside this
  repository's runtime boundary.

## Principal flows

### Construction and reset

1. The CLI or Python caller selects an experiment YAML.
2. The loader parses it into typed experiment, algorithm, model, environment, and
   execution settings; preflight checks extension/provider compatibility.
3. Training orchestration registers the selected environment and model with RLlib.
4. Python constructs Gymnasium or PettingZoo adapters and translates settings across
   PyO3 into a native environment.
5. At reset, a task/scenario is selected, immutable base geometry is paired with an
   episode overlay, and observations are returned through the framework adapter.

### Training and evaluation

1. RLlib EnvRunners request observations and submit actions through the Python adapter.
2. Rust validates and executes actions, mutates native episode state, evaluates
   predicates/rewards/lifecycle rules, and returns results.
3. Python shapes the native result into the declared observation and framework API.
4. RLlib updates policy/value parameters; the Theseo trainer coordinates evaluation,
   curriculum/stage transitions, stopping, and checkpoint publication.
5. Normalized results are persisted locally and optionally projected into TensorBoard
   and MLflow. Tune repeats this lifecycle in resource-isolated trials.

### Artifacts, replay, and explanation

1. Evaluation collectors select episode evidence and write trajectory metadata plus
   occupancy sidecars or compiled-world references.
2. The replay CLI resolves the artifact and launches the separate Rust viewer process.
3. The viewer reconstructs frames from immutable geometry plus ordered overlay changes;
   it does not participate in the training process.
4. Explainability separately combines an identified checkpoint with a trace, scenario,
   or validated observation and writes diagnostic reports.

### Extension admission and execution

1. Python resolves configured extension references and validates manifests and ABI
   compatibility before constructing workers.
2. Native extension crates are built or located outside the transition hot path.
3. Rust loads admitted extensions and invokes them at their declared lifecycle points.
4. Extension failures remain explicit at the native/PyO3 boundary; Python must not
   reinterpret a failed callback as a successful transition.

## System-wide invariants

- Coordinate conversions occur at declared storage/task and Python/Rust boundaries;
  consumers must not infer indexing from tuple shape alone.
- Environment transition semantics are native-owned. Python adapters may translate
  protocols but must not independently reproduce state changes.
- A run is reproducible only from its resolved configuration, implementation identity,
  seeds, checkpoints, and referenced world/task artifacts—not from a tracking UI.
- Compiled-world and cache identities are content-derived and versioned. Mutable
  episode overlays do not alter the immutable base identity.
- Observation and action schemas must match the selected environment, model, algorithm,
  and checkpoint. Compatibility failures must be explicit.
- Evaluation routes/scenarios used for comparison must be deterministic under their
  declared seed and identity.
- Potentially large worlds cross boundaries through bounded queries or references;
  full materialization is not a general architectural assumption.

## Failure boundaries

- YAML/schema/compatibility failures stop before trainer construction and are presented
  by the CLI or calling Python API.
- Native construction, extension, or step failures cross PyO3 as explicit errors; the
  adapter must not fabricate a valid transition or action mask.
- Missing or corrupt world, checkpoint, and trajectory artifacts fail at their owning
  loader. Content-addressed caches may rebuild only when authoritative sources remain.
- Tracking-service failure is contained: training continues when permitted, but the run
  records degraded tracking. Local artifacts remain authoritative.
- Ray worker or trial failure is isolated by Ray/Tune at the execution boundary and is
  represented in trial/run status rather than silently converted into a result.
- Replay/rendering failure cannot mutate training state because the viewer is a separate
  artifact consumer process.

## Maturity and open boundaries

The architecture is implemented, but individual subsystem specifications remain draft
where their tests were inspected rather than executed. The legacy `garden` code inside
this repository coexists with the separately owned Model Garden project and requires a
documented migration boundary. `SurfaceEnv` and some older CLI compatibility paths also
need deeper subsystem-level audits; they do not change the ownership map above.

## Evidence and review limits

This map was traced at the revision named above through `pyproject.toml`, the CLI and
experiment loader, Gymnasium/PettingZoo adapters, RLlib registration and runner code,
the PyO3 module entry point, the native voxel environment/world implementation, the
extension SDK and environment-rule registry, tracking writers, and replay launchers.
The linked subsystem specifications supplied the detailed contracts.

This retrospective pass did not execute training, native-extension, replay, or failure
injection tests. Therefore, the map records implemented ownership and call boundaries,
not fresh performance or runtime-health evidence. The exact migration boundary for the
in-repository `garden` package and the depth of support for `SurfaceEnv` remain open and
belong in their owning subsystem specifications before this page can remove those
qualification notes.
