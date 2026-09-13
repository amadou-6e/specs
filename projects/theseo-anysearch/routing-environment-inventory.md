# Routing environment inventory

Status: research shortlist, not a frozen experiment protocol.
Reviewed: 2026-09-13.

## Scope and admission rule

This inventory distinguishes a *routing task* (environment geometry, connection
demands, and a checkable result) from a scene, asset pack, simulator, or planner
implementation. "Viable" means useful for a specified research role, not that a
source is already licensed, ingested, or certified for Theseo. Keep upstream
tasks unchanged when reporting upstream benchmark results. Any added pipe radius,
bend rule, task pair, or obstacle is a separately named Theseo-derived task.

## Runnable task sources

| Source and direct entry | Supplied environment and task | Research role | Boundary before use |
| --- | --- | --- | --- |
| [Deng, Multi-Group Pipe Routing v1](https://arxiv.org/abs/2608.28697), [ancillary source](https://arxiv.org/src/2608.28697v1), [author repository](https://github.com/bladesaber/MAPF_Pipeline) | Procedural 32^3 3D grid, two corridor generators x two obstacle painters x three difficulty levels; terminals grouped into finite-radius, permanently occupying pipe networks; feasible witness and CBS/PBS/priority-planning baselines. The paper reports 100 instances per cell, or 1,200 distinct generated instances across 12 cells. | Primary synthetic *coupled 3D routing* candidate. Controlled morphology/topology and unsaturated hard cells make it useful for learned search guidance. | Generated corpus is not the same as a shipped immutable corpus. Freeze source revision, seeds, commands, and hashes. Independently validate continuous swept-segment clearance and witness validity before treating a solve as hard-feasible. Software/data reuse license is not established by the arXiv paper license. |
| [ShortestPathLab Industrial Plants](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/), [paper](https://benchmarks.pathfinding.ai/assets/pdf/Nobes2023.pdf) | Five industrial-plant-inspired voxel maps at 10 cm resolution, 2,000 source-target tasks each; average map size 227 million voxels. Endpoints are sampled adjacent to equipment. | Large-volume, held-out-layout 3D *point-path search* and encoder-transfer test. | No pipe radius, terminal tangent, bend, support, or multi-route coupling. Audit actual archive filenames, map/task pairing, and rights before ingestion. Inflated-obstacle variants are new tasks, not upstream scores. |
| [ShortestPathLab Descent](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/) | Thirty voxelized, internally traversable game levels with 2,000 tasks per map. | Distinct 3D room/corridor topology for generalization outside industrial layouts. | Point-agent navigation only; levels originate from a 1995 game, though the voxel benchmark is from 2023. Do not present it as modern engineering CAD. |
| [ShortestPathLab Sandstone](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/) | Eleven CT-derived pore-space voxel maps with 2,000 tasks per map. | Tight, irregular 3D passage control. | A point-path task in rock pores, not pipe installation; voxel/scan rights require audit. |
| [IHNF MEP plant-room routing](https://huggingface.co/datasets/IHNF/mep-plant-room-pipe-routing) | Seven JSON cases: room/equipment/obstacle geometry, pipe terminals, diameter/material, route outputs, and costs; optional Revit visualizations. Dataset states CC BY 4.0. | Reproducible *coordinated piping* cases and route-schema/evaluator design. | Paths are XY polylines with layer heights (2.5D), not arbitrary volumetric routes. Seven cases cannot serve as a broad training corpus. Reimplement and validate the cost/constraint checker before comparing novel solutions. |
| [OptiWindNet RouteSets](https://optiwindnet.readthedocs.io/latest/dataset.html), [dataset](https://zenodo.org/records/20053479) | 13,954 offshore wind-farm cable-network instances with multiple routed solutions, costs, runtimes, and many optimality bounds; CC BY 4.0 data release. | Adjacent multi-terminal network/topology and optimization control. | Embedded cable routes are planar. Useful for network design, not 3D obstacle-volume perception or harness clearance. |

The [Warframe voxel suite](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/)
also has routes (44 maps, 10,000 tasks per map), but the available v1 maps are
circa 2018 and prior visual inspection found sparse occupied geometry. Retain it
only as a low-priority point-search regression control; it does not answer the
request for inspectable, richly structured 3D environments.

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
4. For Industrial Plants, verify exact archives, task/map schema, geometry-level holdout, scale/memory needs, and permitted reuse. Keep its upstream point-path scores distinct from any Theseo finite-radius extension.
5. For any real-CAD-derived task, publish an explicit input/target separation, geometry and terminal provenance, licensing record, and independent validity checker. A historical installed route is a reference, not an optimum certificate.

This inventory does not change the frozen perception-encoder pilot gates or grant
permission to train on, redistribute, or report results from these sources.
