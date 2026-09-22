---
title: World providers
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-world-providers]
related:
  - ../../architecture/world-provider-cli.md
  - ifc-bench-mep-provider.md
---

# World providers

World providers turn an installed generator or converter into a locally verified voxel-world bundle. This subsystem owns provider discovery and invocation, parameter validation, bundle admission, previews, local discovery, and explicit attachment to an experiment. Occupancy storage, task semantics, and training itself are owned elsewhere.

This entry describes implementation revision `theseo-anysearch` `72a413a` (`origin/develop`, 2026-09-16), not the older checked-out repository root. The older [CLI proposal](../../architecture/world-provider-cli.md) is design evidence, not proof that every proposed command or guarantee exists. This entry remains **draft** because some proposal/implementation differences require product decisions.

## Consumers and supported scope

- `anysearch worlds` exposes installed providers, generation, and YAML attachment through `theseo_anysearch/cli/commands/worlds.py`.
- The experiment loader calls `world_providers.selection.validate_selection` when a `worlds` block is present (`theseo_anysearch/experiments/loader.py`).
- The built-in `fixture-boxes` provider and optional CaveDrone, Gazebo, Aerial Gym, and IFC-Bench distributions use the same entry-point boundary (`theseo_anysearch/world_providers/api.py`, `providers/*/pyproject.toml`).
- A generated bundle contains complete binary occupancy, routing sidecars, route artifacts, previews, and `verification.json`; it is not an implicit training run (`theseo_anysearch/world_providers/service.py`, `theseo_anysearch/world_providers/bundle.py`).

## Important limits

The provider service rejects an existing output path, but it does **not** stage the entire output and atomically rename it. A failure after provider writing can leave a partial directory; no verification report or registry entry is written if bundle validation or preview rendering fails. `worlds add` currently supports a `train` world in an existing training/tuning YAML and chooses the lexicographically first task identity; it does not expose per-task selection, multi-world study updates, or sweep attachment (`theseo_anysearch/world_providers/selection.py`). The runtime still uses a complete `uint8` occupancy array for provider verification (`theseo_anysearch/world_providers/bundle.py`).

## Reading map

- [Behavior and limits](contract/README.md)
- [Public interfaces](contract/interfaces.md)
- [Provider extension rules](contract/extensions.md)
- [Internal flow](design/README.md)
- [Python responsibilities](design/python.md)
- [Local workflow](guides/README.md)
- [Evidence and gaps](validation.md)
