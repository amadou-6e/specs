# Target configuration state

Status: draft. Tracks [specs#101](https://github.com/amadou-6e/specs/issues/101).

## Outcome

The main experiment YAML composes typed geometry and task sources with training and
evaluation behavior. Complex geometry generation and reusable task catalogs may be
extracted into supporting YAML files without changing their schemas. Generated
manifests contain identities, derivation, and verification evidence.

## Configuration layers

### Main experiment YAML

The main YAML owns orchestration and runtime behavior:

- experiment identity, output, and seed;
- environment episode limits and runtime behavior;
- geometry-source references and residency controls;
- task-source reference or inline task definition;
- observation, action, reward, lifecycle, and scenario settings;
- training, validation, evaluation, tuning, staging, algorithm, and model settings;
- per-phase task eligibility and sampling/execution policy.

It remains possible to express a small experiment in one file.

### Supporting geometry YAML

A supporting geometry YAML is optional. It is used for procedural generation,
augmentation, candidate resampling, and structural acceptance when those settings are
too complex or reusable to keep inline. It does not own observations, actions, rewards,
or task selection.

File adapters remain geometry sources in the main schema. STL, URDF, 3D map, boxes,
verified-world bundles, and later adapters are not forced through the procedural
generation file.

### Supporting task YAML

A supporting task YAML is an optional external form of the same task schema accepted
inline. It contains fixed task definitions or a task-generation definition. A fixed
task catalog describes what tasks exist; it does not decide whether training,
validation, or evaluation uses them.

### Generated manifests

Generated artifacts own:

- content identities and exact resolved paths;
- source and license records;
- coordinate conversion and world compilation records;
- derivation provenance and explanation;
- verification action/movement assumptions and body geometry;
- reference route and verification evidence;
- resolved task selection for each episode or run;
- geometry and route overlap needed to audit evaluation claims.

These fields may be inspected or optionally pinned, but are not duplicated as mandatory
user-authored experiment fields.

## Unified geometry sources

All occupancy inputs use `env.geometry.sources`:

```yaml
env:
  geometry:
    sources:
      - type: stl
        path: assets/building.stl
        scale: 1.0
        padding: 2
```

A verified world is another source type:

```yaml
env:
  geometry:
    sources:
      - type: world
        path: worlds/wrh-plumb-0
        expected_identity: null

    maximum_decoded_bytes: 268435456
    prefetch_margin: 2
```

Initially, `type: world` remains exclusive with other occupancy sources because sparse
compiled-world transformations and combined provenance require their own accepted
contract. This limitation is explicit and testable; it does not justify a separate
top-level world-selection system.

The target adapter vocabulary includes boxes and STL already supported by typed
sources, plus reviewed URDF and 3D-map adapters when implemented. This specification
does not define every adapter's file-specific parameters.

## Inline and file-backed geometry generation

The same typed generation definition is accepted inline:

```yaml
env:
  geometry:
    generation:
      provider:
        name: obstacle_boxes
        parameters:
          count: [4, 12]
      augmentation:
        paste_boxes:
          count: [1, 5]
      acceptance:
        maximum_attempts: 20
        require_valid_geometry: true
```

or by reference:

```yaml
env:
  geometry:
    generation_file: geometry/obstacle-worlds.yaml
```

The file contains the `generation` payload, versioned with its schema. Mixed inline and
file-backed generation is rejected initially; implicit deep-merge precedence is not
defined.

Episode reachability, route difficulty, and step-budget checks do not belong to
structural geometry acceptance. They move to task generation or per-phase task use.

## Standard authored task catalog

A fixed routing task contains authored objective and classification fields:

```yaml
tasks:
  catalog:
    - id: route-01
      type: routing
      start: [12, 25, 4]
      goal: [83, 60, 17]
      family: single_pipe
      labels: [plumbing, long, vertical]
      body_radius_m: 0.02

    - id: inspection-route-01
      type: routing
      start: [10, 10, 4]
      waypoints:
        - [20, 20, 4]
        - [40, 35, 8]
        - [70, 60, 8]
      family: inspection_route
      labels: [inspection, multi-segment]
      body_radius_m: 0.02
```

For a multi-waypoint task, the last waypoint is the final goal. `goal` and `waypoints`
are mutually exclusive to avoid two final-goal sources.

`body_radius_m` is a task constraint: it states the clearance for which the task is
defined. It does not resize the configured agent. The loader must check compatibility
between the task constraint and the active agent body.

Authored task definitions do not contain an action mode, verification movement model,
provenance claim, derivation reason, world hash, or content hash. Agent and action
settings remain in the environment. Generated verification records capture the exact
assumptions used to validate a resolved task.

Readable `id` values support configuration. Immutable task identities are derived from
the normalized resolved task plus its bound world and recorded in generated manifests.

## External task catalog

The same catalog can be extracted:

```yaml
tasks:
  file: tasks/wrh-plumbing.yaml
```

```yaml
# tasks/wrh-plumbing.yaml
schema_version: 1

catalog:
  - id: route-01
    type: routing
    start: [12, 25, 4]
    goal: [83, 60, 17]
    family: single_pipe
    labels: [plumbing, long]
    body_radius_m: 0.02
```

`tasks.catalog` and `tasks.file` are mutually exclusive. Paths in a task file resolve
relative to that task file unless a field explicitly states otherwise.

## Tasks bundled with a world

A `type: world` geometry source may expose a verified task catalog. The experiment can
import it without copying its tasks:

```yaml
tasks:
  from_geometry_source:
    index: 0
```

The referenced source must be `type: world` and expose compatible tasks. Importing the
catalog does not select one task and does not assign a train/validation/test role.

## Generated episode tasks

Resampled endpoints use a task generator, not fixed catalog syntax:

```yaml
tasks:
  generate:
    type: routing
    family: random_navigation
    labels: [procedural, obstacle-routing]

    endpoints:
      strategy: free_cells
      distance:
        minimum: 20
        maximum: 80

    acceptance:
      maximum_attempts: 50
      require_reachable: true
      maximum_search_nodes: 100000
      recovery_margin_steps: 16
```

The generator resolves against the active geometry and `env.max_steps`. It validates
each accepted concrete task and records that resolved task's generated identity and
verification evidence. `env.max_steps` remains the sole episode step limit; the task
definition does not duplicate it.

## Per-phase task use

The catalog defines available tasks. Training, validation, and evaluation choose
eligible tasks by readable ID, family, or labels and define how to consume them:

```yaml
training:
  tasks:
    include:
      families: [single_pipe]
      labels: [plumbing]
    exclude:
      labels: [very-hard]
    sampling:
      strategy: uniform
```

```yaml
validation:
  tasks:
    include:
      ids: [route-01]
    execution:
      strategy: exhaustive
      episodes_per_task: 3
```

```yaml
evaluation:
  tasks:
    include:
      labels: [long]
    execution:
      strategy: exhaustive
      episodes_per_task: 10
```

Exact include/exclude conjunction semantics remain an open decision; they must be
specified before implementation rather than inferred from examples. Empty eligible
sets fail before training starts.

Generated evaluation tasks use explicit seeds or a materialized catalog so repeated
evaluation is stable.

## Experimental roles and overlap

The middle role is named `validation`, replacing `calibration`. Compatibility with
identity-bearing legacy artifacts is required.

A world is not intrinsically assigned to train, validation, or test. The role describes
how a resolved task is used by one experiment or study. Theseo permits:

- different routes in the same world across phases;
- the same route across phases when explicitly configured;
- whole-world holdout when the user selects distinct worlds.

Generated manifests report world, root-geometry, task, family, and label overlap among
phases. Tooling may warn when an experiment's stated generalization claim conflicts
with observed overlap, but it does not universally reject overlap.

## Expected main YAML shape

```yaml
env:
  geometry:
    sources:
      - type: world
        path: worlds/wrh-plumb-0
    maximum_decoded_bytes: 268435456
    prefetch_margin: 2

  max_steps: 256

  observation:
    mode: box
    box_radius: 16

  action:
    mode: discrete_26

  rewards:
    step_cost: -0.01
    collision_cost: -0.10
    goal_reward: 1.0

tasks:
  from_geometry_source:
    index: 0

training:
  tasks:
    include:
      labels: [plumbing]
    sampling:
      strategy: uniform

validation:
  tasks:
    include:
      labels: [long]
    execution:
      strategy: exhaustive
      episodes_per_task: 3

evaluation:
  tasks:
    include:
      labels: [long]
    execution:
      strategy: exhaustive
      episodes_per_task: 10
```

## Migration direction

The implementation migration must address:

- `env.waypoints_file` and inline waypoints -> `tasks.file` or `tasks.catalog`;
- fixed waypoint routes -> catalog tasks with `waypoints`;
- waypoint curriculum task-generation fields -> `tasks.generate` and per-phase task
  sampling, while curriculum advancement remains training orchestration;
- task-feasibility fields under `env.geometry.validation` -> task acceptance;
- geometry-pool/provider generation -> inline `geometry.generation` or
  `geometry.generation_file`;
- compiled-world and provider-world attachment -> `type: world` source;
- top-level `worlds` identities -> generated resolved manifest, with an optional
  expected world identity pin on the source;
- `calibration` -> `validation` with a tested compatibility path;
- hard world-level split rejection -> overlap reporting and user-selected policy.

During migration, old and new forms may both be accepted but cannot be mixed for the
same concern. The loader must issue actionable deprecation messages and prove that a
legacy configuration and its translated form resolve equivalently.

## Non-goals

- Defining every future geometry adapter's parameters.
- Allowing arbitrary composition with a disk-backed compiled world before sparse
  transformation and provenance contracts are accepted.
- Treating a verified reference route as an instruction shown to the policy.
- Letting task files change the agent action space or physical body silently.
- Automatically inferring an experiment's scientific generalization claim.
- Defining implicit merge precedence between inline and external configuration.

## Open decisions

1. Whether task coordinates use concise `start`/`goal` names with a declared coordinate
   frame or retain explicit `start_storage`/`goal_storage` names.
2. Exact include/exclude semantics when IDs, families, and labels appear together.
3. Whether task catalogs bundled in a world are implicitly available or require the
   explicit `from_geometry_source` declaration.
4. How curriculum stages refer to task IDs and generated-task difficulty without
   duplicating training-stage configuration.
5. Whether an optional strict study policy can reject selected overlap in addition to
   the required overlap report.
6. The compatibility lifetime and identity treatment for legacy `calibration`
   manifests and the current top-level `worlds` block.

## Acceptance criteria

- A simple fixed boxes/STL/world experiment can remain in one YAML.
- Inline and file-backed geometry-generation definitions normalize identically.
- Inline and file-backed task definitions normalize identically.
- A verified world is loadable through `env.geometry.sources` without a second geometry
  attachment mechanism.
- Fixed tasks, multi-waypoint tasks, and resampled tasks use typed, distinguishable
  schemas.
- Training, validation, and evaluation independently select task IDs, families, and
  labels and use explicit sampling/execution policies.
- Imported task metadata cannot change `env.action` or agent body settings; physical
  task constraints are checked for compatibility instead.
- Generated manifests record exact world/task identities, verification assumptions,
  and cross-phase overlap.
- Same-world/different-route experiments are supported.
- Empty task selections, incompatible world-task bindings, ambiguous mixed legacy/new
  fields, and changed expected identities fail before a run starts.
- Legacy configurations have tested translation or explicit rejection guidance.
