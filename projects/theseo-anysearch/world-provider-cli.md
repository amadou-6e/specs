# Installable voxel-world providers and worlds CLI

Status: proposed. Tracks [specs#93](https://github.com/amadou-6e/specs/issues/93).
This specifies the user-facing workflow and provider boundary, not a completed
implementation or authorization to train on any generated corpus. It builds on
the [routing geometry roadmap](routing-geometry-integration-roadmap.md) and its
source, world, task, reference, and split records.

## Outcome

A user can install a voxel-world provider with pip, discover it from the main
`anysearch` CLI, generate a reproducible world with verified routing tasks,
inspect automatically exported PNGs, and explicitly add that world to an
experiment configuration. Generation never starts training. A provider may
ship code and metadata, but generated worlds and third-party source checkouts
remain outside Git and are not bundled into the core package.

## Command contract

| Command | Required behavior |
| --- | --- |
| `anysearch worlds list` | List installed providers with versions, supported parameters and native resolution, plus locally registered generated worlds and their verification state. Reading the list has no generation or network side effect. |
| `anysearch worlds list --remote` | List discoverable downloadable provider distributions from a versioned catalog, clearly distinguished from installed providers. This may access the network, but does not install or execute provider code. Unavailable catalog access has a clear error; the local list still works offline. |
| `anysearch worlds <provider> --seed N --output DIR` | Invoke the named installed provider with validated parameters. Write an identified full-occupancy voxel world and task/reference records, independently verify each accepted task and route, and automatically render PNG previews. Report rejected task strata. Do not mark a failed or partial output verified. Refuse to overwrite an existing output directory. |
| `anysearch worlds add DIR --config experiment.yaml` | Check the world manifest, file hashes and verification report, then make an explicit, idempotent update to the existing training or tuning YAML. The config must unambiguously identify the target data role; refuse an ambiguous role or a root-geometry identity already assigned to a conflicting split. Show the proposed change and preserve unrelated settings. This command neither generates worlds nor starts a run. |

The separate `verify` and `preview` commands are not required in the normal
workflow because generation performs both. A future recheck command may be
added for imported or transferred worlds. Interactive `worlds view` and
replayer integration are deferred; PNG previews are the initial inspection
surface. Do not rename the commands above to `providers`, `generate`,
`attach`, or `add-to-pool`.

## Provider and world contract

- The core package owns the `worlds` command group, discovery/registration,
  manifest validation, independent task/route checking, previews, and YAML
  integration. Optional pip distributions register named providers through a
  versioned provider API; absent or incompatible providers produce actionable
  errors without breaking the core CLI. Provider-specific dependencies do not
  become mandatory dependencies of `theseo-anysearch`.
- A provider declares its version, source identity and rights, supported
  parameters and bounds, native voxel resolution, coordinate frame, world
  extent, output format, and task capabilities. Arbitrary CLI parameters are
  rejected rather than silently ignored. Remote catalog metadata is not
  trusted as an installed provider or as permission to use its outputs.
- A generated world stores complete binary occupancy, units, axis order,
  origin, generator version and seed, parameter values, source/license record,
  content hashes, task endpoints, movement and body-size rules, independently
  checked reference routes, and a verification report. The report states what
  was checked and what was not. A route feasible against voxel cubes is not
  thereby feasible for a continuous flight controller or optimal.
- Preview PNGs show occupancy and routes using named slice/projection views,
  coordinate axes, scale, start/goal markers, and a legend. They are derived
  artifacts, not the source of geometry truth. Rendering failures fail the
  complete generation command rather than producing a verified world with no
  inspection output.
- Training/tuning YAML references the immutable world identity and manifest
  path in its declared data role. The run loader checks hashes again and
  refuses missing or changed worlds. A world selected for train cannot be
  silently reused for calibration or test; all crops and observations from a
  root geometry retain the same split.

## CaveDrone provider boundary

The first provider wraps the pinned upstream CaveDroneSim
`World::Generate(seed)` source, preserving its native 192 x 56 x 192 grid and
0.5 m voxels. Its provider distribution may obtain the pinned source only by
an explicit, rights-recorded setup step; pip installation must not silently
download or compile an unverified upstream checkout. Generation records the
upstream revision and validates its source bytes before use. Seed changes
produce layouts within one generator family, not a held-out topology family.

`--seed` and `--output` are required in the initial CLI. Native resolution is
listed as a capability, not presented as a freely configurable CaveDrone
parameter. Any future `--voxel-size-m` option is a separately versioned
resampling conversion with a new world identity and fresh task/route checks;
it cannot claim the source generator natively produced that resolution.
Derived fixed-goal voxel routes remain distinct from CaveDroneSim's native
exploration-and-return objective and simulated sensor observations.

## Implementation order and acceptance

1. Implement the provider-neutral interface, CLI list/generate/add behavior,
   manifest validation, PNG previews, YAML integration, and synthetic fixture
   provider. Test offline discovery, missing/incompatible providers, parameter
   validation, deterministic identities, failed verification, corrupt files,
   preview failures, idempotent config updates, and split leakage. No
   third-party source is needed for its CI suite.
2. After that interface is reviewed and integrated, implement the CaveDrone
   pip provider against it. Reuse the existing source-faithful export and
   swept-sphere voxel-cube replay; verify a pinned seed twice with identical
   output hashes, rejected-task reporting, PNGs, and a YAML round trip. Do not
   include generated corpora or upstream source in the wheel or repository.

Each implementation task gets its own issue and PR. The CaveDrone issue is
dependent on the provider-neutral interface; stacking before review is not
the default. Neither task changes an active perception-encoder
preregistration or authorizes a new training run.
