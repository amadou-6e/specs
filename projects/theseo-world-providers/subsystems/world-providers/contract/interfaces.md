# World-provider interfaces

At implementation revision `72a413a`, the user-facing command group is `anysearch worlds` (`theseo_anysearch/cli/commands/worlds.py`):

| Surface | Current behavior |
| --- | --- |
| `worlds list` | Prints installed provider metadata, broken-provider diagnostics, and registered local worlds rechecked as `verified` or `missing-or-changed`. No provider generation. |
| `worlds list --remote` | Reads a version-1 metadata catalog, packaged by default or from `ANYSEARCH_WORLDS_CATALOG`; it does not install providers. |
| `worlds <provider> --seed N --output DIR [declared options]` | Resolves one installed provider and generates/verifies a new output directory; prints JSON including world identity, task count, limitations, and preview paths. |
| `worlds add DIR --config experiment.yaml` | Validates and attaches a verified training world to one compatible existing YAML; prints a diff and JSON status; never starts a run. |

There are no separate `worlds verify` or `worlds preview` commands at this revision. Direct library entry points are `theseo_anysearch.world_providers.api` (`ProviderInfo`, `ProviderParameter`, `GenerationSummary`, `WorldProvider`), `theseo_anysearch.world_providers.service.generate_world/load_verified_world`, and `theseo_anysearch.world_providers.selection.add_to_experiment/validate_selection`. The provider returns routing sidecars plus `occupancy.npy`; the service writes `verification.json` and six `previews/{xy,xz,yz}-{projection,slice}.png` files (`theseo_anysearch/world_providers/api.py`, `theseo_anysearch/world_providers/bundle.py`, `theseo_anysearch/world_providers/service.py`, `theseo_anysearch/world_providers/render.py`).

The current experiment selection block is `worlds` with `role`, `study_id`, `study_root`, `root`, `world_identity_sha256`, `root_geometry_id`, `dataset_identity_sha256`, `split_identity_sha256`, and `task_identity_sha256`. `WorldSelectionConfig` forbids unknown fields and freezes parsed values (`theseo_anysearch/world_providers/models.py`). Selection requires `env.geometry.extent`, `env.geometry.compiled_world_path`, and `env.waypoints_file` to match the chosen bundle (`theseo_anysearch/world_providers/selection.py`). This is the **current** shape, not the proposed future configuration split.
