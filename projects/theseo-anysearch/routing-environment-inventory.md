# 3D routing environment inventory

Status: research shortlist, not a frozen experiment protocol.
Reviewed: 2026-09-13.

## Scope and admission rule

This inventory admits only routing through a 3D volume or a freely navigable 3D
space. It distinguishes a *3D routing task* (environment geometry, connection
demands, and a checkable result) from a scene, asset pack, simulator, or planner
implementation. Planar networks and XY routes constrained to prescribed height
layers are out of scope, even when their results can be rendered in 3D.
"Viable" means useful for a specified research role, not that a source is
already licensed, ingested, or certified for Theseo. Keep upstream tasks
unchanged when reporting upstream benchmark results. Any added pipe radius,
bend rule, task pair, or obstacle is a separately named Theseo-derived task.

## Runnable task sources

| Source and direct entry | Supplied environment and task | Research role | Boundary before use |
| --- | --- | --- | --- |
| [Deng, Multi-Group Pipe Routing v1](https://arxiv.org/abs/2608.28697), [ancillary source](https://arxiv.org/src/2608.28697v1) | Procedural 32^3 3D grid, two corridor generators x two obstacle painters x three difficulty levels; terminals grouped into finite-radius, permanently occupying pipe networks; feasible witness and CBS/PBS/priority-planning baselines. The paper reports 100 instances per cell, or 1,200 distinct generated instances across 12 cells. | Primary synthetic *coupled 3D routing* candidate. Controlled morphology/topology and unsaturated hard cells make it useful for learned search guidance. | The paper-cited GitHub repository returned 404 on 2026-09-13, but individual arXiv ancillary C++ files were retrievable; do not classify this as paper-only. A generated corpus is not a shipped immutable corpus. Freeze source revision, seeds, commands, and hashes. Independently validate swept-segment clearance and witnesses. No software/data reuse license was established from the arXiv release. |
| [ShortestPathLab Industrial Plants](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/), [paper](https://benchmarks.pathfinding.ai/assets/pdf/Nobes2023.pdf), [download repository](https://bitbucket.org/shortestpathlab/benchmarks) | Five industrial-plant-inspired voxel maps at 10 cm resolution, 2,000 source-target tasks each; average map size 227 million voxels. Endpoints are sampled adjacent to equipment. | Strongest published industrial-layout source for 3D *point-path search* and encoder-transfer tests. | No pipe radius, terminal tangent, bend, support, or multi-route coupling. Attribution instructions do not establish a data license; clear reuse rights before redistribution. Audit archive filenames and map/task pairing. Inflated-obstacle variants are new tasks, not upstream scores. |
| [ShortestPathLab Descent](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/) | Thirty voxelized, internally traversable game levels with 2,000 tasks per map. | Distinct 3D room/corridor topology for generalization outside industrial layouts. | Point-agent navigation only; levels originate from a 1995 game, though the voxel benchmark is from 2023. Audit data rights; do not present it as modern engineering CAD. |
| [ShortestPathLab Sandstone](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/) | Eleven CT-derived pore-space voxel maps with 2,000 tasks per map. | Tight, irregular 3D passage control. | A point-path task in rock pores, not pipe installation; voxel/scan rights require audit. |

## Compact drone navigation candidates

These sources are relevant to small, difficult flight volumes. A drone task must
allow free vertical motion and check the swept vehicle body, not just a point path
through a 2D floor plan. The source task and any Theseo-derived fixed-goal task
must be reported separately.

| Source and direct entry | Supplied geometry and task | Research role | Boundary before use |
| --- | --- | --- | --- |
| [Aerial Gym Simulator](https://github.com/ntnu-arl/aerial_gym_simulator), [bounded obstacle configuration](https://github.com/ntnu-arl/aerial_gym_simulator/blob/main/aerial_gym/config/env_config/env_with_lidar_nav_obstacles.py), [active-perception navigation examples](https://github.com/ntnu-arl/active-perception-RL-navigation) | Source-defined 3D obstacle and wall assets plus a drone navigation task. The cited configuration samples a bounded volume roughly 10-15 m wide in each horizontal axis and 6-10 m high; the active-perception work supplies 10-, 20-, and 30-obstacle inference examples. | Runnable compact flight-task candidate with controllable obstacle density and sensor observations. | Random obstacle count is not evidence of narrow-passage or multi-route topology. Audit actual placements, start/goal sampling, collision geometry, and licensing. Its Isaac Gym integration is substantial; exporting source geometry into a simpler voxel evaluator would be a derived task. |
| [AvoidBench](https://github.com/tudelft/AvoidBench) | Indoor and forest flight scenes; seeded random maps and start/goal trials with flight and environmental-complexity metrics. The Unity scene is distributed as a simulator release, and the runner can save point clouds. | External obstacle-avoidance benchmark with an existing flight-task protocol. | The scene is not supplied as a convenient raw collision-mesh corpus. Verify whether indoor trials require genuine 3D route choices rather than local avoidance. Keep upstream scores distinct from any extracted-voxel or fixed-pair task. The published setup targets Ubuntu 20.04/ROS Noetic. |
| [Gazebo maps: 3D maze and vertical tunnel](https://github.com/engcang/gazebo_maps) | Downloadable Gazebo world archives, including `3d_maze.tar.xz`; the repository documents a launchable `3d_maze/eazy_maze.world` and a vertical-tunnel scene. | Concrete compact geometry for held-out, topology-focused flight routes. | These are worlds, not a packaged start/goal benchmark. Inspect the collision model to confirm that height changes are necessary and no over-wall shortcut exists. Define reachable, clearance-checked task pairs and an evaluator before using them as evidence. |
| [CaveDroneSim](https://github.com/makarov-mm/cave-drone) | Source-generated 3D voxel chambers and tunnels, a partially observed occupancy map, simulated flight, and an exploration-and-return task. | Procedural irregular-tunnel family for testing an encoder under partial observation. | Its native objective is exploration, not fixed-goal path planning, and the source does not establish a small-volume benchmark. Freeze world dimensions/seeds, derive valid start/goal pairs, and separate those results from the upstream exploration task. |

For a derived compact-drone suite, control difficulty by minimum body clearance,
geodesic detour, and required altitude changes rather than obstacle count alone.
Candidate layouts include offset openings at different heights, overhead detours,
dead ends, and narrow vertical passages. Certify each case against a full-map 3D
planner after obstacle inflation, then hold out whole layout families and source
worlds during encoder selection. Report success, body collisions, path cost,
clearance, and planning latency; add dynamic-feasibility checks before claiming a
trajectory is flyable.

## 3D scene sources needing task construction

| Source | Downloadable geometry | Missing routing-task work |
| --- | --- | --- |
| [IRIS-v2 industrial room](https://zenodo.org/records/18671364) | Real 530 m^2 industrial room; aligned CAD, mesh, scans, pipe objects, and P&ID. The CAD archive is 81.8 MB. | No packaged new-pipe endpoints, installation constraints, or evaluator. Extract candidate connections, remove all target-route geometry from model input, and check leakage and permissions before making a derived benchmark. One room alone cannot support cross-site generalization. |
| [IFC-Bench MEP projects](https://huggingface.co/datasets/sylvainHellin/ifc-bench) | Building IFC scenes with discipline models. Candidate projects listed as CC BY 4.0 include `duplex`, `dental_clinic`, `sixty5`, and `wbdg_office`; `digital_hub` is listed as MIT. Confirm each model's `license.txt` and pipe/port census. | Existing QA questions are not routing tasks. Derive connections from IFC ports/systems or explicitly annotate them, with target segments removed from occupancy. Check that the model actually has connected pipe/duct/cable geometry and no route leakage. The previously cited `samuel_macalister_sample_house/mep.ifc` is GPLv3, despite the dataset-level CC BY label. |

IfcOpenShell exposes [geometry conversion](https://docs.ifcopenshell.org/ifcopenshell-python/geometry_processing.html)
and [distribution-port/system queries](https://docs.ifcopenshell.org/autoapi/ifcopenshell/util/system/index.html).
Those APIs make extraction plausible; they do not establish that any particular
IFC has complete, correct port connectivity.

## Small engineering fixtures, not benchmark corpora

- [PipeWiringOptimization](https://github.com/yeyeleijun/PipeWiringOptimization/blob/master/test_case/test.py): an explicit 20^3, five-pipe 3D test with terminal directions and radii. Its active obstacle list is empty; a box example is commented out. Useful for radius/bend and multi-route regression, not statistical ranking. No repository license was established.
- [Aker KBE pipe-routing assignment](https://github.com/Hallvaeb/automation-p3-pipe-routing): procedural 3D environment/equipment ports, diameter and elbow parameters, and a constructed connection sequence. Useful for terminal-direction and elbow-geometry fixtures; no general obstacle-search benchmark or independent evaluator was verified. No repository license was established.

Do not promote a rendered [HoloOcean](https://byu-holoocean.github.io/holoocean-docs/develop/packages/Ocean/PierHarbor/pierharbor.html)
scene, Mercuna video, UP-Bench planner repository, or the unpublished industrial
instances in [Belov et al.](https://harabor.net/data/papers/bddhkw-fmapft3dpr-socs20.pdf)
to this runnable list without actual downloadable geometry *and* route tasks.

## Required audit before the first comparative run

1. For Deng, reproduce the generator and baselines from one pinned source revision; save a seed-separated development/calibration/test manifest. A final set must not include development cases. Hold out at least one generator combination for morphology/topology transfer.
2. Independently validate every witness and returned route as continuous, finite-radius swept geometry against static obstacles and other groups. The published [`CompositeGrid::is_move_free` implementation](https://arxiv.org/src/2608.28697v1/anc/pipe_design/src/grid/CompositeGrid.cpp) checks cell centres for unit diagonal moves, which alone does not prove continuous clearance between centres. Recompute success if any route fails the independent checker.
3. Reproduce the published 26-connected/Manhattan low-level baseline, then add a matched admissible 3D-distance heuristic control before attributing gains to learned guidance. Report feasibility, success versus time, expansions, memory, and route cost separately by generator/difficulty cell.
4. For Industrial Plants, verify exact archives, task/map schema, geometry-level holdout, scale/memory needs, and permitted reuse. Keep upstream point-path scores distinct from any Theseo finite-radius extension. Because canonical endpoints are adjacent to equipment, measure and publish the fraction that remain valid at each proposed radius before selecting a derived task set; do not silently move endpoints or invent a collision exemption.
5. For any real-CAD-derived task, publish an explicit input/target separation, geometry and terminal provenance, licensing record, and independent validity checker. A historical installed route is a reference, not an optimum certificate.
6. Keep final geometries untouched during architecture and hyperparameter selection. Five Industrial Plant maps are too few to treat one held-out map as a precise estimate of generalization; report each map separately, and do not conflate a largest-map scale test with a pure topology test.

This inventory does not change the frozen perception-encoder pilot gates or grant
permission to train on, redistribute, or report results from these sources.
