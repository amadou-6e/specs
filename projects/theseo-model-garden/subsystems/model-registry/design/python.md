# Python responsibility mapping

This page maps the registry's behavior to unambiguous Python modules and follows the
publication-to-consumption sequence. Model training internals are referenced only at
the boundary where they hand an artifact to the registry.

## Publication

- [`theseo_anysearch/garden/store.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/garden/store.py)
  owns `GardenStore`, the two YAML registries, built-in preset discovery, package
  writing, alias resolution, and the training-run index.
- [`theseo_anysearch/garden/encoder.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/garden/encoder.py)
  extracts the encoder submodule before publication. Its
  `load_encoder_from_store` helper returns a state dictionary despite its `nn.Module`
  annotation; the main RLlib consumer does not use this helper.
- [`theseo_anysearch/cli/commands/garden.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/cli/commands/garden.py)
  invokes publication after direct training or after retraining the best Tune
  configuration and presents list/inspect output.

## Discovery

- [`theseo_anysearch/garden/__init__.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/garden/__init__.py)
  calls `register_builtin_presets` during import. This means importing the package can
  write user-home state.
- `GardenStore.resolve_ref` interprets aliases and paths. It is independent from
  `theseo_anysearch.cli.registry`, which resolves experiment runs rather than encoder
  packages.

## Consumption

- [`theseo_anysearch/rllib/models/cnn.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/rllib/models/cnn.py)
  owns the current downstream adapter. `PretrainedVoxelModel` reads metadata,
  constructs `VoxelEncoder3D`, loads its state, and applies freezing.
- [`theseo_anysearch/garden/models/ae.py`](https://github.com/amadou-6e/theseo-anysearch/blob/49fef5f4f9d3fb21325931e1ce1eed89e743cdcc/theseo_anysearch/garden/models/ae.py)
  defines that concrete encoder architecture.

## Responsibility gaps

No module currently owns manifest schema migration, checkpoint/metadata integrity,
atomic publish, concurrent registry access, certification evaluation, or promotion
status. Those are open product responsibilities rather than implicit duties of the
files above.
