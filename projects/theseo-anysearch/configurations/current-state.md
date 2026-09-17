# Current configuration state

Status: implementation inventory. Tracks
[specs#101](https://github.com/amadou-6e/specs/issues/101).
Implementation reference: `theseo-anysearch` merge commit
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c` on `develop`.

## Main experiment YAML

The experiment YAML is already the composition root. Its principal blocks include
`experiment`, `env`, `training`, `evaluation`, `algorithm_config`, `model_config`,
`staging`, and optional world-selection metadata.

`env` contains both runtime concerns and inputs that construct an episode:

- agent count, episode step limit, seed, and trail mode;
- fixed waypoint file and waypoint curriculum;
- task success/termination contract;
- geometry, observation, action, reward, lifecycle, and scenario blocks;
- optional heterogeneous-agent and hunter/hunted settings.

The loader converts the typed nested settings into the legacy flat runtime dictionary
consumed by the Python and Rust environments.

## Geometry today

`env.geometry` accepts several overlapping generations of configuration:

- ordered typed small-world `sources` for boxes and STL;
- a reset-time Python or native geometry `provider` plus arbitrary parameters;
- legacy `stl_path`, `stl_paths`, `scale`, `scale_range`, `boxes`, `padding`, and
  geometry-pool fields;
- `grid_size` or a three-axis `extent`;
- a flexible geometry `pool` dictionary;
- geometry/task `validation` settings;
- one compiled-world path or a compiled-world catalog;
- expected world identity and worker-local node cache;
- runtime decoded-memory and prefetch controls.

The schema rejects important ambiguous combinations. A provider cannot be combined
with fixed, pooled, scaled, or compiled geometry. A compiled world cannot currently be
combined with small-world sources. Typed `sources` cannot be combined with runtime pool
or scale-range generation.

The `validation` block is misleadingly broad. At reset it may perform both structural
geometry validation and episode-task feasibility:

- validate start and goal bounds and occupancy;
- run bounded A* using the configured action directions;
- reject no-path or planner-budget-exhausted episodes;
- ensure shortest-path length plus recovery margin fits `env.max_steps`;
- derive path length, detour ratio, direction changes, vertical displacement, planner
  expansion count, and optional clearance diagnostics;
- accept or reject a candidate by a named difficulty band;
- resample a geometry-pool candidate up to `maximum_attempts`.

For a fixed world, validation failure raises rather than producing another world.

## Start and goal selection today

There is no single task-source abstraction. Start and goal can come from:

1. Rust fallback sampling of two geometry surface cells from the reset seed. This does
   not prove reachability.
2. A JSON `waypoints_file` containing one fixed `start` and `goal`.
3. Inline waypoints or an inline multi-waypoint route.
4. Trainer-broadcast waypoint pairs or routes.
5. A waypoint curriculum that samples visited stages and may generate new stages by
   random, monotonic-distance, goal-distance, segment-distance, explicit-route, or
   seeded-world-catalog behavior.
6. A scenario provider that can modify episode state.

The reset paths converge on native `set_waypoints`, but definition, sampling,
validation, and provenance remain distributed across separate settings and trainer
code.

## Verified worlds today

World providers generate a bundle containing occupancy, source/conversion/world
records, routing-task records, verified route references, a split record, previews,
rights evidence, and hashes. A generated bundle may contain several routing tasks.

`anysearch worlds add` currently creates a second configuration path:

- it writes a top-level `worlds` block containing role, study identifiers, bundle path,
  world/root/dataset/split identities, and one task identity;
- it compiles bundle occupancy into a world pack;
- it writes the chosen task start/goal into a generated waypoint JSON;
- it sets `env.geometry.extent`, `env.geometry.compiled_world_path`, and
  `env.waypoints_file`;
- it validates the resulting experiment YAML but does not start a run.

Current limitations include:

- only the `train` role is attachable even though the schema also names
  `calibration` and `test`;
- generated IFC-Bench worlds are assigned `test`, so the advertised `worlds add` path
  cannot attach them to training;
- task selection sorts by task identity instead of preserving provider order or
  exposing an explicit selection policy;
- geometry/root overlap across roles in one study is rejected even when distinct
  routes in familiar geometry are the intended experiment;
- generated identities are duplicated into user-facing YAML even though the bundle is
  authoritative;
- verified worlds are not represented as ordinary geometry sources.

## Task records today

Immutable routing-task sidecars combine several categories:

- objective: start and goal;
- classification: task family;
- physical verification assumption: body radius;
- planner/action verification assumption: movement model;
- provenance and derivation explanation;
- binding to an exact world identity;
- content-derived task identity.

This is appropriate for an audit record but too broad for a user-authored task
definition. In particular, an imported task must not configure the agent action space,
and users should not have to author generated provenance or identity hashes.

## Split terminology today

Manifests and world selections use `train`, `calibration`, and `test`. `calibration`
is intended as the held-out set used for checkpoint and hyperparameter selection, which
is conventionally named `validation`. The term is embedded in identity-bearing
artifacts, so renaming requires compatibility or migration rather than text-only edits.

## Consequences

- Simple fixed-world experiments expose implementation and provenance detail.
- Related task behavior is configured under waypoints, curriculum, geometry
  validation, world selection, scenarios, and trainer settings.
- Provider-produced worlds and directly imported geometry follow different YAML paths.
- It is unclear which fields are authored intent versus generated evidence.
- Reusing a task catalog across training, validation, and evaluation is difficult.
