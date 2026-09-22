# Model-registry interfaces

This page records the concrete local interfaces through which models are published,
discovered, inspected, and loaded. Paths into the implementation are stated in full
on first use so the similarly named experiment registry is not confused with this
subsystem.

## Stored package layout

```text
<garden-root>/
└── <name>/
    ├── model.pt
    ├── encoder.pt
    ├── meta.json
    ├── loss_curve.json
    └── <tag>/                 # tagged publication uses this level instead
        ├── model.pt
        ├── encoder.pt
        ├── meta.json
        └── loss_curve.json
```

The default CLI root is `runtime/garden`. Package-bundled presets live under
`theseo_anysearch/garden/pretrained/<name>/<tag>`.

## Machine-local registries

| Interface | Default | Override | Meaning |
|---|---|---|---|
| Model registry | `~/.anysearch/garden_registry.yaml` | `ANYSEARCH_GARDEN_REGISTRY` | Maps model references to directories |
| Config registry | `~/.anysearch/garden_configs.yaml` | `ANYSEARCH_GARDEN_CONFIGS` | Maps short names to garden YAML files |
| Run registry | `<garden-root>/cache/runs.json` | Select a different garden root | Records extracted training-run sources |

These files are simple mappings written in place. They are neither schemas nor
portable manifests.

## Python API

[`theseo_anysearch/garden/store.py`](../../../../../../theseo_anysearch/garden/store.py)
provides:

- `GardenStore.save`, `load_encoder_state`, `meta`, `loss_curve`, `list_models`,
  `exists`, and `resolve_ref`;
- `register_config`, `resolve_config`, and `list_configs`; and
- `register_builtin_presets`, invoked as an import side effect by
  [`theseo_anysearch/garden/__init__.py`](../../../../../../theseo_anysearch/garden/__init__.py).

`resolve_ref` accepts `name`, `name:tag`, or an existing path. A drive-letter path is
recognized before colon-based tag parsing.

## CLI surface

[`theseo_anysearch/cli/commands/garden.py`](../../../../../../theseo_anysearch/cli/commands/garden.py)
defines the user-facing commands:

| Command | Registry interaction |
|---|---|
| `anysearch garden train CONFIG [--tag TAG]` | Trains, saves a package, and updates model aliases |
| `anysearch garden tune CONFIG` | Optionally retrains and publishes the selected trial |
| `anysearch garden list` | Lists packages under one store root; it does not enumerate every global alias |
| `anysearch garden inspect REF` | Resolves a reference and prints metadata and loss history |
| `anysearch garden add FILE.yaml` | Registers a reusable garden configuration, not an encoder package |
| `anysearch garden add RUN_REF` | Extracts observations and records a training-run source, not an encoder package |

The overloaded `add` command is therefore outside model publication for both of its
forms; its presence under `garden` should not be read as a package-install operation.

## Anysearch consumer

[`theseo_anysearch/rllib/models/cnn.py`](../../../../../../theseo_anysearch/rllib/models/cnn.py)
uses `custom_model_config.pretrained_encoder` as the reference and
`freeze_encoder` as a boolean defaulting to `true`. It reads `meta.json`, constructs
`VoxelEncoder3D`, loads `encoder.pt`, and concatenates its latent output with auxiliary
observation features before policy and value heads. This is a legacy `TorchModelV2`
integration, not an RLModule interface.
