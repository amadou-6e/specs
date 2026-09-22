# World-provider design

This page explains how installed provider code becomes an independently checked local bundle and, only on request, an experiment selection. The design separates provider execution from data admission: a provider can write files, but it cannot mark those files verified by itself. The implementation reference is `theseo-anysearch` revision `72a413a`; module paths below are relative to that repository root.

The processing sequence is:

```text
installed entry point -> validated parameters -> provider output directory
 -> shared routing sidecars + occupancy verification -> preview rendering
 -> verification.json -> local registry
 -> optional worlds add -> compiled runtime pack + task waypoints + YAML
 -> experiment-loader revalidation
```

`theseo_anysearch/world_providers/api.py` isolates optional plugin discovery. `theseo_anysearch/world_providers/service.py` orchestrates generation, report hashes, remote catalog reads, and the local registry. `theseo_anysearch/world_providers/bundle.py` validates provider output independently of the provider's own claims, using shared routing manifests and a swept-sphere voxel collision check. `theseo_anysearch/world_providers/render.py` derives six inspection images. `theseo_anysearch/world_providers/selection.py` bridges accepted bundles to training configuration and the compiled-world runtime; `theseo_anysearch/experiments/loader.py` repeats selection checks when loading a configured world. The [Python map](python.md) follows these responsibilities in execution order.

The bundle directory is the authoritative data source; `worlds.json` stores only discovery paths and identities. Source downloads, where used, are separately content-addressed and SHA-256 checked by `theseo_anysearch/world_providers/source_cache.py`. The bundle's `verification.json` includes hashes for the occupancy and required sidecars/routes, and preview hashes; opening it later recomputes those hashes. Generated outputs are not inserted into Git by this flow.

There are three distinct trust boundaries: installed provider code is executable and must be installed knowingly; downloaded source bytes are untrusted until hash-checked; generated geometry/routes are untrusted until the provider-neutral bundle verifier accepts them. The verifier proves voxel-route clearance under the recorded body radius, not the correctness of a physical controller or native benchmark labels (`theseo_anysearch/world_providers/api.py`, `theseo_anysearch/world_providers/source_cache.py`, `theseo_anysearch/world_providers/bundle.py`).

The design favors complete, independently checkable small-to-medium voxel bundles. It pays memory proportional to the full occupancy array and renders complete projections. The current service also writes directly to the final output path, so failed generation is not an atomic rollback. YAML replacement is separately staged and validated before replacement, but pack and waypoint artifacts may be created before that replacement (`theseo_anysearch/world_providers/service.py`, `theseo_anysearch/world_providers/selection.py`).
