---
title: Command-line architecture
status: active
kind: architecture
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
supersedes: null
related: [README.md, configuration.md]
---

# Command-line architecture

## Purpose and scope

The `anysearch` command is the human-facing composition boundary across experiment
registration, training and tuning, artifact inspection, tracking, explanation,
geometry tooling, the optional model garden, and native replay. It owns command
dispatch, reference resolution at the command boundary, process launch, progress
presentation, and conversion of command failures into terminal output and exit status.
It does not own training, artifact, geometry, explanation, or replay semantics.

Command flags and task-oriented instructions belong to Typer help and the owning
subsystem guides. This page instead records how command families cross subsystem and
process boundaries. It describes product repository revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`.

## System context

The external actor is a local operator invoking the Python console entry point. Inputs
are experiment YAML paths, registered names, run selectors, geometry inputs, or
existing artifact paths. Outputs are terminal messages, registry updates, run-local
artifacts, and separately launched viewer processes.

```text
operator
   |
   | arguments, paths, selectors
   v
Python `anysearch` / Typer
   |-- registry + typed experiment loading --> local configuration and run artifacts
   |-- run orchestration --------------------> Ray/RLlib, trainers, Tune, tracking
   |-- explanation service -----------------> checkpoints + explanation artifacts
   |-- subprocess launch --------------------> TensorBoard, MLflow, native replay UI
   `-- geometry/model tooling --------------> owning tool and extension contracts
```

Ray, MLflow, TensorBoard, and the native replay binary are dependencies used by
particular command paths, not part of the command dispatcher itself. The model-garden
group is an optional-project integration surface and does not make its models part of
the core CLI contract.

## Components and ownership

`theseo_anysearch.cli.main` constructs the root Typer application. It implements the
current top-level experiment lifecycle commands and attaches the `replay`, `mlflow`,
`ray`, and `garden` groups. It also retains the deprecated `experiment`, `train`, and
`tune` groups. The command modules under `theseo_anysearch.cli.commands` adapt terminal
arguments to services; they are not alternate owners of those services' behavior.

| CLI edge | Data crossing the edge | Canonical owner |
| --- | --- | --- |
| experiment reference to configuration | registry name or path, resolved YAML, output override | [Training and tuning](../subsystems/training-and-tuning/contract/interfaces.md) and [configuration architecture](configuration.md) |
| run command to execution | typed experiment or sweep and run options | [Training and tuning](../subsystems/training-and-tuning/README.md) |
| run selector to inspection/tracking | run directory, metadata, event store, tracking URI | [Experiment tracking](../subsystems/experiment-tracking/README.md) |
| replay selector to native UI | resolved trajectory path or Tune directory, subprocess arguments | [Trajectory and replay](../subsystems/trajectory-and-replay/contract/interfaces.md) |
| explanation request to explanation service | checkpoint selector, trace/scenario, attribution settings | [Policy explainability](../subsystems/policy-explainability/contract/interfaces.md) |
| geometry command to compiler/provider tooling | source paths, compilation or extraction settings | [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) |

The experiment registry is local CLI state used to map short names to experiment
locations. Persisted experiment and run artifacts remain authoritative for execution
and inspection; a registry entry is not an experiment definition or run record.

## Data and control flow

### Start a run

1. `run` resolves a registered name or path through `theseo_anysearch.cli.registry`.
2. The experiment loader validates and resolves the YAML. The command applies an
   explicit output override and checks referenced geometry-pool availability.
3. A sweep expands into ordered experiment runs, a Tune definition delegates to
   `TuneRunner`, and an ordinary experiment delegates to `ExperimentRunner`.
4. The owning runner creates and updates run-local metadata, checkpoints,
   trajectories, metrics, and status. The CLI prints a summary and the returned run
   information; it does not independently reconstruct successful completion.

Framework imports needed only for execution are generally located inside command
functions or runner paths. This reduces the cost and failure surface of unrelated
commands, but the root module still imports its command groups and explanation command
adapters when the Typer application is constructed. Therefore startup is not a formal
guarantee that every optional dependency is deferred.

### Resolve and inspect existing work

`list`, `inspect`, `resume`, `repeat`, `show-data`, TensorBoard, MLflow, and replay
begin with a registry reference, run selector, or concrete path. Resolution produces a
specific run or artifact location before the command delegates to the corresponding
reader, runner, or external process. `list` deliberately reads raw YAML for display
and output-location discovery where possible; that display path is not typed
configuration validation.

Resume and repeat are execution operations, not mutations of the archived definition:
they load persisted run context and delegate the new work to the runner contract.
Tracking and replay consume artifacts and must not redefine their meaning.

### Launch another process

Replay locates and starts the separately built `voxel-replay` Rust binary. TensorBoard
and MLflow commands launch their respective viewer processes against resolved local
stores. Process lifetime, port availability, and executable discovery are failure
boundaries; none of these viewer launches changes whether the underlying run artifacts
are valid.

## System-wide invariants

- The supported training entry point is `anysearch run`; deprecated groups remain
  compatibility adapters and must not become the basis of new workflows.
- A short registry name resolves location only. Typed YAML and persisted artifacts
  retain their owning contracts and identities after resolution.
- CLI presentation may summarize or format subsystem output but must not introduce a
  second interpretation of configuration, metrics, trajectories, or world data.
- Commands that consume existing artifacts resolve a concrete artifact before
  launching a viewer or resuming work. Viewer availability is independent of artifact
  integrity.
- Python-to-Rust replay crosses a process boundary through serialized trajectory or
  compiled-world artifacts; rendering is not embedded in the training process.
- Paths displayed by the CLI are resolved according to the configuration or artifact
  contract that owns them, not uniformly relative to the shell working directory.

## Compatibility and failure boundaries

Typer performs command-line parsing before command execution. Registry and path errors
are presented by the relevant command and normally exit before training begins. Typed
configuration, runner, geometry, and explanation failures originate in their owning
subsystems; the CLI may add context but must not silently reinterpret them.

The deprecated `experiment`, `train`, and `tune` groups remain registered for backward
compatibility. Their presence does not imply behavioral parity with every newer
top-level workflow. `anysearch --help` and subgroup help are authoritative for the
installed revision's concrete command inventory.

A missing `voxel-replay`, TensorBoard, or MLflow executable prevents that viewer from
starting but does not corrupt a completed run. Conversely, finding a viewer executable
does not validate the artifact it is asked to open. Failures after orchestration begins
are recorded and recovered according to the runner and artifact contracts rather than
by the root Typer application.

## Related decisions and subsystems

- [Project architecture](README.md)
- [Configuration architecture](configuration.md)
- [Training and tuning](../subsystems/training-and-tuning/README.md)
- [Experiment tracking](../subsystems/experiment-tracking/README.md)
- [Trajectory and replay](../subsystems/trajectory-and-replay/README.md)
- [Policy explainability](../subsystems/policy-explainability/README.md)
- [Worlds and geometry](../subsystems/worlds-and-geometry/README.md)

No accepted decision record currently establishes the CLI grouping as immutable. New
command families should follow subsystem ownership and compatibility requirements
rather than treating the present Typer layout as a permanent architectural boundary.
