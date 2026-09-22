# World-provider contract

This records observed behavior at implementation revision `72a413a`. The shared routing sidecar schemas are defined in `theseo_anysearch/environments/routing_manifests.py`; this page specifies how the provider service admits them.

## Generation and verification

1. Provider lookup loads a built-in fixture plus valid `theseo_anysearch.world_providers` entry points. A broken optional entry point is reported as unavailable without preventing other providers from listing or loading (`theseo_anysearch/world_providers/api.py`).
2. Before invocation, unknown parameters, missing required parameters, wrong value types, and out-of-range numeric values are rejected. An existing output path is refused. The provider receives the seed, output path, and resolved parameter map (`theseo_anysearch/world_providers/service.py::_parameters`, `generate_world`).
3. The provider writes `occupancy.npy` and routing sidecars. Admission requires a nonempty, one-to-one task/reference set; matching manifest identities; a complete binary `uint8` occupancy array with the declared extent and hash; valid task endpoints; and a reference route for every task. Each route must begin/end at its task endpoints, use six-axis unit steps, and pass swept-sphere collision checking against occupied voxel cubes and world bounds (`theseo_anysearch/world_providers/bundle.py::load_bundle`). This is **not** a proof of optimality or continuous-controller feasibility.
4. Rights must permit each split member's intended training/evaluation use. The output resolution must equal the provider declaration, and fixed native extent (when declared) must match. The service then renders six deterministic projection/slice PNGs and records hashes of required bundle files and previews in `verification.json` (`theseo_anysearch/world_providers/service.py::generate_world`, `theseo_anysearch/world_providers/render.py`).
5. Reopening through `load_verified_world` recomputes bundle and preview hashes and compares world and dataset identities. The local registry is a discovery index; it does not override this revalidation (`theseo_anysearch/world_providers/service.py`).

## Failure and resource boundaries

- A validation or rendering failure prevents creation of `verification.json` and registry admission, but the provider may already have written a partial output directory. There is no atomic whole-bundle publish (`theseo_anysearch/world_providers/service.py::generate_world`).
- The verifier loads full occupancy into memory; the provider path is therefore not a sparse large-world streaming verifier (`theseo_anysearch/world_providers/bundle.py::load_bundle`).
- `cached_sources` accepts only HTTPS manifests with nonempty SHA-256 hashes, rejects unsafe relative paths and non-HTTPS redirects, enforces a caller limit no greater than 32 MiB per file, validates existing cache content, and fails offline if a complete verified cache is absent (`theseo_anysearch/world_providers/source_cache.py`). This helper does not grant rights to use a source.
- The optional remote catalog is metadata only. It may be read from the packaged JSON, a local path, or an HTTPS URL; HTTPS reads are bounded to 1 MiB. It never installs or executes a provider (`theseo_anysearch/world_providers/service.py::remote_catalog`).

## Attachment

`worlds add` requires a previously verified bundle, a training/tuning YAML with `env` and `training`, a matching `train` split member, no conflicting geometry or waypoint source, and an unambiguous same-study split assignment. It compiles the occupancy into a runtime pack, writes task waypoints, validates the proposed temporary YAML with the experiment loader, and only then replaces the YAML. Repeating an identical selection is idempotent. On each later load the loader rechecks the bundle, pack identity, task waypoint content, rights, and same-study assignments (`theseo_anysearch/world_providers/selection.py`; `theseo_anysearch/experiments/loader.py`).

The model names `train`, `calibration`, and `test`, but the live `add` path rejects roles other than `train`. The term `calibration` remains in code despite the subsequent naming discussion; no rename is claimed here (`theseo_anysearch/world_providers/models.py`, `theseo_anysearch/world_providers/selection.py`).

## Open contract questions

- Should generation publish an entire bundle atomically and clean failed outputs? The older proposal says failure-closed publication; current code only withholds verified status and registry admission.
- Should task selection and non-training roles be first-class in `worlds add`? Current code picks the first sorted task identity and rejects non-train roles.
- How should the current single-world `worlds` YAML block evolve with the proposed task/geometry/main-YAML separation? This entry does not preempt that design.
