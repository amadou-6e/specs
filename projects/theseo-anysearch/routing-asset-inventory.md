# 3D routing asset and integration inventory

Status: research and implementation planning, not an experiment authorization.
Reviewed: 2026-09-13. Tracks [specs#86](https://github.com/amadou-6e/specs/issues/86)
and depends on the [environment shortlist](routing-environment-inventory.md).

## What counts as an asset

Keep four records distinct: **geometry** (occupied/free/unknown space), **task**
(start, goal, vehicle or route constraints), **observation** (what the method can
see), and **reference** (a witness, route, or cost whose optimality is stated).
A scene or component model is not a routing task. A generated map is not an
independent held-out geometry merely because it has a different seed. The roles
below are proposals, not permission to train, redistribute, or amend a frozen run.

## Existing implementation entry points

These are from implementation commits
[`155d9e5`](https://github.com/amadou-6e/theseo-anysearch/tree/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a)
(`develop`) and
[`117bd8a`](https://github.com/amadou-6e/theseo-anysearch/tree/117bd8ad3d304d6f0a5a7f421cc7aa1bafae3fb2)
(`exp/perception-encoder`), not a claim about later code.

| Surface | Accepted input today | Important limit |
| --- | --- | --- |
| [World compiler](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/worlds/compiler.py) | Integer occupied boxes, 3D `.npy` occupancy, or ASCII STL; emits a hashed chunked world pack. | STL path requires a cubic extent and fit-normalizes the model. It is not a metric-preserving IFC, STEP, SDF, URDF, binary-STL, or point-cloud importer. |
| [3D map loader](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/map3d.py) | `.3dmap.zip` map to sparse occupied coordinates and cubic crops. | No matching `.3dscen` task parser found; `rev_voxel` expands the full volume in Python, unsuitable for large maps. It does not compile the zip directly into a world pack. |
| [Geometry pool](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/environments/geometry_pool.py) | `pool_meta.json` plus cubic `uint8` `.npy` files; 0 means free, 1 means occupied. | Pool sampling does not by itself preserve upstream task IDs, physical units, or geometry-family holdouts. Environment coordinates are one-based, array indices zero-based. |
| [Garden collectors](https://github.com/amadou-6e/theseo-anysearch/blob/155d9e527fe81a9fcb4276e3b7629b4de8d44c9a/theseo_anysearch/garden/data_config.py) | STL list, generated boxes, fixed environment, or prior run observations. | No external-world/task adapter. A fixed STL scale or independently fit-normalized crop must not silently replace source metric dimensions. |
| [Pilot corpus](https://github.com/amadou-6e/theseo-anysearch/blob/117bd8ad3d304d6f0a5a7f421cc7aa1bafae3fb2/theseo_anysearch/garden/pilots/corpus.py) | Frozen 65^3 procedural worlds and 17^3/33^3/65^3 crops. | Its family named `imported` draws synthetic ellipsoids; it is **not** evidence of an external-asset import. External corpora need new dataset/run identities. |

## Source assets and proposed roles

`Verified` means the file type was inspected in a public repository or an
ignored local sample. `Published` means the source describes it but the payload
was not inspected here. The proposed role is specific to the current research
question; it does not rename an upstream benchmark.

| Source | Geometry, task, observation and reference assets | Evidence and availability | Proposed use and missing adapter |
| --- | --- | --- | --- |
| [Deng multi-group pipe routing](https://arxiv.org/src/2608.28697v1) | C++ generator for 32^3 occupancy, terminal groups, finite-radius pipes, and feasible witnesses; no fixed released map corpus verified. | Published ancillary source; source license and generated-file schema still unaudited. | Candidate **training generator** and coupled-route test after pinned build/seed manifests and an independent swept-volume checker. Do not treat a feasible witness as an optimum. |
| [ShortestPathLab Industrial Plants](https://bitbucket.org/shortestpathlab/benchmarks/src/master/voxel-maps/industrial-plants/), [Descent](https://bitbucket.org/shortestpathlab/benchmarks/src/master/voxel-maps/descent/), [Sandstone](https://bitbucket.org/shortestpathlab/benchmarks/src/master/voxel-maps/sandstone/) | Per-map `.3dmap.zip` voxel geometry and `.3dscen` start/goal cases. Inspected `plant01`: ZIP member `plants/plant01.3dmap`, header `voxel 195 128 100`; scenario begins `version 2`, map name, then numeric query columns whose full semantics need verification. | Verified public file metadata and one downloaded pair. Plant geometry is 10 cm per voxel per the [benchmark](https://benchmarks.pathfinding.ai/3d-benchmarks/voxel-maps/); Descent and Sandstone directories use the same map and scenario extensions. No local full corpus. | Primary **external point-path evaluation**. Add a strict scenario parser, coordinate/occupancy checks, and a streaming or sparse map-to-world-pack path. Keep published point-agent tasks unchanged. Finite-radius pipe/drone variants receive new task IDs and endpoint-validity reports. Audit data rights before redistribution. |
| [Aerial Gym](https://github.com/ntnu-arl/aerial_gym_simulator), [navigation task](https://github.com/ntnu-arl/active-perception-RL-navigation) | Python scene/pose configuration plus URDF obstacle components, bounded walls, goal-conditioned flight and depth/LiDAR observations. Inspected panel and thin-obstacle URDFs use explicit collision boxes. The environment-assets tree contains 1,113 `.urdf` files, mostly component variants, **not** 1,113 complete worlds. | Verified public source tree and sample collision XML; no worlds exported locally. | Best candidate for **controlled compact training**: resolve collision-link transforms and seeded instance poses into metric occupancy, then derive fixed start/goal and difficulty manifests. Keep the native simulator task separate. Do not equate obstacle count with route topology. |
| [Gazebo maps 3D maze](https://github.com/engcang/gazebo_maps/blob/master/3d_maze.tar.xz) | `3d_maze.tar.xz` contains `.world`, nested `model.sdf` and `model.config`, box collision models, materials and a JPG texture. No route-query file. | Verified downloaded archive. `easy_maze_3d/model.sdf` places walls across about 90 m by 90 m; collision wall heights are 4 or 8 m; `easy_maze.world` has no flight ceiling. The separate vertical tunnel was **not** inspected. | **Derived test fixture only**, not an existing compact task. Resolve SDF `model://` includes and collision poses; add a collision roof with its underside below any wall top that must prevent overflight, accounting for drone radius. Give the roofed geometry a new ID and hash, preserve the original open-top world, and verify connectivity, clearance, and whether fixed task pairs require 3D motion. A roof alone can leave a planar maze. |
| [CaveDroneSim](https://github.com/makarov-mm/cave-drone) | C++ procedural dense voxel world (noise chambers plus random-walker tunnels), simulated LiDAR, partial-occupancy map, and exploration/return control loop. | Published source description; no exported map corpus or fixed-goal tasks verified. | Candidate **procedural training family** after generator/seed export, geometry-family split, independent clearance test, and fixed-goal task construction. Native exploration metrics must remain separate. |
| [AvoidBench](https://github.com/tudelft/AvoidBench) | Unity standalone release ZIP, YAML map/trial/goal parameters, ROS RGB/depth/odometry/goal topics, optional point-cloud export, and native flight metrics. | Published runner and task contract; raw collision-mesh access not verified. | **External flight evaluation** through its native interface. A point cloud is an observation, not a trustworthy solid occupancy map; voxel conversion would define a distinct task. Heavy ROS Noetic/Unity setup. |
| [IRIS-v2](https://centreborelli.github.io/scene-functional-alignment/), [data record](https://zenodo.org/records/18671364) | Zenodo record v2.0 lists PLY scan files, image and annotation ZIPs, a P&ID PDF, and `cad_model.zip`. Inspected CAD ZIP: `cad_model.fbx`, a binary PLY triangle mesh (about 1.19M vertices and 2.36M faces), and an object-tree TXT with `PIPING` and `CABLETRAYS` groups. Route connectivity and units remain unverified. | Verified Zenodo metadata and CAD archive members. The record declares **CC BY-NC-ND 4.0**; no training or redistribution approval follows from this inspection. | Later **rights-gated real-site transfer case**. First audit CAD entities and pipe provenance; use aligned scans as observations and structural CAD as collision reference. Remove any target installed route from model input. One room cannot estimate cross-site generalization. |
| [IFC-Bench MEP projects](https://huggingface.co/datasets/sylvainHellin/ifc-bench) | IFC discipline models; QA CSV is **not** a routing-task file. Locally present `duplex` architecture/MEP and `sixty5` electrical models are IFC2X3. | Verified local IFC headers; per-model licensing, ports, and route connectivity not yet checked. | Later **derived engineering evaluation** with IfcOpenShell geometry/port extraction, target-route removal, and independent collision checks. Split by building, not by individual query or nearby crop. |
| [Automotive cabin harness](https://www.cadcrowd.com/3d-models/cabin-harness-automotive-fusebox-battery) | Locally present 73 MB `.stp` assembly (`CONFIG_CONTROL_DESIGN` STEP header), including modeled harness and electrical packaging; not a complete car/engine bay. | Verified local header and [CC BY-NC listing](https://www.cadcrowd.com/3d-models/cabin-harness-automotive-fusebox-battery); route/solid structure not parsed. | **Reference/audit only** until legal scope and CAD topology are checked. No training, redistribution, or benchmark claim from the local file. |
| [PipeWiringOptimization](https://github.com/yeyeleijun/PipeWiringOptimization/blob/master/test_case/test.py), [Aker routing assignment](https://github.com/Hallvaeb/automation-p3-pipe-routing) | Source-defined small 3D grids or equipment/port fixtures and route constraints, not diverse scene archives. | Published source; see [shortlist caveats](routing-environment-inventory.md). | Unit/regression fixtures for radius, terminal direction, bends, and simultaneous occupancy, **not** a generalization corpus. |

Ignored local assets also include an older Warframe `.3dmap`/`.3dscen` copy,
individual OBJ/STL files, and Kenney/other model packs. They are **excluded**:
Warframe was removed by scope decision; standalone models and packs do not
become environments or tasks by voxelization. Their presence is not training
approval. No upstream asset or converted corpus belongs in the specs repository.

## Canonical conversion contract

Build optional, source-specific adapters at the input boundary. Feed collision
occupancy to the existing `.npy`/world-pack path, with immutable sidecars for
tasks, sensor observations, unknown space, and provenance; the world pack alone
does not represent those layers. Do not add IFC, CAD, or simulator dependencies
to the garden model or planner core. Every converted dataset needs:

1. **Source record:** upstream URL and revision/release, individual asset hashes,
   file/member paths, license and redistribution decision, generator version and
   seed if applicable, and exact conversion command/version.
2. **World record:** three-axis extent; meters per voxel; source-to-world rigid
   transform, axis order and handedness; zero-based storage coordinates; separate
   occupied, observed-free, and unknown states; collision-object classes and
   any excluded target-route object IDs. Geometry IDs must survive cropping.
3. **Task record:** task family (`point_path`, `drone_flight`, `single_pipe`, or
   `coupled_pipes`), start/goal in world and source coordinates, body shape/radius,
   clearance and turn constraints, query identity, and `upstream` versus `derived`
   provenance. A changed radius, ceiling, endpoint, obstacle, or target mask is a
   new task, never an upstream score.
4. **Observation/reference record:** sensor model and pose, visible/unknown mask,
   reference route or cost, and whether that reference is merely feasible,
   independently verified, or certified optimal. Never feed a hidden completion
   or installed target route into the encoder input.
5. **Split record:** geometry/site/layout/generator-family membership, train/
   calibration/test assignment, fixed query list, and hashes. All crops, masks,
   and randomizations of one base geometry stay on the same side of a split.

## Integration order

This is the source-priority summary. The reviewable implementation packages
and acceptance gates are in the
[3D routing geometry integration roadmap](routing-geometry-integration-roadmap.md).

1. **Prove the benchmark path on `plant01`.** Parse its `.3dscen` as structured
   task data, validate pairing and coordinates, and ingest sparse map cells
   without dense `rev_voxel` expansion. Compare a full-map classical baseline
   to the unchanged point-path cases before evaluating a learned head. Keep all
   five Industrial Plants as external evaluation unless a new split is justified.
2. **Build compact training worlds from analytic collision geometry.** Export
   Aerial Gym URDF collision boxes plus resolved scene poses, and separately
   export CaveDroneSim voxel seeds. Freeze generated worlds and task pairs before
   fitting encoders; select held-out layout families, not just different seeds.
   Use the same occupancy and query manifests for frozen-encoder and raw-grid
   controls.
3. **Add derived external stress cases.** Convert Gazebo SDF collision shapes,
   add a separately versioned collision roof, and certify bounded flight tasks.
   Run AvoidBench in its own simulator for flight-level comparison rather than
   pretending its point cloud is a full map.
   Descent/Sandstone remain independent point-path transfer controls.
4. **Attempt engineering CAD only after the simpler path is reliable.** Use a
   separate IFC/STEP/IRIS adapter to preserve metric scale and object IDs. Audit
   ports, historical route removal, rights, and independent swept-body validity
   before proposing real-assembly evaluation. Do not train on the NC harness.

For every adapter, reject unresolved units, missing collision dependencies,
unbounded overflight, invalid endpoints, and ambiguous free-versus-unknown
space. Compare source collision queries with the voxel checker at sampled
interiors, surfaces, openings, and diagonal motions. Record rejected cases and
source-level holdout counts rather than silently repairing them.

## Inspection evidence

The ignored implementation checkout held these samples at review time; they are
not committed specifications or a portable dataset:

| Sample | Observed content | SHA-256 |
| --- | --- | --- |
| `runtime/research-assets/plant01.3dmap.zip` | 197,911-byte ZIP; member `plants/plant01.3dmap`, `voxel 195 128 100`. | `0aa958fbf25db45d6e9c531ece0c1a2534e06caa4adf34ce301e05fd0d2ad8e3` |
| `runtime/research-assets/plant01.3dscen` | 76,602-byte text, `version 2`, map name and query rows. | `48eba4bb7e642c882878d0a430ffd70d3ef78c8209e9d530736ad95290c536b1` |
| `runtime/research-assets/3d_maze.tar.xz` | 406,560-byte archive with SDF box collision models and no task file. | `5159e9f38b301307f71eccbe2ce101fd434398e60fd78ddd338e891fbb66deb1` |
| `runtime/research-assets/iris-cad-model.zip` | 81,839,849-byte archive with FBX, binary PLY triangle mesh, and object-tree TXT. | `98b86a09711686fcab1e2d5fb900316bd3dce2c10605bd22756e45a31c991b4f` |

The file inspection does not establish reuse rights, complete model validity,
or successful simulator integration. Neither this inventory nor its correction
changes any frozen perception-encoder protocol.
