# Roadmap for integrating 3D routing geometries

Status: proposed implementation sequence, not an experiment preregistration or
authorization to use third-party assets for training. Tracks
[specs#88](https://github.com/amadou-6e/specs/issues/88). Based on the
[environment shortlist](routing-environment-inventory.md) and
[asset inventory](routing-asset-inventory.md) at specs commit
`8292e2cda7ccf3464d995b0233978caa6f411dd1`. Review the inventories and
source rights again before executing a package.

## Outcome and boundaries

The first deliverable is a reproducible, **external 3D point-path evaluation**
on one Industrial Plants map and its actual query file. The second is a
**controlled compact training family** with fixed geometry and query identities
from scene generators. Only then add roofed-maze transfer, simulator-native
flight evaluation, and engineering route constraints. This order gives an
end-to-end measurement before adding CAD or full simulator dependencies.

Do not relabel component models as environments, feasible reference routes as
optimal, or an occupancy array as a partially observed sensor input. An
upstream task and any modified radius, roof, crop, or obstacle set are separate
tasks. External data cannot be added to a frozen perception-encoder run:
experiments need a merged governing spec SHA and fresh dataset, split, query,
preregistration, and run identities.

## Existing implementation to reuse

The implementation anchors below are pinned to
[`develop@155d9e5`](https://github.com/amadou-6e/theseo-anysearch/tree/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a);
the experimental garden reference is
[`exp/perception-encoder@117bd8a`](https://github.com/amadou-6e/theseo-anysearch/tree/117bd8ad3d304d6f0a5a7f421cc7aa1bafae3fb2).

| Existing surface | Reuse | Work still needed |
| --- | --- | --- |
| [`environments/map3d.py`](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/map3d.py) | Loads `.3dmap.zip` occupancy and makes cubic crops. | Strict map validation and a separate `.3dscen` query parser. The current parser tolerates malformed coordinate lines and expands `rev_voxel` in Python. |
| [`worlds/compiler.py`](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/worlds/compiler.py) and [world-pack contract](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/docs/world_pack_format.md) | Compiles non-cubic `.npy` occupancy or boxes into hashed, chunked packs; the Gymnasium environment can use a compiled pack. | Keep meters, source transform, visibility, task queries, and provenance in sidecars; the pack is occupancy, not a complete dataset. For `plant01` (195 x 128 x 100, about 2.5 million cells), use the existing `.npy` path first; add direct sparse compilation only if a measured larger-map need warrants it. |
| [`environments/task_identity.py`](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/task_identity.py) and [`validation.py`](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/validation.py) | Content-addressed accepted tasks, endpoint checks, deterministic A*, and difficulty descriptors. | Add portable external-query metadata and an independent continuous or swept-body collision check. Current A* calls point occupancy; `clearance_radius` is used for descriptors, not route feasibility. |
| [`geometry_pool.py`](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/geometry_pool.py) and [garden pilot dataset](https://github.com/amadou-6e/theseo-anysearch/blob/117bd8ad3d304d6f0a5a7f421cc7aa1bafae3fb2/theseo_anysearch/garden/dataset.py) | Compact cubic `uint8` grids and geometry-ID-aware samples. | Preserve source/site/layout family and all crops under one split; add task and observation sidecars rather than silently mixing with the frozen synthetic pilot corpus. Storage is zero-based; live task coordinates are one-based. |

The target flow is:

```text
source files + rights record
    -> source-specific geometry/task adapter
    -> occupancy world pack + metric transform/provenance sidecar
    -> immutable task, observation, reference, and split manifests
    -> independent validity checks
    -> point planner evaluation OR compact encoder dataset OR native simulator
```

## Work packages

Each implementation package needs its own theseo-anysearch issue and
`exp/<issue>` branch from the then-current `exp/perception-encoder` integration
branch when it supports the perception campaign. Review its PR before merging
to that branch; selectively promote reusable code to `develop` under the
existing promotion workflow. No package below implies a merge or GPU budget.

| ID | Depends on | Deliverable and source | Exit evidence |
| --- | --- | --- | --- |
| **G0: contracts and fixtures** | This roadmap reviewed | Versioned source/world/task/observation/reference/split sidecars; tiny hand-built boxes, tunnel and invalid-query fixtures; source-rights register. | Deterministic IDs, round-trip coordinates, visible-versus-unknown separation, zero silent invalid inputs, and CI tests with no network downloads. |
| **G1: first point-path slice** | G0 | Strict `.3dmap.zip` + `.3dscen` importer for ShortestPathLab `plant01`; compile via `NpySource`; fixed query runner and baseline. | One reproducible end-to-end report with source hashes, accepted/rejected query counts, search semantics, valid replayed paths, runtime, and peak memory. No claim of upstream score comparability until query columns and movement rules are verified. |
| **G2a: compact scene export** | G0 | Instantiate seeded Aerial Gym obstacle layouts; transform URDF **collision** bodies, walls, starts and goals into metric occupancy and task manifests. | Re-export is hash-identical; transformed collision samples agree with source geometry; task pairs include genuine detours and altitude-change cases. Components alone do not count as worlds. |
| **G2b: tunnel-family export** | G0 | Export pinned CaveDroneSim voxel generator outputs and fixed-goal pairs separately from its native exploration task. | Generator version and seed reproduce maps; held-out chamber/tunnel layout families and clearance-checked tasks are explicit. Do not call its exploration score a fixed-goal routing score. |
| **G3: training and frozen-code evaluation** | G1 plus G2a; G2b optional extension | Feed compact worlds into new geometry-ID-aware garden data manifests, with full-world truth separated from sensor-visible input and independently checked local labels. Run frozen-encoder heads alongside raw-grid, spatial and shuffled-code controls. | Train/calibration/test split by source site and generator topology family, not crop or seed alone; fixed query/crop hashes; new protocol and run IDs; identical tasks for all controls; no test-set model selection. |
| **G4: roofed maze transfer** | G0, G1 | Convert Gazebo SDF collision boxes and poses; create a separately identified roofed variant, not a replacement of the open-top `easy_maze.world`. | Roof underside, body radius, world bounds and source hash recorded; independent checker rules out overflight; connected, valid query pairs and a planar-only control identify whether the task truly needs 3D motion. If not, retain it only as an enclosed-maze case. |
| **G5: native flight benchmark** | G1, a runnable planner interface | Run AvoidBench through its native Unity/ROS interface with pinned scenes and trials; log its sensor stream, outcomes and resource use. | Native flight metrics and versioned scene/trial IDs are reproducible. Do not treat an exported point cloud as ground-truth occupancy or equate simulator and voxel scores. |
| **G6: engineering track** | G0, G1, independent rights review | Start with Deng's 32^3 multi-pipe generator and small PipeWiring/Aker fixtures. Then assess IFC-Bench port and installed-route extraction; investigate IRIS and the cabin harness only if rights and topology permit. | Independent swept-volume, bend, terminal, inter-route and obstacle checks; installed target routes excluded from model input; each site held out whole. Rights-gated CAD never enters training by default. |
| **G7: comparative report** | G1, G3, G4; G5/G6 reported separately when ready | Paired benchmark of point planning, frozen-code heads and their controls on the exact same geometry/query manifests; source-family and difficulty breakdowns. | Collision-free success and query coverage reported first, then route cost, clearance, search expansions, time and memory with uncertainty across geometry IDs. Explicitly separate upstream tasks, derived tasks, and simulator-native scores. |

G1 is the first runnable milestone. G2a and G2b may proceed in parallel after
G0, with separate source-adapter ownership; G4 can proceed after G1 without
waiting for encoder training. G5 depends
on a closed-loop planner interface and may remain an external benchmark rather
than block G7. G6 is a distinct engineering objective and must not hold up the
drone/point-path track.

## Cross-cutting acceptance rules

- **Coordinate and collision fidelity:** record axis order, handedness, origin,
  meters per voxel, transforms, source collision class and outside-map policy.
  Test known box transforms exactly; sample interiors, surfaces, openings,
  diagonals and borders against the source collision model. Reject missing
  dependencies, unit ambiguity, non-watertight occupancy assumptions, and
  unbounded bypasses instead of silently fixing them.
- **Task validity:** preserve raw upstream query rows while resolving their
  semantics. Count every rejected query with a reason. For accepted tasks,
  require free start/goal, correct motion model, independent route replay and
  collision checks. A search timeout is not proof of no path. Finite-radius
  flight and piping require obstacle inflation or swept-body validation beyond
  the present point-A* check.
- **Topology and difficulty:** record component count, passage clearance,
  geodesic detour, direction changes, altitude displacement and whether a
  projected planar route exists. Sampling to a target obstacle percentage is
  not a topology guarantee. Keep planar, overflight and disconnected cases as
  named controls, not successes for a 3D-routing claim.
- **Experiment integrity:** keep all crops, partial observations, query
  variants and roofed versions of one source layout in the same split. Freeze
  corpus/query manifests before fitting, use a separate calibration pool,
  and report every seed/site. New external assets do not retroactively revise
  completed pilot outcomes or inherit their validation gates.
- **Rights and storage:** store source archives and generated corpora outside
  Git. Commit only converters, synthetic fixtures, manifests, source hashes,
  resolved configurations and compact reports. A public URL or downloadable
  CAD file is not a training or redistribution license; stop the affected
  source at the rights gate and continue with cleared sources.

## Decision checkpoints

1. **After G1:** if the scenario columns or published movement rules remain
   ambiguous, release parser/conversion evidence but label the benchmark
   `not_comparable`; do not report a published-route improvement. If they are
   verified, freeze the point-task suite before trying learned methods.
2. **After G2a/G2b:** inspect actual topology and leakage by layout family.
   If cases are mostly open space or planar, revise the generator and issue a
   fresh dataset identity before training; do not lower a score gate to admit
   uninformative worlds.
3. **After G3/G4:** proceed to larger contexts only if the smaller frozen
   encoder has a measurable, reproducible advantage over the matched raw-grid
   and spatial controls on held-out geometries while retaining collision-safe
   routing. Otherwise use the failure strata to choose the next bounded task
   or observation design.
4. **Before G5/G6 claims:** establish simulator deployment parity or CAD
   rights/route provenance respectively. Either may be deferred without
   blocking the already valid point-path and compact-world results.
