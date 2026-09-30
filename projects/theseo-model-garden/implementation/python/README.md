# Python implementation

The Python implementation is currently split. The standalone `theseo_model_garden`
package at commit `756e5dd18251ae877ed3277a37f39e16f4b90764` contains the
`compact-spatial-code-v1` inference slice. The broader garden training, collection,
and legacy registry code remains in `theseo_anysearch/garden/` at experimental source
snapshot `88e220ccdbca8c87c56875b5d742427eb7947540`. The command-line adapter
remains `theseo_anysearch/cli/commands/garden.py`; AnySearch consumer integration
remains in `theseo_anysearch/rllib/models/cnn.py`. The responsibility map below
describes those remaining AnySearch-hosted paths, not files already extracted.

This page is contributor guidance for navigating and changing that implementation. It
does not define dataset, encoder, qualification, or registry behavior; those guarantees
belong to the contracts under `projects/theseo-model-garden/subsystems/`.

## Responsibility map

| Path | Contributor responsibility |
| --- | --- |
| `theseo_anysearch/garden/data_config.py` | Pydantic configuration models, discriminated source types, YAML loading, and custom Python component import. |
| `theseo_anysearch/garden/collect.py` | Source-specific observation collection, source identities, and observation-cache production. |
| `theseo_anysearch/garden/augment.py` | Online transformations of binary voxel grids and paired-grid augmentation. |
| `theseo_anysearch/garden/dataset.py` | PyTorch datasets, deterministic train/validation splitting, multi-radius datasets, and radius-aware batching. |
| `theseo_anysearch/garden/models/ae.py` | 3D, 2D, and triplanar encoders plus autoencoder and variational-autoencoder decoders and losses. |
| `theseo_anysearch/garden/models/mvm.py` | Masked-voxel-model encoder, masking, transformer decoder, and masked-cell loss. |
| `theseo_anysearch/garden/encoder.py` | Architecture factory and extraction of the deployable encoder from a pretraining model. |
| `theseo_anysearch/garden/trainer.py` | Device placement, data loading, optimization, validation, early stopping, and training results. |
| `theseo_anysearch/garden/tune_runner.py` | Ray Tune search-space translation and trial orchestration. |
| `theseo_anysearch/garden/store.py` | Local configuration registry, artifact publication, tags, metadata, checkpoint lookup, and loading. |
| `theseo_anysearch/garden/presets/` | Built-in radius-specific YAML presets registered during package import. |
| `theseo_anysearch/garden/pretrained/` | Repository-shipped encoder artifacts and their metadata. |
| `theseo_anysearch/cli/commands/garden.py` | User-facing CLI composition across collection, training, tuning, inspection, and registry operations. |
| `theseo_anysearch/rllib/models/cnn.py` | Consumer-side loading of a Garden encoder into an RLlib voxel model. |

Keep changes at the narrowest owner. For example, a new augmentation belongs in
`theseo_anysearch/garden/augment.py` with its schema in
`theseo_anysearch/garden/data_config.py`; it should not be implemented inside the CLI.
Likewise, policy-specific adaptation belongs in `theseo_anysearch/rllib/models/cnn.py`,
not in the artifact store.

## Dependency boundaries

The package uses NumPy for collected grids and augmentation, Pydantic and PyYAML for
configuration, and PyTorch for datasets, models, training, and checkpoints. Ray is
needed by the tuning path. Environment-backed collectors additionally depend on the
AnySearch environment and native extension used by the configured source.

Keep imports at their current boundary:

- `theseo_anysearch/garden/data_config.py` must remain usable for configuration
  validation without constructing a model or starting Ray.
- `theseo_anysearch/garden/tune_runner.py` defers runtime-heavy Garden imports until a
  trial actually executes. Preserve that separation when adding tuning behavior.
- Custom encoders and sources are imported only when their configured Python reference
  is instantiated. Import failures should identify the configured component rather
  than silently selecting a built-in implementation.
- The `torch-cpu` and `torch-gpu` dependency groups in `pyproject.toml` select a PyTorch
  installation; code must not assume that CUDA is present merely because PyTorch is.

Do not introduce reverse dependencies from reusable Garden modules into
`theseo_anysearch/cli/commands/garden.py` or RLlib. CLI and policy code compose the
Garden package; the Garden package does not depend on those consumers.

## Data and tensor conventions

Collected occupancy samples are binary NumPy arrays with shape `(N, N, N)` and are
converted to `float32` by `GardenDataset` in
`theseo_anysearch/garden/dataset.py`. Model batches generally have shape
`(batch, N, N, N)`; the 3D encoder adds a singleton channel, the 2D encoder treats the
z dimension as channels, and the triplanar encoder extracts the three center planes.

Preserve these conventions across collection, augmentation, model inputs, and the
RLlib consumer. A dimension permutation that trains successfully can still publish an
encoder with incorrect spatial semantics. Tests for new architectures should therefore
assert shapes and axis-sensitive behavior, not only a finite loss.

Multi-radius training requires batches whose samples share a spatial size. Keep that
constraint in `MultiRadiusDataset` and `RadiusBatchSampler` rather than padding samples
implicitly. Architecture changes must explicitly state whether their encoder is
size-agnostic and whether their decoder supports every configured radius.

## Identity, caches, and artifacts

Collection caches are written beneath the configured cache directory by
`theseo_anysearch/garden/collect.py`. Source hashes are part of cache correctness: any
new input that can change collected observations must participate in the identity.
Never reuse a cache entry merely because its file exists.

`GardenStore` in `theseo_anysearch/garden/store.py` owns published model directories,
tags, metadata, and `encoder.pt`. The deployable checkpoint is an encoder state dict,
not a self-describing executable model. Loading therefore requires the matching
architecture and configuration. Changes to parameter names, tensor shapes, radius
semantics, or architecture defaults are compatibility changes and need explicit
migration or versioning evidence.

Repository-shipped artifacts under `theseo_anysearch/garden/pretrained/` are not normal
source files. Do not regenerate, replace, or commit checkpoints as a side effect of a
test or local run. A publication change must include the qualification evidence and
identity required by the model-registry contract.

The local named-configuration registry defaults to
`~/.anysearch/garden_configs.yaml` and can be redirected with
`ANYSEARCH_GARDEN_CONFIGS`. Tests and automation must redirect this state to an
isolated temporary location rather than modify a contributor's registry.

## Errors and diagnostics

Raise configuration errors at the earliest layer that has enough context to explain
them. Pydantic validation should reject structurally invalid YAML; factories should
reject unsupported architecture/approach combinations; collectors should identify the
source that failed; and the store should identify the missing or incompatible
artifact. Do not convert these failures into a fallback architecture, empty dataset,
or untrained encoder.

Error messages should include stable configuration paths, source identities, or
artifact names where available, but must not embed transient object representations as
machine-readable contracts. CLI formatting belongs in
`theseo_anysearch/cli/commands/garden.py`; reusable modules should raise meaningful
Python exceptions rather than terminate the process.

## Performance hazards

- Voxel memory grows cubically with the observation side length. Avoid copying full
  datasets or materializing all augmented variants in memory.
- The masked-voxel decoder creates one query per voxel, so its attention and activation
  costs become significant at large radii. Measure memory as well as wall-clock time
  when changing `decoder_dim`, layers, heads, or supported radii.
- `VoxelEncoder2D` uses the voxel side length as its input-channel count; unlike the 3D
  adaptive-pooling path, one instance is not automatically compatible with arbitrary
  radii.
- Augmentation occurs in `GardenDataset.__getitem__`. Avoid global random state and
  expensive per-sample conversions that multiply across DataLoader workers.
- Collection and training caches may be shared by repeated experiments. Identity bugs
  can look like performance wins, while missing reuse can make Tune retrain or recollect
  identical inputs.
- Do not import or initialize Ray, CUDA, an environment, or a large checkpoint during
  package discovery when the work can be deferred to the command or trial that needs it.

Performance changes require measurements representative of the affected radii,
architecture, device, and batch size. A CPU unit-test runtime does not establish GPU
memory safety or Tune throughput.

## Testing

The focused test package is `tests/test_garden/test_unit/`. Current suites cover
augmentation, configuration, dataset behavior, and the store:

- `tests/test_garden/test_unit/test_garden_augment.py`
- `tests/test_garden/test_unit/test_garden_data_config.py`
- `tests/test_garden/test_unit/test_garden_dataset.py`
- `tests/test_garden/test_unit/test_garden_store.py`

Add tests beside the owning behavior. Model or trainer changes that are not covered by
those files require new focused tests under `tests/test_garden/test_unit/`; consumer
integration changes also require the relevant RLlib tests, especially
`tests/test_rllib/test_unit/test_cnn_models.py`. A tuning change should test search-space
translation without starting Ray where possible, then use a marked integration test
when real Ray behavior is the subject.

Use temporary directories for stores, caches, checkpoints, and configuration
registries. Tests must be offline and deterministic unless explicitly marked for an
external runtime. Assert artifact contents and identities in addition to path
existence. For stochastic augmentation or masking, inject or seed the owning random
generator and test invariants rather than relying on one accidental sample.

Before review, run the smallest owning suite first, followed by consumer or integration
suites affected by the change. Report skipped GPU, native-extension, or Ray validation
as a limitation; do not describe an unrun environment as passing.

## Contributor workflow

1. Identify the owning subsystem contract under
   `projects/theseo-model-garden/subsystems/` and confirm whether the requested change
   is behavioral, experimental, or implementation-only.
2. Trace the path from configuration through collection, datasets, model construction,
   training, publication, and consumption. Modify only the owners involved.
3. Decide whether cache identity or checkpoint compatibility changes before editing.
4. Add a focused regression test, then implement the smallest complete change.
5. Run `tests/test_garden/test_unit/`, plus CLI, RLlib, Ray, or GPU checks when those
   boundaries changed.
6. Update the owning subsystem documentation for observable behavior. Record research
   claims or training outcomes under `projects/theseo-model-garden/research/` or
   `projects/theseo-model-garden/experiments/`, not on this implementation page.

This is the fixed Python partition. It is not a template for creating additional
implementation folders.
