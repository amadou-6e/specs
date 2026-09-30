# Cached Gazebo maze provider

Implements specs#97 through theseo-anysearch#466 then #467. Stack the provider
PR on the isolated adapter PR; neither is merged without review. The owning
interface is `world-provider-cli.md`. No package-index publication is required.

## Installation and commands

`theseo-anysearch[gazebo]` selects the separate `theseo-anysearch-gazebo` wheel.
Installation never downloads geometry or executes Gazebo. Local builds/install
use a wheel directory, as with the Aerial Gym provider.

```powershell
anysearch worlds gazebo --seed 42 --meters-per-voxel 0.5 --output worlds/maze-42
anysearch worlds gazebo --seed 42 --meters-per-voxel 0.25 --offline true --output worlds/maze-42-fine
```

Generation downloads pinned sources automatically on first use. Repeated calls
verify and reuse original archives, regenerating from SDF at the requested
resolution, not resampling old occupancy. `ANYSEARCH_GAZEBO_CACHE` overrides
`~/.cache/anysearch/gazebo`. Offline misses and corruption fail explicitly.
`--layout roofed` is initially the only layout. Seed selects the first of the
accepted fixed derived queries by deterministic rotation; it does not alter
static maze geometry. All accepted queries remain available in sidecars.

## Source and safety

Pin engcang/gazebo_maps at `6ecf68cf659e122be58fc09c7a2af61b956c3301`:

- `3d_maze.tar.xz`: `5159e9f38b301307f71eccbe2ce101fd434398e60fd78ddd338e891fbb66deb1`.
- `common_models.tar.xz`: `03f46d349e46b55d4acba5c310d44205f1dab04ba8e107016dd4520551464a50`.
- Include the pinned BSD-3-Clause LICENSE with its verified hash after audit.

Reuse the bounded HTTPS source cache with an explicit per-manifest size limit
of 4 MiB per compressed file (existing providers retain 2 MiB defaults).
Archive validation is separate: at most 512 members, 32 MiB total uncompressed,
2 MiB per regular member; reject duplicate/noncanonical paths, traversal,
absolute paths, backslashes, links, special files and unsupported SDF dependencies.
Never extract or execute code. Read only allowlisted collision XML from the
verified archives; retain verified member hashes. Cache publication is atomic.

## Geometry and tasks

Preserve the separately identified original open-top crop. Derived roof bounds
are [-46,46] x [-46,46] x [0,9] meters, roof underside 8 m and thickness 1 m.
Gazebo source coordinates are Z-up; voxel storage is `(source x, source z,
source y)` because the native replayer renders storage axis 1 as vertical.
Thus the 0.5 m extent is `184 x 18 x 184`, not `184 x 184 x 18`.
GridFrame must record this permutation and all planar/altitude checks operate
on the mapped vertical axis. A viewer-only transform is insufficient.
Resolution must be between 0.25 and 0.5 m and divide all bounds; cap 5 million
voxels before allocation. Default sphere radius is 0.25 m, positive and below
0.5 m. Outside bounds is forbidden. Record conservative voxel-cube clearance
and replay against source primitives independently. Check roof anti-overflight,
connectivity, endpoint validity and source/voxel parity at each resolution.

Keep original converter v1 evidence unchanged. Provider conversions use a new
converter version and dataset identity. Generation exports a provider-compatible
roofed bundle, verification and six PNGs; rejected queries are reported, zero
accepted queries fail generation. Report planar-only unless the computed tasks
actually require altitude change. Routes are feasible witnesses, not optimal
trajectories or native simulator/controller results.

Source rights remain reviewed for evaluation only: no training attachment or
redistribution grant is inferred from the repository-level license. A future
expanded audit requires its own recorded revision. The bundle uses the test
partition. `worlds add` therefore rejects attaching it as training data under
the current interface; test this rejection rather than pretending a training
round trip succeeds. A later audited training-capable version can reuse normal
YAML attachment and split checks. Viewing remains the existing PNG workflow.

## Acceptance

Offline fixtures cover collision transforms/includes, archive attacks and limits,
first-use download, cache verification/offline reuse, resource validation,
resolution-specific regeneration, rejected queries, roof closure, PNG output,
extra/entry-point isolation and installed-wheel discovery. Run the real pinned
source conversion separately and commit only compact reports and hashes, not
archives, generated arrays, environments or wheels.
