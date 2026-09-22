# Provider extension contract

An optional world provider is an installed Python distribution that generates a routing-world bundle for the provider-neutral admission service. This page states what an extension must supply and what Theseo checks before calling a world verified. It describes `theseo-anysearch` revision `72a413a`; the defining protocol and discovery code is `theseo_anysearch/world_providers/api.py` in that repository.

## Discovery and trust boundary

Register an entry point in `theseo_anysearch.world_providers`. Its name must equal `provider.info.name`, and `fixture-boxes` is reserved for the built-in provider. The entry point may load a provider instance or a class instantiated without arguments. Listing installed providers imports entry-point code: a remote catalog entry is only metadata and does not install, execute, or license a provider. An invalid optional plugin is omitted from usable providers but reported by `provider_errors()` and the CLI (`theseo_anysearch/world_providers/api.py`, `theseo_anysearch/cli/commands/worlds.py`). Install only code you trust.

## Metadata and parameter declaration

Supply `ProviderInfo` with API version `1`, a lower-case hyphenated name, version, description, positive finite native meters per voxel, and optionally a positive three-axis native extent. Declare provider-specific parameters with `ProviderParameter`: kinds are `integer`, `number`, `text`, and `boolean`, with applicable defaults, required flags, and numeric bounds. The common `seed` and `output` names are reserved. If the provider declares a `resolution_parameter`, it must name a numeric parameter; the generated resolution must equal that parameter's resolved value (`theseo_anysearch/world_providers/api.py`, `theseo_anysearch/world_providers/service.py`).

## Generation and output

Implement `generate(*, seed: int, output: Path, parameters: dict) -> GenerationSummary`. The provider writes a full `occupancy.npy` array and shared routing sidecars under the supplied output directory: source, conversion, world, and split manifests plus matching `task-*.json`, `reference-*.json`, and route artifacts. The exact formats are owned by `theseo_anysearch/environments/routing_manifests.py` and checked by `theseo_anysearch/world_providers/bundle.py`. `GenerationSummary` may report rejected task strata and limitations, but those claims do not replace verification.

The provider does **not** write or approve the final six previews or `verification.json`; the core service produces those after independent bundle validation (`theseo_anysearch/world_providers/service.py`, `theseo_anysearch/world_providers/render.py`). A provider-specific test should cover its conversion and at least one generated bundle admitted through the shared verifier, not only a mocked summary.

## Admission, failure, and isolation

The core verifier rejects missing or mismatched sidecars, non-binary or wrongly shaped occupancy, invalid identities/endpoints/routes, wrong resolution or fixed extent, insufficient rights for a split member's intended use, and routes failing voxel-bound or swept-clearance checks (`theseo_anysearch/world_providers/bundle.py`, `theseo_anysearch/world_providers/service.py`). This checks generated data independently of plugin assertions; it does not sandbox plugin execution or establish physical-controller feasibility.

An extension should treat the output directory as expendable until admission succeeds. The current service refuses an existing path but writes directly to the final one; provider or preview failure may leave partial files there. It withholds `verification.json` and registry admission on such a failure, but does not guarantee atomic cleanup. Reopening a registered world recomputes its integrity checks (`theseo_anysearch/world_providers/service.py`).

## Optional source acquisition and rights

Providers that download sources can use `theseo_anysearch/world_providers/source_cache.py` for bounded HTTPS retrieval with hash and offline-cache checks. The helper accepts no per-file limit above 32 MiB and does not determine whether a source may be used for training or evaluation. The provider must supply the applicable rights evidence and dependencies in its own distribution; core extras exist for the shipped optional providers (`providers/*/pyproject.toml`, repository `pyproject.toml`).

The [world-provider contract](README.md) specifies the common observable result; this page is limited to extension obligations and the boundary of independent admission.
