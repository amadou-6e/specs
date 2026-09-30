# Python package boundary for extraction

Status: target contract for [theseo-anysearch #502](https://github.com/amadou-6e/theseo-anysearch/issues/502) and [specs #135](https://github.com/amadou-6e/specs/issues/135). The first, non-closing package move is [AnySearch PR #505](https://github.com/amadou-6e/theseo-anysearch/pull/505). Pre-move observations are pinned to `theseo-anysearch` `origin/develop` commit `fd94554c9620096f94aaed95ffda6a1bbd4711ec`; statements about #505 are proposed until that PR merges.

## Ownership

The provider SDK owns the versioned provider protocol, metadata and parameter validation, discovery, provider-neutral bundle admission, previews, verification record, and bounded source acquisition. Optional provider distributions own source-specific conversion, dependencies, and rights evidence. The AnySearch host owns its CLI, experiment loading and configuration, runtime world compilation, and policy execution. `worlds add` is a host integration, not a provider SDK operation. A provider can be installed and generate/admit a world without Ray, RLlib, an AnySearch experiment, or the AnySearch CLI.

Move the shared routing sidecar schemas and the minimum collision/admission primitives needed for independent verification into a lightweight public contract package, or an equivalently small dependency of the SDK. This package must be importable without initializing `theseo_anysearch.environments`: that parent package currently imports the environment stack. Do not fix the import only by changing the final module name while leaving the heavy parent initializer in the import path. The host can use the same sidecar package when attaching an admitted bundle.

`theseo_anysearch/world_providers/selection.py` currently imports `theseo_anysearch.worlds.compiler` and `theseo_anysearch.experiments.loader`; `service.py` imports `theseo_anysearch.cli.registry`. These are host dependencies. Move selection and experiment-specific validation behind a host adapter. Give the SDK its own registry-path policy or accept an explicit registry path from the host; it must not import a private CLI helper. Check the full transitive import graph, including package `__init__.py` files, before declaring the SDK lightweight.

The Gazebo adapter currently imports an Aerial Gym exporter. Shared conversion behavior belongs in a small shared library with explicit ownership, or in Gazebo's adapter if genuinely specific; one optional provider must not require another optional provider merely to import or generate its own world. Test each provider wheel alone with the SDK.

## Provider and helper ownership

The four wheels remain independently selectable extensions. Their source-specific exporters should move beside the owning wheel; an installed provider must not rely on another optional provider's exporter. The locations in the second column are the pre-move locations at the pinned `develop` revision, not the final layout.

| Wheel | Current exporter | Target owner |
| --- | --- | --- |
| `providers/aerialgym` | `environments/aerial_gym_export.py` | Aerial Gym wheel: pinned URDF/source acquisition, conversion and its source-box witness. |
| `providers/cavedrone` | `environments/cave_drone_export.py` | Cave Drone wheel: pinned simulator-source bridge and source-specific route conversion. |
| `providers/gazebo` | `environments/gazebo_maze_export.py` | Gazebo wheel: pinned SDF acquisition, collision conversion and source-specific witness. |
| `providers/ifcbench` | `environments/ifc_bench_export.py` | IFC Bench wheel: IFC solids, rights and task conversion. |

The Euler roll/pitch/yaw rotation used by Aerial Gym and Gazebo is provider-neutral conversion math, not an Aerial Gym API. #505 places it in `theseo_anysearch/worlds/rotation.py`; when provider wheels become host-independent, move or expose this small helper from a neutral lightweight dependency. Cave Drone and IFC Bench both import `environments/voxel_route_replay.py`. Extract only the pure route/clearance primitives they actually share into a provider-neutral contract; episode replay, environment execution and runtime world compilation remain AnySearch-owned. Treat that split as unfinished in #505, not as evidence that the wheels already install alone.

The SDK needs `WorldExtent` and a stable world-contract fingerprint for sidecar identity. Compiled-world chunk and overview manifest classes describe AnySearch runtime storage and belong with the host. #505 temporarily moves the whole `world_manifest.py` into the SDK; narrow that surface before #502 closes, keeping old class imports compatible through host re-exports. Fingerprint compatibility must be tested with existing records.

## Compatibility during relocation

API version `1` uses the installed entry-point group `theseo_anysearch.world_providers` (`world_providers/api.py`). Keep that group discoverable through the migration. A package rename may change the entry-point **target** and distribution name, but changing the group without a compatibility reader would silently orphan installed third-party providers. If a new group is introduced later, discovery must read both for an announced transition, deduplicate by provider name, and reject conflicting definitions visibly. Preserve the public version-1 `ProviderInfo`, `ProviderParameter`, `GenerationSummary`, and `WorldProvider` behavior or define a versioned adapter and migration guide before breaking it.

Python import compatibility is separate from entry-point discovery. #505 keeps `theseo_anysearch.world_providers.*`, `theseo_anysearch.environments.routing_manifests`, `theseo_anysearch.environments.shape_collision`, and `theseo_anysearch.worlds.manifest` as aliases or host re-exports, with type identity preserved where the contract types moved. Keep these old paths for every `0.x` AnySearch release after the move, without import-time warnings that would flood plugin discovery and existing runs. Removal requires a separately reviewed major-version migration: inventory installed provider entry points and public imports, publish replacement paths and an upgrade guide, test old and new imports against the same artifacts, and announce a deprecation window before the removal release. Do not silently delete aliases just because first-party plugins have migrated. The current #505 code implements aliases, not that future removal process.

Bundle file formats and identity checks must remain compatible with verified worlds already produced by version 1. Any incompatible schema change needs an explicit format version, a reader or migration path, and fixtures proving old bundles can still be opened. Extraction must not make a previously verified world silently unverifiable because package import paths changed.

## Acceptance evidence

1. In a clean environment with only the SDK and one provider installed, import the SDK, discover that provider, generate a bundle, and independently admit it. Assert Ray, RLlib, the AnySearch CLI, experiment loader, and environment runtime are not imported or required.
2. Install each optional provider independently, including Gazebo without Aerial Gym, and run one real admitted-bundle test per provider.
3. Install a third-party-style fixture registered only under `theseo_anysearch.world_providers`; prove it is still discovered after relocation and bad/duplicate entry points report diagnostics.
4. Open an existing version-1 verified bundle, detect a tampered artifact, and attach a valid bundle through the AnySearch host adapter. Keep host integration tests separate from SDK-only tests.
5. Document the package/dependency graph and publish installation commands for SDK-only and host-plus-provider use. Compare installed dependency sets to catch accidental heavyweight imports.

See the [current implementation map](../../subsystems/world-providers/design/python.md) and [extension contract](../../subsystems/world-providers/contract/extensions.md) for the pre-extraction behavior.
