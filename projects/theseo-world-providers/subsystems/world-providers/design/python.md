# Python implementation map

The world-provider flow is coordinated in Python: it discovers trusted installed plugins, admits their generated files through a provider-neutral verifier, and optionally attaches an accepted bundle to an experiment. This map describes implementation revision `theseo-anysearch` `72a413a`. Every path below is relative to that repository root, not to this specification. Follow the [design overview](README.md) for ownership and trust boundaries and the [interfaces](../contract/interfaces.md) for user-facing commands.

## Entry point and acquisition

`theseo_anysearch/cli/commands/worlds.py` dispatches `list`, dynamic provider commands, and `add`. It reports unavailable plugin diagnostics rather than hiding the built-in provider. `theseo_anysearch/world_providers/api.py` owns the version-1 provider protocol, parameter declarations, metadata validation, entry-point discovery, and import errors. The built-in provider is in `theseo_anysearch/world_providers/fixtures.py`; optional distributions under `providers/` register through the same entry-point group.

Some optional providers acquire external source files. `theseo_anysearch/world_providers/source_cache.py` handles bounded, SHA-256-checked HTTPS retrieval and offline cache reuse. The provider distribution chooses its source and is responsible for source-specific conversion and rights evidence; the cache helper does not grant usage rights.

## Generate, verify, and register

`theseo_anysearch/world_providers/service.py` validates the requested parameters and nonexistent output path, calls the provider, coordinates independent admission, writes the verification report, and updates the local discovery registry. Admission is performed by `theseo_anysearch/world_providers/bundle.py`, which loads the full `occupancy.npy` array and checks manifest identities, endpoints, routes, bounds, and voxel collision clearance. The shared routing sidecar formats live in `theseo_anysearch/environments/routing_manifests.py`; swept collision geometry is implemented in `theseo_anysearch/environments/shape_collision.py`.

`theseo_anysearch/world_providers/render.py` creates the six headless projection/slice PNGs after bundle validation. The service hashes those previews and required bundle files into `verification.json`. A local registry record helps discovery, but reopening a world rechecks the bundle instead of trusting that record. Generation is not an atomic directory transaction: if a plugin or later validation fails, files written to the requested directory can remain.

## Attach and consume

`theseo_anysearch/world_providers/selection.py` validates a verified training bundle, chooses its current single task, creates the runtime pack and waypoint artifact, prepares a YAML change, and validates the proposed experiment before replacing the YAML. `theseo_anysearch/world_providers/models.py` defines the typed `worlds` selection fields and same-study assignment representation. `theseo_anysearch/experiments/loader.py` revalidates selected artifacts when the experiment is loaded; successful `worlds add` output is not a permanent waiver of verification.

The compiled-world pack is supplied by `theseo_anysearch/worlds/compiler.py`, which belongs to world storage rather than the provider plugin protocol. Native world access begins downstream of this Python attachment path. This provider map does not claim a Rust provider API.
