# Cached IFC-Bench MEP routing provider

Implements specs#99 through theseo-anysearch#489 then #490. Stack the
provider PR on the isolated adapter PR; neither is merged without review.
The owning interface is `world-provider-cli.md`. No package-index
publication is required.

## Installation and commands

`theseo-anysearch[ifcbench]` selects the separate `theseo-anysearch-ifcbench`
wheel. Installation never downloads geometry or parses IFC files. Local
builds/install use a wheel directory, as with the Gazebo and Aerial Gym
providers.

```powershell
anysearch worlds ifcbench --seed 0 --discipline plumbing --output worlds/wrh-plumb-0
anysearch worlds ifcbench --seed 0 --discipline electrical --output worlds/wrh-elec-0
```

Generation downloads the pinned West Riverside Hospital IFC files
automatically on first use. Repeated calls verify and reuse the original
files, re-extracting geometry at the requested resolution rather than
resampling old occupancy. `ANYSEARCH_IFCBENCH_CACHE` overrides
`~/.cache/anysearch/ifcbench`. Offline misses and corruption fail explicitly.
`--source west-riverside-hospital` is initially the only accepted value;
other IFC-Bench projects are out of scope until reviewed and added by a
separate spec update. `--discipline` selects `plumbing` (from
`plumb_ifc4.ifc`) or `electrical` (from `elec_ifc4.ifc`); there is no
combined-discipline output in the initial provider.

## Source and safety

Pin `sylvainHellin/ifc-bench` at tagged release `v2.0.1`, commit
`e1c4b0025ac42acf50f792e46a0ab33f4382e90e`, not the floating `main` branch:

- `projects/west_riverside_hospital/plumb_ifc4.ifc`:
  `bb53f0eb8f7295e91e0fb6ec6b79a30022a2e0e248714aab6bb1a8930c4793dd`.
- `projects/west_riverside_hospital/elec_ifc4.ifc`:
  `8e404c4e4c9085338383a89ae57a3a31ebe96ee406214392a1bf69a6775dcecc`.
- `projects/west_riverside_hospital/license.txt`:
  `2d7d4e28831e12cc6ae47ec03560d602e139f1f73617bb2ed3dfe1782e8c97f4`.

The model's own `license.txt` states CC BY 3.0 Unported, not the Hugging Face
dataset card's repository-level CC BY 4.0 tag; the card's tag covers the
question-answering benchmark wrapper and does not itself relicense each
donated project. `license.txt` attributes the model to Solihin, W., *West
Riverside Hospital IFC Models*, OpenIFC Model Repository, University of
Auckland, and records a use confirmation from Professor Robert Amor. CC BY 3.0
permits share and adapt, including commercial use, with attribution; this is
a project-level grant, not a confirmed per-entity clearance of every embedded
manufacturer catalog object or annotation inside the IFC files, so treat the
audit as project-level and preserve the attribution text verbatim in
generated bundles and rights evidence.

Reuse the bounded HTTPS source cache with an explicit per-manifest size limit
of 32 MiB per file; both pinned files exceed the existing 2/4 MiB provider
defaults. IFC files are ASCII STEP text, not archives: skip archive-member
validation and instead bound the parse to a fixed maximum entity count and
reject any file whose declared `FILE_SCHEMA` is not `IFC2X3` or `IFC4`.
IfcOpenShell performs the parse against the verified, hash-checked file only;
never execute embedded scripts, macros, or referenced external references.
Cache publication is atomic.

## Geometry and tasks

IFC files carry a project-level unit declaration (`IFCSIUNIT` or
`IFCCONVERSIONBASEDUNIT`) and an `IfcSite`/`IfcBuilding`/`IfcBuildingStorey`
placement hierarchy; do not assume meters or a fixed origin without reading
these entities. Confirm the West Riverside Hospital model's declared length
unit and record it in the conversion report alongside the resolved
`source_origin_m`.

Open question, to resolve during the adapter issue before any `GridFrame` is
fixed: IFC's schema declares a Z-up world coordinate system, but this must be
independently confirmed against the model's own geometry (bounding-box aspect
ratio, storey elevations) rather than assumed from the schema default, given
the Gazebo Z-up/Y-up defect (theseo-anysearch#477, fixed by #478) that shipped
from relying on `GridFrame`'s identity default instead of recording the
actual source-to-storage permutation. `storage_axes_in_source` must be set
explicitly, and an axis-mapping regression test analogous to
`test_gazebo_z_up_maps_to_renderer_y_up` is required before merge, not assumed
safe by analogy to Gazebo's fix.

Extract `IFCPIPESEGMENT`/`IFCPIPEFITTING` (plumbing) or
`IFCCABLECARRIERSEGMENT`/`IFCCABLECARRIERFITTING` (electrical) solids plus
their `IFCDISTRIBUTIONPORT` connectivity graph; fall back to
`IFCFLOWSEGMENT`/`IFCFLOWFITTING` only where the specific type is absent, and
record the fallback rate per file in the conversion report. Task family is
`single_pipe` for one endpoint-to-endpoint plumbing run and `coupled_pipes`
for a routed electrical circuit; cable/conduit routing reuses the pipe task
families rather than introducing a new one, since both are a
route-through-a-connected-network problem over the same manifest schema. Flag
this reuse for review rather than treating it as settled by this document.
Resolution is fixed by the source geometry's smallest routable cross-section,
not user-selectable, unlike the procedural Gazebo/Aerial Gym providers; record
the resolved `meters_per_voxel` and cap voxel count before allocation the same
way. Reverify every accepted task against both the extracted solids and the
occupied voxel cubes; a route feasible in the voxel grid is not thereby proof
the physical pipe/cable run is unobstructed by non-MEP building elements the
adapter did not extract (structure, architecture, fire, sprinkler, mechanical
systems present as sibling IFC files but not consumed by this provider).
Record this as an explicit limitation, not a verified guarantee, in every
generation report.

## Acceptance

Offline fixtures cover unit/placement extraction, the confirmed axis mapping
and its regression test, pipe/cable entity extraction including the
generic-flow-entity fallback path, connectivity-graph task derivation for
both disciplines, rejected/infeasible task reporting, first-use download,
cache verification/offline reuse, and installed-wheel discovery, using a
small excerpted IFC fixture rather than the full multi-hundred-megabyte
pinned files, so CI has no network or multi-minute parse dependency. Run the
real pinned West Riverside Hospital conversion separately and commit only
compact reports and hashes, not the source IFC files, generated arrays, or
wheels.
