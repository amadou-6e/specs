---
title: Configuration architecture
status: active
kind: architecture
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
supersedes: null
related: [README.md, cli.md]
---

# Configuration architecture

## Purpose and scope

Configuration is a cross-subsystem composition mechanism, not one monolithic
schema. This page maps how YAML becomes typed runtime state, where configuration
ownership lies, and where failures cross subsystem boundaries. Exact fields and
defaults belong to the Pydantic models and the linked subsystem contracts.

This view describes `theseo-anysearch` implementation revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`.

## Entry points and representations

There are two public loading paths:

- `settings.load_experiment(path)` delegates to
  `experiments.loader.load_experiment`. It is the experiment-oriented path used for
  plain experiments and sequential sweep documents.
- `settings.load_settings(path, overrides)` delegates to
  `settings.loading.load_settings`. It loads the smaller runtime `Settings` model
  and optionally deep-merges caller-provided overrides before validation.

Both paths parse YAML into ordinary mappings, select concrete algorithm and model
configuration classes from the RLlib registries, and then construct Pydantic models.
The principal typed representations are `ExperimentConfig`, `SweepConfig`, and
`Settings`. `ExperimentConfig.to_settings()` deliberately drops experiment-only
metadata such as rendering, tracking, Tune, and staging when producing trainer
settings.

## Plain-experiment resolution flow

```text
experiment YAML
    |
    v
yaml.safe_load
    |
    v
training.algorithm + training.model
    |
    +--> algorithm registry --> concrete AlgorithmConfig subtype
    +--> model registry ------> concrete ModelConfig subtype
    |
    v
ExperimentConfig validation
    |
    +--> root and cross-section validators
    +--> stage payload validation, when staging is enabled
    |
    v
experiment.output_dir resolution
    |
    v
runner / tuner / environment construction
```

For a plain experiment, an explicitly relative `experiment.output_dir` is resolved
against the YAML file's parent. If the field is absent, the YAML parent itself is
used. An absolute path remains unchanged. The resulting `ExperimentConfig` supplies
Python orchestration; its `EnvConfig` is converted by the environment bridge into
the native settings consumed across PyO3.

## Sweep and stage composition

A top-level `sweep` selects `SweepConfig` instead of `ExperimentConfig`. Each sweep
entry is recursively merged over `sweep.base`, its entry name is inserted into the
experiment section, and the result is independently typed and validated by
`expand_sweep`. Unlike the plain-experiment path, `expand_sweep` does not receive the
source YAML path and therefore does not perform the loader's YAML-relative
`output_dir` resolution. A caller that executes expanded sweeps owns any required
path normalization.

Staging is a separate composition layer inside `ExperimentConfig`. A stage
recursively overrides only `env`, `training`, `evaluation`, and `algorithm_config`.
The merged payload is retyped and revalidated before use. Policy-contract fields
such as the action, observation, grid size, algorithm, and model cannot change across
stages. This is stricter than an unvalidated dictionary overlay.

## Ownership

- [Environment runtime](../subsystems/environment-runtime/contract/configuration.md)
  owns actions, agents, lifecycle rules, episode sources, rewards, and runtime
  settings.
- [Training and tuning](../subsystems/training-and-tuning/contract/configuration.md)
  owns algorithms, resources, evaluation, staging, pretraining, stopping, Tune, and
  the distinction between learner and EnvRunner resources.
- [Observations and policy models](../subsystems/observations-and-models/README.md)
  owns observation/model compatibility and model-specific semantics.
- [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) owns geometry,
  compiled-world, coordinate, storage, and world-identity semantics.
- [Experiment tracking](../subsystems/experiment-tracking/contract/configuration.md)
  owns tracking destinations and publication behavior.

Root models compose these sections and enforce cross-section constraints. The fact
that a field is nested in `ExperimentConfig` or `Settings` does not transfer its
contract to the configuration loader.

## Cross-subsystem invariants

- A plain experiment becomes typed before runner, trainer, or environment
  construction.
- Algorithm and model selectors choose registered concrete configuration classes.
  Unknown selectors fail before training starts.
- Pydantic models reject unknown fields in the root and principal configuration
  blocks through `extra="forbid"`.
- Algorithm/environment constraints are validated at the composed root. Examples
  include single-agent restrictions, imitation support, and evaluation-dependent
  early-stop thresholds.
- Stage overlays are validated as complete experiment configurations and cannot
  mutate declared policy-contract fields.
- Configuration that affects an artifact's identity is interpreted by that
  artifact's owning subsystem; inclusion in YAML alone does not establish identity.

## Persistence and reproducibility boundary

For a standard run launched with a configuration path, the runner copies the source
YAML to the run directory as `experiment.yaml`. If no source path exists, it writes
the in-memory model as JSON under that filename. The copied source is not a canonical
serialization of every resolved default or path. Reproducing a run therefore also
depends on the implementation revision, registered configuration classes, defaults,
extension sources, and other artifacts recorded by their owning subsystems.

Tune has additional serialization and archive behavior in its runner. Consumers
must not assume that every execution mode persists configuration in the same form.

## Failure and compatibility boundaries

YAML parsing failures originate before typed configuration exists. Missing required
keys can fail during selector lookup or Pydantic construction. Unknown algorithm or
model names fail at the registry boundary. Field and cross-section violations fail
during model validation. Extension/provider preflight failures occur after loading
but before useful execution, while native conversion failures stop environment
construction at the Python-to-Rust boundary.

Compatibility helpers may accept documented historical access or merge forms, but
they must preserve meaning in the current typed representation. The earlier
architecture page's prospective five-section schema and claim that every section was
mandatory are not current universal contracts and are not retained as an alternative
schema.

## Known architecture gaps

- Plain-experiment and sweep `output_dir` normalization are asymmetric because sweep
  expansion lacks source-path context.
- Standard-run archival does not guarantee a canonical, fully resolved
  configuration snapshot.
- Algorithm and model registries live under the RLlib integration even though their
  selectors participate in general configuration loading.

These observations describe current boundaries; they are not requirements to change
them without an accepted decision or issue.

## Related documents

- [Project architecture map](README.md)
- [Command-line architecture](cli.md)
- [Environment runtime](../subsystems/environment-runtime/README.md)
- [Training and tuning](../subsystems/training-and-tuning/README.md)
- [Observations and policy models](../subsystems/observations-and-models/README.md)
- [Worlds and geometry](../subsystems/worlds-and-geometry/README.md)
- [Experiment tracking](../subsystems/experiment-tracking/README.md)
