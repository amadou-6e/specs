# Terrain And Geometry Generator Spec

## Goal

Add a generator pipeline for this repository that can produce:

1. random terrains
2. random obstacle geometries
3. approximations of real engineering spaces for routing tasks
4. optional imported geometries from external `.stl` or convertible CAD assets
5. routing tasks with explicit start/end anchors, and later connector or waypoint sets

This should support both:

- fast synthetic training data generation
- evaluation on more realistic imported shapes

## Current Repository Fit

This repository is already close to supporting this.

- Python config already supports `stl_path`, `geometry_boxes`, and `waypoints_file` in [`theseo_anysearch/models.py`](c:/Users/acisse/Documents/CodeWorkspace/theseo-anysearch/theseo_anysearch/models.py).
- Rust already ingests STL and voxelizes it in [`theseo_anysearch/core/src/world/ingest/stl.rs`](c:/Users/acisse/Documents/CodeWorkspace/theseo-anysearch/theseo_anysearch/core/src/world/ingest/stl.rs) and [`theseo_anysearch/core/src/world/ingest/voxelize.rs`](c:/Users/acisse/Documents/CodeWorkspace/theseo-anysearch/theseo_anysearch/core/src/world/ingest/voxelize.rs).
- The repo already ships simple hand-made test geometries in [`usage/geometries/README.md`](c:/Users/acisse/Documents/CodeWorkspace/theseo-anysearch/usage/geometries/README.md).

## Important Constraints In The Current Code

1. STL import is currently ASCII STL only.
   [`stl.rs`](c:/Users/acisse/Documents/CodeWorkspace/theseo-anysearch/theseo_anysearch/core/src/world/ingest/stl.rs) scans only `vertex ...` lines and does not parse binary STL.

2. The voxelizer converts meshes into occupied voxels and then solid-fills the interior.
   That is good for obstacles and surface navigation, but not enough by itself for internal free-space extraction in cabins, ducts, and harness channels.

3. Real routing tasks need anchors.
   The repo has `waypoints_file`, which is the right primitive to extend into:
   - start/goal pairs
   - connector sets
   - multi-pin bundles
   - clip or clamp sequences

4. Default grid sizes are small for detailed interiors.
   Fine cable-routing scenes will likely need either:
   - higher-resolution voxelization
   - local crops around the route corridor
   - multi-resolution representations

## Feasibility Summary

### Short answer

This is feasible.

The best path is not "blobs only". The practical solution is a hybrid:

- blobs / implicit fields for terrain and organic clutter
- CSG / primitives for engineering-style components
- imported STL or STEP-derived meshes for realism
- explicit anchor metadata for wiring tasks

### How far blobs can get you

Blob-style implicit surfaces are useful for:

- caves, berms, ramps, mounds
- cable slack obstacles
- soft partitions
- organic housings
- rough occupancy fields for clutter

They are not a good direct model for:

- brackets
- trays
- stamped panels
- connector housings
- seat rails
- aircraft ribs
- machine frames

RenderMan's blobby surface documentation describes these shapes as simple primitives that blend into rounded masses, which is consistent with their strengths and weaknesses: <https://renderman.jp/appnote.31.html>.

### How close we can get to real engineering spaces

#### Engineering components

High feasibility.

Use CSG and parametric feature generators:

- boxes
- cylinders
- filleted channels
- cut pockets
- bosses
- through holes
- slots
- ribs
- trays
- clamps

This can get reasonably close to mechanical parts, fixture plates, brackets, covers, housings, junction blocks, and routing trays.

The best evidence is that synthetic machining-feature STL corpora already exist. FeatureNet publishes 24 classes with 1000 randomly generated STL models per class: <https://github.com/madlabub/Machining-feature-dataset>.

#### Car interiors for cabling

Medium feasibility with procedural generation alone.

You can approximate:

- cabin voids
- dashboard bulkheads
- center tunnels
- seat pedestals
- HVAC ducts
- cable trays
- connector zones

You will not get convincing OEM-like geometry from blobs alone. For that, you need imported CAD or meshes plus anchor annotations.

#### Plane interiors

Medium feasibility for coarse cabin and equipment-bay layouts.

You can model:

- fuselage-like curved shells
- overhead bins
- floor beams
- cable raceways
- equipment racks
- sidewall cutouts

But realistic aircraft interiors are usually assembly-heavy and clearance-driven. Procedural generation can make good training proxies, but evaluation should use imported assets.

#### Construction machines

Medium-to-high feasibility.

These spaces are usually a good fit for a hybrid generator:

- articulated frames and boxes
- engine bays
- hydraulic line corridors
- guard structures
- access panels
- cable bundles around rigid mechanical assemblies

Compared with passenger-car interiors, these spaces are often more boxy and easier to approximate with primitives and imported subassemblies.

## Recommended Geometry Strategy

### Tier 1: Procedural Terrain Generator

Use this for fast RL curriculum generation.

Representation:

- height fields
- signed distance fields
- metaball/blob fields
- optional marching-cubes export to STL

Outputs:

- rolling terrain
- steps
- ramps
- trenches
- overhang-like clutter
- caves or tunnels if using full 3-D fields

Recommendation:

- use blobs only for terrain and amorphous clutter
- do not use blobs as the main representation for engineering assemblies

### Tier 2: Procedural Engineering Geometry Generator

Use this for synthetic but structured routing scenes.

Representation:

- primitive library
- CSG composition
- rule-based placement
- optional skeleton-to-mesh extrusion for trays and channels

Core primitives:

- box
- cylinder
- capsule
- bent duct
- tray
- bracket
- rib
- flange
- clip
- connector block
- perforated panel

Scene templates:

- equipment bay
- dashboard cavity
- seat base routing area
- avionics rack bay
- chassis side rail
- pipe cluster
- machine boom base

### Tier 3: Imported Real Geometry

Use this for realism and external validation.

Recommended sources:

- ABC Dataset: 1 million CAD models, with STL and STEP-related formats available. It also exposes FeatureScript metadata, which is useful if later you want to learn procedural generators from CAD programs rather than only final meshes: <https://deep-geometry.github.io/abc-dataset/>
- FeatureNet machining-feature STL corpus: good for procedural feature priors and part-level obstacle libraries: <https://github.com/madlabub/Machining-feature-dataset>
- FS-AI ADS-DV CAD: official open vehicle CAD subset for sensor and compute installation tasks, with STEP/Fusion files and connector-related geometry context: <https://github.com/FS-AI/FS-AI_ADS-DV_CAD>
- Public CAD libraries such as GrabCAD can provide practical STL or STEP examples, but license checks must be explicit on each asset.

## Wiring Task Data: What Exists And What Is Missing

### What I found

There are useful public examples, but open datasets that give all of the following together are rare:

- full geometry mesh
- explicit routing start/end anchors
- connector semantics
- ground-truth cable paths

The best public references I found are:

1. Berkeley cable routing dataset
   It provides 1442 expert routing demonstrations where trajectories start with the cable in the gripper and end when routed through a clip, but it is demonstration data rather than a clean STL-plus-endpoints benchmark:
   <https://sites.google.com/view/cablerouting/data>

2. SOLIDWORKS Electrical 3D harness exercise
   It includes an example harness-routing project with five connectors linked by a harness, and a pre-existing route path in the assembly:
   <https://swelectrical-help.solidworks.com/dl/swe/CHM/2022/EN/HelpOnLine/EW4SW_EX07.htm>

3. FS-AI ADS-DV CAD
   It gives real vehicle geometry context plus connector location information and connector types for additional sensor/electrical integration. That is useful as a near-real benchmark seed even if the cable route itself is not labeled:
   <https://github.com/FS-AI/FS-AI_ADS-DV_CAD>

4. GrabCAD harness-routing examples
   These are practical examples of connector import, harness assembly, and rerouting workflows, but they are tutorial/community assets and need per-model license review:
   <https://grabcad.com/tutorials/car-wire-harness-connector-terminal-assembly-by-creo-parametric-3d-routing-and-design>

### What this means for this repo

You should expect to create your own benchmark format for routing tasks:

- `geometry.stl`
- `anchors.json`
- `task.json`
- optional `route_reference.json`

Suggested anchor schema:

```json
{
  "anchors": [
    {"id": "src_power", "kind": "connector", "point": [12, 8, 4], "normal": [1, 0, 0]},
    {"id": "dst_ecu", "kind": "connector", "point": [54, 22, 11], "normal": [-1, 0, 0]}
  ]
}
```

Suggested task schema:

```json
{
  "tasks": [
    {
      "id": "power_route_a",
      "start_anchor": "src_power",
      "end_anchor": "dst_ecu",
      "bundle_radius": 2,
      "clearance": 1,
      "must_visit": ["clip_1", "clip_2"]
    }
  ]
}
```

## Recommendation For Actual Implementation

### Phase 1

Build an internal synthetic generator first.

Deliverables:

- terrain generator
- engineering-scene generator
- STL exporter
- anchor generator
- deterministic seeds

Why:

- fast to iterate
- no licensing friction
- ideal for curriculum learning

### Phase 2

Add robust external geometry ingestion.

Deliverables:

- binary STL support
- optional STEP-to-STL conversion outside the repo runtime
- mesh normalization
- scale normalization
- watertightness checks
- anchor annotation tools

This phase matters because many useful corpora, including ABC, provide binary STL or STEP-like assets, while this repo currently expects ASCII STL.

### Phase 3

Create a benchmark pack for wiring and routing.

Target packs:

- synthetic tray-and-connector scenes
- synthetic cabin routing scenes
- imported vehicle/equipment scenes with hand-authored anchors
- clip sequence tasks

## Best Technical Direction

### Recommended

Use a hybrid generator:

- SDF/blob terrain for terrain and clutter
- CSG/parametric primitives for engineering components
- imported meshes for realism
- explicit anchor metadata for routing

### Not recommended

Do not try to cover all target spaces with blobs alone.

That will produce:

- poor flat surfaces
- weak edge semantics
- bad connector realism
- unrealistic interior packaging

## Concrete Next Step For This Repository

The most valuable next implementation step is:

1. define a `generated_scene` artifact format
2. generate synthetic engineering scenes plus anchors
3. export them as STL + JSON
4. teach the existing env loader to accept anchor/task metadata
5. add binary STL support

## Proposed Spec Additions Later

Follow-up specs would be useful for:

- binary STL support
- scene generator API
- anchor/task JSON schema
- benchmark pack layout
- STEP ingestion pipeline

## Source Notes

External references used for this assessment:

- ABC Dataset: <https://deep-geometry.github.io/abc-dataset/>
- FeatureNet STL dataset: <https://github.com/madlabub/Machining-feature-dataset>
- FS-AI ADS-DV CAD: <https://github.com/FS-AI/FS-AI_ADS-DV_CAD>
- Berkeley cable routing data: <https://sites.google.com/view/cablerouting/data>
- SOLIDWORKS Electrical harness exercise: <https://swelectrical-help.solidworks.com/dl/swe/CHM/2022/EN/HelpOnLine/EW4SW_EX07.htm>
- GrabCAD Creo harness example: <https://grabcad.com/tutorials/car-wire-harness-connector-terminal-assembly-by-creo-parametric-3d-routing-and-design>
- RenderMan blobby implicit surfaces note: <https://renderman.jp/appnote.31.html>
