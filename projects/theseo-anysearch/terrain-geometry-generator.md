# Terrain, Geometry, And Navigable Task Specification

Status: draft

Last audited implementation: `theseo-anysearch` `origin/develop` at `9bcd120` on 2026-09-02

Specification issue: [#17](https://github.com/amadou-6e/specs/issues/17)

## Purpose

Define one coherent geometry surface for AnySearch. Users must be able to add,
generate, validate, load, and reproduce geometries without accidentally creating
impossible tasks, unsuitable training distributions, or incomparable evaluations.

The architecture protects four separate questions:

1. **Geometry validity:** is the occupied world structurally well formed?
2. **Task feasibility:** can the configured agent solve this task in that world?
3. **Training suitability:** does the task provide useful difficulty and diversity?
4. **Evaluation suitability:** is the task stable enough for comparison?

A geometry can be valid while a selected start and goal are disconnected. A task can
be feasible but uselessly easy. A useful training task can still be unsuitable for
evaluation if it changes between iterations. These results remain separately testable
even when one pipeline invokes them together.

## Goals

- Preserve simple fixed boxes and STL loading for small experiments.
- Support varied synthetic obstacles and imported engineering geometry.
- Prove navigability after all geometry transformations and task placement.
- Characterize routing difficulty using the configured action space.
- Support deterministic training generation and stable evaluation suites.
- Use one logical artifact contract across in-memory and large disk-backed worlds.
- Allow Python and native extensions without allowing them to bypass validation.
- Support future terrain, engineering-scene, wiring, and connector-routing use cases.

## Non-goals For The First Delivery

- Applying dense NumPy transformations directly to compiled worlds.
- Generating production-quality automotive or aircraft CAD procedurally.
- Solving arbitrary multi-agent joint-motion planning in the first validator.
- Replacing the existing heuristic planners.
- Adding difficulty metrics before safe obstacle generation itself works.

## Current Implementation

### Working capabilities

| Capability | Current behavior | Appropriate use |
|---|---|---|
| Fixed boxes | Inclusive axis-aligned boxes become occupied voxels. | Controlled walls, gaps, corridors, and regression fixtures. |
| Fixed STL | One ASCII STL is voxelized into a cubic environment. | Small static imported scenes. |
| STL scale variation | `scale_range` samples a scale and rebuilds on reset. | Limited variation of one small mesh. |
| Offline geometry pools | `.npy` occupancy grids are sampled at reset and installed with `set_geometry()`. | Diverse small-world training. |
| Pool extraction | Multiple STL inputs, SO(3) rotations, scale variation, quality filters, atomic writes, and metadata. | Preparing reusable small-world datasets. |
| Random box augmentation | `paste_boxes()` adds random solid boxes to a sampled dense grid. | Mechanically generating obstacle layouts. |
| Runtime base replacement | Single- and multi-agent native environments expose `set_geometry()`. | Reusing an environment with a new small-world base. |
| Compiled worlds | `BoxSource`, `NpySource`, and `StlSource` compose into content-addressed chunk packs. | Large finite worlds and immutable geometry. |
| Regional residency | Compiled chunks are loaded, pinned, prefetched, and evicted under a memory budget. | Large-world training and simulation. |
| Bounded occupancy queries | Scenario providers query points and regions without full materialization. | Large-world task placement and validation. |
| Candidate indexes | Typed candidates are queried deterministically with budgets. | Spawn, goal, surface, and portal selection. |
| Heuristic planners | A*, Dijkstra, weighted A*, and replanning A* query live occupancy. | Feasibility, demonstrations, and references. |
| Compiled-world identity | Sources, extent, compiler settings, algorithms, and hashes identify a pack. | Cache reuse and reproducibility. |
| Replay references | Trajectories reference immutable bases and store overlays as deltas. | Large-world replay without duplication. |

### Existing but incomplete or unsafe capabilities

#### Ambiguous runtime and preprocessing settings

`stl_paths`, `pool_size`, and `scale_variants_per_map` appear beside runtime fields.
Normal construction directly handles one `stl_path`, inline boxes, an already-built
pool, or one compiled-world path. Multiple-STL and pool-generation settings primarily
belong to preprocessing. They need compiler-backed semantics or an explicit
preprocessing schema.

#### Implicitly exclusive source paths

The small-world builder selects `compiled world`, else `fixed STL`, else `inline
boxes`. STL and boxes do not compose through regular experiment YAML. Compiled worlds
and dense pool augmentation do not compose. Precedence must become explicit, and
conflicting legacy combinations must fail during preflight.

#### Unsafe box augmentation

`paste_boxes()` does not check whether it occupies the start or goal, disconnects
them, makes the required path exceed the episode budget, requires unavailable actions,
or produces an unsuitable or duplicate sample. It works mechanically but is not yet a
safe task generator.

#### Coarse pool validation

Extraction can require a large connected free-space component. That is useful
geometry validation, but it does not prove reachability for a later start/goal pair.

#### Geometry-unaware waypoint curricula

The record policy in AnySearch PR #217 learned a 96-action route on an empty 32-cubed
grid. `segment_distance` defines geometric waypoint spacing, not traversable path
length. Obstacles can invalidate or lengthen a segment. `monotonic_distance` currently
rejects populated geometry. A teacher finding a detour after selection does not make
the task generator safe.

#### Materialization and ingestion limits

Small-world boxes, STLs, and pools become Python lists of occupied coordinates. This
does not scale to large dense worlds. Fixed ingestion also expects ASCII STL, compiled
STL voxelization requires a cubic extent, and per-reset scale variation repeats
voxelization without a feasibility gate.

#### Candidate and mutation gaps

Compiled worlds can carry candidate indexes, but compilation does not automatically
produce task-specific candidates or prove their pairwise feasibility. The public
contract also does not fully state when base replacement or overlay mutation
invalidates identities, indexes, caches, or feasibility results.

## Required Concepts

### Geometry proposal

A typed description of sources and transformations before installation. Providers
return an inert proposal rather than mutating a live environment.

### Geometry validation result

Reports bounds, encoding, occupancy, free-space connectivity, and source integrity,
independent of a particular task.

### Task feasibility result

Reports whether one concrete task is solvable, including a path, path length, planner,
and rejection reasons. The first implementation supports one agent and one start/goal
pair, using the configured action mode.

### Training suitability result

Reports difficulty and diversity without deciding curriculum advancement. Initial
descriptors include shortest-path length, direct distance, detour ratio, direction
changes, vertical displacement, planner expansions, and optional clearance measures.

### Evaluation suite

A fixed collection of geometry/task identities stratified by difficulty and reused
across iterations, trials, checkpoints, algorithms, and machines.

## Immediate Delivery: Safe Random-Box Training

The first implementation wraps the existing pool plus `paste_boxes()` reset path. It
does not introduce a new planner or compiled-world transformation system.

```text
sample base pool geometry
-> paste random boxes
-> select start and goal
-> confirm both are free
-> run an existing heuristic with the configured action mode
-> confirm a path exists and fits the episode budget
-> accept, or reject and resample
```

### Required behavior

- Validate the final augmented geometry, not the original pool sample.
- Use a hard, positive attempt limit and fail clearly after exhaustion.
- Never silently fall back to unaugmented or easier geometry.
- Record categorized rejection counts.
- Produce identical accepted tasks for identical seeds and inputs.
- Preserve existing pool behavior when validation is disabled.
- Do not require difficulty metrics or persistent identities in this slice.

The validator compares heuristic path length with the actual episode budget. A caller
may reserve a recovery margin such as `episode_budget >= ceil(path_length * 4 / 3)`.
The margin is policy, not part of A*.

Failure categories include `start_occupied`, `goal_occupied`, `no_path`,
`path_exceeds_budget`, `planner_budget_exhausted`, and
`generation_attempts_exhausted`.

### Acceptance criteria

1. Random boxes cannot silently create an impossible accepted episode.
2. Endpoints are checked after every augmentation.
3. Existing A* proves reachability using only selectable actions.
4. Accepted paths satisfy the configured episode-budget rule.
5. Rejection and resampling are deterministic for a fixed seed.
6. Exhaustion reports categorized counts.
7. Training and evaluation can enable validation independently.
8. Tests cover occupied endpoints, disconnection, detours, budget overflow,
   action-mode differences, deterministic resampling, and exhaustion.

## Follow-up Milestones

### 1. Reusable validators

Extract geometry and feasibility validators from the first augmentation call site.
Apply them to fixed boxes, fixed STLs, pools, providers, and compiled worlds. Use
bounded occupancy reads for large worlds.

### 2. Difficulty characterization

Expose existing planner results instead of duplicating search. Support explicit
difficulty bands and balanced sampling across them.

### 3. Deterministic identities and stable evaluation

Hash base geometry, transformations, seeds, resolved task, action mode, validator
versions, and relevant planner settings. Extend existing dataset/world fingerprints.
Persist stable heterogeneous evaluation suites.

### 4. Typed source composition for small worlds

Replace implicit precedence with explicit sources and transformations:

```yaml
geometry:
  extent: [64, 64, 64]
  sources:
    - type: stl
      path: factory.stl
      scale: 40
    - type: boxes
      boxes:
        - [10, 10, 1, 12, 40, 20]
  transformations:
    - type: random_boxes
      count: [2, 8]
```

This initially targets in-memory worlds. It defines composition, validation order,
compatibility translation, and errors for ambiguous legacy combinations.

### 5. Geometry providers

Follow the scenario and reward extension pattern: read-only context and bounded world
queries produce a typed `GeometryProposal`, which the framework validates and
installs. Support deterministic Python providers first, then a versioned native ABI.

### 6. Unified artifacts

Define one logical artifact containing geometry identity, extent and coordinates,
provenance, occupancy representation, candidates, validation and difficulty metadata,
overview data, and schema/algorithm versions. Small worlds may load into memory;
large worlds retain regional residency.

### 7. Sparse compiled-world transformations

This is deliberately separate. Dense `paste_boxes()` cannot operate on a world whose
purpose is to avoid dense materialization. Evaluate compiling a new immutable world,
immutable augmentation layers, chunk-local generation, or validated episode overlays.

## Long-Term Geometry Sources

### Procedural terrain and clutter

Use height fields, signed-distance fields, and metaball/blob fields for terrain,
caves, ramps, trenches, and amorphous clutter. Blobs are not the main representation
for engineering assemblies.

### Procedural engineering scenes

Use CSG and parametric boxes, cylinders, channels, trays, brackets, ribs, clips,
connector blocks, ducts, housings, and panels. Compose equipment bays, cabins, racks,
chassis rails, pipe clusters, and machine frames.

### Imported real geometry

Use imported assets for realism and external validation. Follow-ups include binary
STL, optional external STEP conversion, normalization, watertightness diagnostics,
licensing provenance, and anchor annotation.

Research sources include the [ABC Dataset](https://deep-geometry.github.io/abc-dataset/),
[FeatureNet](https://github.com/madlabub/Machining-feature-dataset),
[FS-AI ADS-DV CAD](https://github.com/FS-AI/FS-AI_ADS-DV_CAD), and
[Berkeley cable-routing demonstrations](https://sites.google.com/view/cablerouting/data).
External assets require per-asset license review.

## Routing Anchors And Tasks

Real routing benchmarks need semantic anchors in addition to geometry. An artifact
should support connector points and normals, while tasks reference start/end anchors,
bundle radius, clearance, and required clips. Anchor placement and validation occur
after final geometry resolution.

## Determinism And Compatibility

- Fixed seeds determine attempts, transformations, candidates, and tie-breaking.
- Hash-map iteration order must not affect accepted geometry or routes.
- Algorithm and validator versions participate in persistent identities.
- Training may generate fresh accepted tasks; evaluation uses persisted identities.
- Legacy single-source YAML remains loadable through a canonical adapter.
- Previously ignored conflicting fields must fail or emit a time-bounded warning.
- Checkpoint restoration requires compatible model, observation, and action contracts.
- Imitation reuse additionally requires compatible geometry/task identity.

## Operational Diagnostics

The eventual CLI should offer `anysearch geometry validate`, `geometry inspect`, and
`geometry sample`. Reports include occupancy, connectivity, feasibility, path length,
detour ratio, rejection reasons, attempts, difficulty distribution, identities, and
representative replayable tasks.

## Open Decisions

1. Whether feasibility settings belong under augmentation, scenario generation, or a
   shared episode-preparation block.
2. Whether recovery margin is a ratio, fixed steps, or a completion condition.
3. Which planner expansion/time limit is safe inside reset.
4. When small accepted geometries first receive persistent identities.
5. How multi-agent feasibility adds collision and interaction constraints.
6. Which sparse transformation model governs compiled worlds.

## Verification Strategy

- Unit-test each validation result independently.
- Property-test fixed-seed determinism and coordinate bounds.
- Compare planner actions with the configured action space.
- Test compatibility translation and rejection of ambiguity.
- Benchmark reset throughput before enabling validation by default.
- Build stable fixtures for easy, detour, narrow, disconnected, and over-budget cases.
- Verify in-memory and compiled backends agree for the same bounded world.
- Link implementation issues and pull requests to specification issue #17.

## Implementation Work Items

| Order | Issue | Work item | Dependency |
|---:|---|---|---|
| 1 | [AnySearch #298](https://github.com/amadou-6e/theseo-anysearch/issues/298) | Validate augmented obstacle tasks and resample impossible episodes. | None; first unblocking slice. |
| 2 | [AnySearch #299](https://github.com/amadou-6e/theseo-anysearch/issues/299) | Extract reusable geometry-validity and task-feasibility contracts. | #298. |
| 3 | [AnySearch #300](https://github.com/amadou-6e/theseo-anysearch/issues/300) | Expose obstacle-routing difficulty descriptors and sampling bands. | #299. |
| 4 | [AnySearch #301](https://github.com/amadou-6e/theseo-anysearch/issues/301) | Persist geometry-task identities and stable evaluation suites. | #299 and #300. |
| 5 | [AnySearch #302](https://github.com/amadou-6e/theseo-anysearch/issues/302) | Add typed composable geometry sources for small worlds. | Can begin independently; integrate with #299. |
| 6 | [AnySearch #303](https://github.com/amadou-6e/theseo-anysearch/issues/303) | Add validated Python geometry-generation providers. | #299 and #302. |
| 7 | [AnySearch #304](https://github.com/amadou-6e/theseo-anysearch/issues/304) | Add a versioned native geometry-provider ABI. | #303 contract stabilized. |
| 8 | [AnySearch #305](https://github.com/amadou-6e/theseo-anysearch/issues/305) | Unify small and compiled geometry artifact contracts. | #301 and #302; coordinate with existing #296. |
| 9 | [AnySearch #306](https://github.com/amadou-6e/theseo-anysearch/issues/306) | Support deterministic sparse transformations of compiled worlds. | #305 and existing #296. |
| 10 | [AnySearch #307](https://github.com/amadou-6e/theseo-anysearch/issues/307) | Add geometry validation, inspection, and sampling CLI tools. | Basic form after #299; enrich after #300 and #301. |
