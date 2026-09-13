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
from scene generators. A separately derived roofed-maze test then probes
transfer. This order gives an end-to-end measurement without adding CAD or
full simulator dependencies to the gate-bearing path.

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

| ID and issue | Depends on | Deliverable and source | Exit evidence |
| --- | --- | --- | --- |
| **[G0 #411](https://github.com/amadou-6e/theseo-anysearch/issues/411): contracts and fixtures** | This roadmap merged | Versioned source/world/task/observation/reference/split sidecars; tiny hand-built boxes, tunnel and invalid-query fixtures; source-rights register. | Deterministic IDs, round-trip coordinates, visible-versus-unknown separation, zero silent invalid inputs, and CI tests with no network downloads. |
| **[G1 #412](https://github.com/amadou-6e/theseo-anysearch/issues/412): first point-path slice** | #411 merged | Strict `.3dmap.zip` + `.3dscen` importer for ShortestPathLab `plant01`; compile via `NpySource`; fixed query runner and baseline. | One reproducible end-to-end report with source hashes, accepted/rejected query counts, search semantics, valid replayed paths, runtime, and peak memory. No claim of upstream score comparability until query columns and movement rules are verified. |
| **[G2a #413](https://github.com/amadou-6e/theseo-anysearch/issues/413): compact scene export** | #411 merged | Instantiate seeded Aerial Gym obstacle layouts; transform URDF **collision** bodies, walls, starts and goals into metric occupancy and task manifests. | Re-export is hash-identical; transformed collision samples agree with source geometry; task pairs include genuine detours and altitude-change cases. Components alone do not count as worlds. |
| **[G2b #414](https://github.com/amadou-6e/theseo-anysearch/issues/414): tunnel-family holdout** | #411 merged; optional for first training run | Export pinned CaveDroneSim voxel generator outputs and fixed-goal pairs separately from its native exploration task. | Generator version and seed reproduce maps; held-out chamber/tunnel layout families and clearance-checked tasks are explicit. Required before any tunnel-family generalization claim. |
| **[G3a #415](https://github.com/amadou-6e/theseo-anysearch/issues/415): dataset and controls** | #412 and #413 merged | Feed compact worlds into new geometry-ID-aware garden data manifests; keep full-world truth separate from sensor-visible input and independently checked local labels. Prepare matched frozen-code, raw-grid, spatial and shuffled-code controls. | Group splits by complete layout/site, with a topology-family holdout when multiple families exist; never split by crop or seed alone. Fix query/crop hashes and identical tasks for controls; test leakage and labels. No training run yet. |
| **[G3b #416](https://github.com/amadou-6e/theseo-anysearch/issues/416): training and assessment** | #415 merged; [specs#92](https://github.com/amadou-6e/specs/issues/92) preregistration merged; compute budget approved | Execute the compact encoder and frozen-code head comparison with fresh external-corpus dataset/query/run identities. | Resolved configs, resource use, geometry-level uncertainty, matched-control scores and failure strata assessed against the frozen protocol; no test-set model selection. |
| **[G4 #417](https://github.com/amadou-6e/theseo-anysearch/issues/417): roofed maze transfer** | #411 and #412 merged | Convert Gazebo SDF collision boxes and poses; create a separately identified roofed variant, not a replacement of the open-top `easy_maze.world`. | Roof underside, body radius, world bounds and source hash recorded; independent checker rules out overflight; connected, valid query pairs and a planar-only control identify whether the task truly needs 3D motion. If not, retain it only as an enclosed-maze case. |
| **[G7 #418](https://github.com/amadou-6e/theseo-anysearch/issues/418): comparative report** | #412, #416 and #417 merged; #414 only for tunnel claim | Paired benchmark of point planning, frozen-code heads and controls on identical geometry/query manifests; source-family and difficulty breakdowns. | Collision-free success and query coverage first, then route cost, clearance, expansions, time and memory with uncertainty across geometry IDs. Explicitly separate upstream and derived tasks. |

AvoidBench's native flight loop and IFC/STEP/IRIS/cabin-harness engineering
imports remain in the [asset inventory](routing-asset-inventory.md), **outside
this gate-bearing issue chain**. Open separate issues only after a reviewed
decision names the gate they answer, their rights are cleared, and a runnable
task contract exists. Do not use their absence to block #418 or claim they were
tested.

## Prescribed issue and PR resolution order

1. Review and merge specs [#85](https://github.com/amadou-6e/specs/pull/85),
   then [#87](https://github.com/amadou-6e/specs/pull/87), then
   [#89](https://github.com/amadou-6e/specs/pull/89). Before implementation,
   replace each task issue's pinned draft spec SHA with the exact merged
   governing SHA. Opening these issues does not authorize running experiments.
2. Implement **#411** first. Its reviewed `exp/411` PR must be merged into
   `exp/perception-encoder` before any source-adapter branch starts.
3. After #411, **#412**, **#413**, and **#414** may be implemented in parallel
   on distinct source modules. Each branch starts from the then-current
   integration tip and has its own reviewed PR. Their PRs may merge in any
   order; update a published branch from the integration tip before continuing
   if another merges first. #412 is the first runnable evaluation milestone.
4. Start **#415** only after #412 and #413 are merged. **#417** may start after
   #412 and proceed in parallel with #415/#416. #414 is not a prerequisite for
   the first compact training run.
5. After #415 defines the actual imported data contract, resolve
   [specs#92](https://github.com/amadou-6e/specs/issues/92) in a separate
   reviewed and merged preregistration PR. Start **#416** only after that
   merged spec is pinned in its issue and an explicit compute budget is
   approved. Freeze fresh data/query/run identities before training; review
   its evidence PR before integration.
6. Start **#418** after #412, #416 and #417 are integrated. Include #414 only
   if it has been integrated and a tunnel-family claim was preregistered;
   otherwise state the narrower source coverage. Review the result PR last,
   close each implementation issue explicitly after its accepted integration,
   and use a separate promotion issue to cherry-pick accepted commits to
   `develop`. No PR is merged solely because its predecessor passed CI.

```text
specs #85 -> #87 -> #89 -> #411
#411 -> {#412, #413, #414}
{#412, #413} -> #415 -> specs#92 -> #416
#412 -> #417
{#412, #416, #417} -> #418
#414 -> #418 only when claiming tunnel-family transfer
```

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
  flight requires obstacle inflation or swept-body validation beyond the
  present point-A* check; future piping adds its own route constraints.
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
2. **After G2a, and G2b if used:** inspect actual topology and leakage by layout family.
   If cases are mostly open space or planar, revise the generator and issue a
   fresh dataset identity before training; do not lower a score gate to admit
   uninformative worlds.
3. **After G3b/G4:** proceed to larger contexts only if the smaller frozen
   encoder has a measurable, reproducible advantage over the matched raw-grid
   and spatial controls on held-out geometries while retaining collision-safe
   routing. Otherwise use the failure strata to choose the next bounded task
   or observation design.
4. **Before any later simulator or CAD claim:** establish simulator deployment
   parity or CAD rights/route provenance under a separate reviewed task. Neither
   is part of this campaign's success claim.
