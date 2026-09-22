---
title: Model Garden monolithic design record
status: superseded
kind: architecture
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../subsystems/README.md
  - ../subsystems/dataset-pipeline/README.md
  - ../subsystems/encoder-models/README.md
  - ../subsystems/pretraining-and-qualification/README.md
  - ../subsystems/model-registry/README.md
  - ../experiments/README.md
  - ../research/README.md
---

# Model Garden — Pre-trained Voxel Encoders

> **Historical architecture evidence.** This document preserves the original
> monolithic Model Garden proposal and its implementation plan. It is superseded as a
> current architecture specification by the [project architecture map](README.md) and
> the contracts and designs of the owning [subsystems](../subsystems/README.md).
> Statements below describe the proposal at the time it was written; they are not
> evidence that a feature is implemented, supported, or still planned.

## Record scope and provenance

This record is retained because it captures the initial end-to-end design connecting
data collection, augmentation, encoder pretraining, artifact storage, CLI workflows,
and Anysearch policy integration. Those concerns now have separate owners:

- [Dataset pipeline](../subsystems/dataset-pipeline/README.md) owns collection,
  caching, splitting, and augmentation contracts.
- [Encoder models](../subsystems/encoder-models/README.md) owns built-in and custom
  encoder construction and tensor compatibility.
- [Pretraining and qualification](../subsystems/pretraining-and-qualification/README.md)
  owns training, tuning, evaluation, and qualification evidence.
- [Model registry](../subsystems/model-registry/README.md) owns artifact packaging,
  certification, discovery, and resolution.
- [Experiments](../experiments/README.md) and [research](../research/README.md) own
  empirical outcomes and discovery evidence rather than runtime guarantees.

The preserved body is intentionally not normalized to the focused architecture
template: rewriting it would erase the distinction between the original proposal and
the current, evidence-backed architecture. Follow its links to canonical owners before
using any schema, command, path, performance estimate, or implementation sequence.

Pre-train spatial encoders on voxel observations independently of RL, then
plug them into any policy as a frozen or fine-tunable backbone. The model
garden is a versioned local store of encoder checkpoints at
`runtime/garden/`.

Architecture selection and scaling for 3D voxel inputs are investigated in
[Scalable 3D Voxel Perception Encoders](../research/perception-encoders.md). That document is
discovery evidence; its proposed pyramid encoder is not part of this specification
until its acceptance gates have been met and reviewed.

The pre-policy experiment sequence and minimum checkpoint certification metrics are
defined in [Standalone Voxel Encoder Pretraining](../subsystems/model-registry/contract/certification.md).
Those gates freeze the encoder and do not use RLlib or downstream navigation results.

---

## Motivation

The 3D CNN and 2D CNN policy models (see `cnn-models.md`) learn perception
and control jointly from sparse RL rewards. This is slow and unstable: the
encoder must simultaneously learn what the geometry looks like and what to do
about it. Pre-training separates these concerns:

1. **Pre-train** the encoder on a large collection of random voxel
   observations using a self-supervised objective (AE or MAE). No rewards
   needed — just rollouts from the Rust env.
2. **Store** the encoder checkpoint in the model garden.
3. **Load** the checkpoint into the RL policy, freeze most weights, and only
   train the policy/value heads and optionally a thin top-layer projection.

Result: the encoder already understands geometry before RL starts. The policy
head learns control from a meaningful feature space rather than random noise.

---

## Data Ingestion

Pre-training data is a large corpus of `(N, N, N)` binary voxel grids
representing the agent's local neighbourhood at many different positions across
one or more geometries. This section defines how that corpus is collected,
cached, and split.

---

### Collection Strategies

Three collection types are supported, listed from most to least efficient:

#### `position_sample` (recommended)

Sample agent positions directly from the free-space cells of a voxelized
geometry without running full episodes. For each sampled position, call the
Rust env's batch observation method to extract the `local_grid`.

- **Why preferred**: no wasted episode steps; uniform spatial coverage; 10–50×
  more samples per second than random rollout.
- **Requires**: a Rust-side `sample_box_obs(positions, radius)` method (see
  Rust Extension below) and at least one geometry source.

```
geometry → voxelize → list all free-space cells
→ sample N positions uniformly → batch_box_obs → (N, n, n, n) array
```

#### `training_run`

Load `local_grid` observations from the trajectory recordings of a completed
RL training run. No env interaction needed — the observations are extracted
directly from the saved trajectory JSON files.

- **Use when**: you have existing training runs and want to bootstrap
  pre-training from policy-conditioned observations without re-running the env.
- **Limitation**: trajectory data reflects the trained agent's state
  distribution, which may be spatially narrow. Mix with `position_sample`
  sources for better coverage.
- **Registered via** `anysearch garden add <run_ref>` — see CLI Commands.

---

### Geometry Sources

Each `position_sample` or `rollout` source specifies where the geometry comes
from. Two options:

#### Fixed env config (`geometry.env`)

Mirrors the standard `env:` block used in training YAMLs. Supports `stl_path`,
`geometry_boxes`, `scale`, `grid_size`. Single geometry.

#### Geometry sampler (`geometry.sampler`)

Procedurally generates multiple geometries. Two sampler types:

**`random_boxes`** — random axis-aligned box obstacles placed inside the grid.
Ties into the future terrain-geometry-generator (see
`spec/terrain-geometry-generator.md`).

```yaml
geometry:
  sampler:
    type: random_boxes
    seed: 42
    num_geometries: 50          # how many distinct geometries to generate
    num_boxes: [1, 5]           # range: min and max boxes per geometry
    box_min_size: [3, 3, 3]     # minimum box side length per axis (cells)
    box_max_size: [12, 12, 12]  # maximum box side length per axis (cells)
    grid_size: 32
```

**`stl_list`** — cycle through a collection of STL files. For each geometry,
apply `rotations_per_geometry` independent random SO(3) rotations before
voxelizing. Each rotation produces a distinct voxel world from which positions
are sampled. This is the primary source of rotational diversity — no post-hoc
grid rotation augmentation is used.

The source can point to an explicit file list or a directory (all `.stl` files
discovered recursively). See the Geometry Dataset Format section below.

```yaml
geometry:
  sampler:
    type: stl_list
    dir: data/geometries/obstacles/   # discover all .stl files via index.yaml
    scale: 40.0                       # default scale; overridden by index.yaml
    total_samples: 60000              # distributed across all files and rotations
    seed: 42                          # null = non-deterministic
```

Or with explicit paths:

```yaml
geometry:
  sampler:
    type: stl_list
    paths:
      - usage/geometries/stepped_terrain.stl
      - usage/geometries/pipe_junction.stl
    scale: 40.0
    total_samples: 60000
    seed: 42
```

**`total_samples`**: the sampler allocates the budget evenly across STL files
(`per_file = total_samples // len(files)`). For each file it draws random SO(3)
rotations one at a time, samples positions from each rotated world, and stops
when the per-file quota is filled. No need to tune `rotations_per_geometry` and
`samples_per_rotation` separately.

**SO(3) sampling**: uniform on the rotation group via quaternion sampling
(`scipy.spatial.transform.Rotation.random(rng)`). Applied in-memory to STL
vertex coordinates before voxelization; source files on disk are never modified.

**Geometry world caching**: each (STL file, rotation) pair is voxelized once
and saved to `runtime/garden/cache/worlds/<stl_hash>_<rotation_idx>.npz`
before positions are sampled. On re-runs the cached world is loaded rather
than re-voxelizing, making subsequent data collection fast even for large STLs.

**Collection loop:**
```
per_file = total_samples // len(stl_files)
for stl_file in stl_files:
    collected = 0
    rotation_idx = 0
    while collected < per_file:
        R = Rotation.random(rng)
        world = load_or_voxelize(stl_file, R, cache_dir)   # cached on disk
        free = world.free_cells()
        k = min(len(free), per_file - collected)
        positions = rng.choice(free, k, replace=False)
        grids += sampler.sample_box_obs(positions, radius)
        collected += k
        rotation_idx += 1
```

---

### Geometry Dataset Format

A geometry dataset is a folder of `.stl` files with an optional `index.yaml`
for per-file metadata. The `stl_list` sampler with `dir:` discovers all `.stl`
files in the folder (non-recursive by default; set `recursive: true` to walk
subdirectories).

**Folder layout:**

```
data/geometries/obstacles/
  index.yaml                  # optional — per-file metadata and defaults
  stepped_terrain.stl
  pipe_junction.stl
  cube.stl
  bracket_a.stl
  bracket_b.stl
```

**`index.yaml` schema:**

```yaml
# Defaults applied to all files unless overridden per entry.
defaults:
  scale: 40.0
  grid_size: 32
  exclude: false

geometries:
  - path: stepped_terrain.stl
    tags: [terrain, stepped]

  - path: pipe_junction.stl
    scale: 35.0              # overrides default scale for this file
    tags: [pipe, junction]

  - path: draft_geometry.stl
    exclude: true            # skip this file without deleting it
```

If no `index.yaml` is present, all `.stl` files in the folder are included
with the `scale` from the sampler config. Files named `_*.stl` (underscore
prefix) are automatically excluded as drafts.

**Recommended dataset layout for the project:**

```
data/
  geometries/
    obstacles/               # simple box/primitive obstacles for bootstrapping
      index.yaml
      cube.stl
      stepped_terrain.stl
      pipe_junction.stl
    engineering/             # CSG-generated engineering scenes (future)
      index.yaml
      bracket_a.stl
      bracket_b.stl
      duct_bend.stl
    imported/                # externally sourced geometry (ABC dataset, etc.)
      index.yaml
      abc_00001.stl
      abc_00002.stl
```

The `data/geometries/` folder is separate from `usage/geometries/` (which
holds manually crafted reference scenes for experiments and demos). Pre-
training datasets can be large (hundreds of files); keeping them under `data/`
keeps the repo clean.

---

### Caching

Two cache layers, both under `runtime/garden/cache/`:

#### World cache (`worlds/`)

Each (STL file, SO(3) rotation) pair is voxelized once and written to
`worlds/<stl_sha256>_<rotation_idx>.npz`. On subsequent runs the saved voxel
world is loaded directly — no STL parsing or voxelization happens again. This
is the most expensive step for large geometries.

```
runtime/garden/cache/
  worlds/
    a3f2c1_0.npz     # stepped_terrain.stl, rotation 0
    a3f2c1_1.npz     # stepped_terrain.stl, rotation 1
    b7e4d2_0.npz     # pipe_junction.stl, rotation 0
    ...
```

#### Observation cache (`obs/`)

The full collected observation array for a source is saved as
`obs/<source_hash>.npz`. **Cache key**: SHA-256 of the serialised source
config dict — any change to `geometry`, `total_samples`, `seed`, or
`obs_key` invalidates only that source's cache.

```
runtime/garden/cache/
  obs/
    c9a1f3.npz       # observations + metadata.json for one source
    d4b2e7.npz
```

**Storage per observation cache entry:**
```
observations: float32 array (M, n, n, n)
metadata.json: source config, collection timestamp, world hashes used
```

Sources are concatenated after loading; the combined dataset is shuffled
with `split.seed` before train/val split.

**`force_refresh`**: set `true` to delete and re-collect both observation
and world caches for all sources in the config.

---

### Full `data:` YAML Reference

```yaml
data:
  sources:

    # --- most efficient: direct position sampling ---
    - type: position_sample
      geometry:
        env:
          stl_path: usage/geometries/stepped_terrain.stl
          scale: 40.0
          grid_size: 32
      num_samples: 100000         # number of agent positions to sample

    # --- procedural geometry variety ---
    - type: position_sample
      geometry:
        sampler:
          type: random_boxes
          seed: 42
          num_geometries: 50
          num_boxes: [1, 5]
          box_min_size: [3, 3, 3]
          box_max_size: [12, 12, 12]
          grid_size: 32
      num_samples: 100000

    # --- STL dataset: SO(3)-rotated geometry for rotational diversity ---
    - type: position_sample
      geometry:
        sampler:
          type: stl_list
          dir: data/geometries/obstacles/   # discovers all .stl via index.yaml
          scale: 40.0
          total_samples: 60000              # budget distributed across files
          seed: 42

    # --- policy-conditioned data from a completed training run ---
    - type: training_run
      run: multi_agent_ppo_asha:v3          # registered via garden add
      obs_key: local_grid

  cache:
    path: runtime/garden/cache    # each source cached as <hash>.npz
    force_refresh: false          # set true to re-collect ignoring cache

  split:
    val_fraction: 0.1
    seed: 42
```

---

### Rust Extension: Batch Position Sampling

`position_sample` collection requires a new Rust PyO3 method on
`PyMultiVoxelEnv` (or a lightweight `PyVoxelSampler` helper that doesn't
model episodes):

```rust
/// For each (x, y, z) position in `positions`, return the local_grid box
/// observation as a flat Vec<f32> of length (2*radius+1)^3.
/// Positions outside the grid or inside filled geometry are skipped.
pub fn sample_box_obs(
    &self,
    positions: Vec<[u16; 3]>,
    radius: u32,
) -> Vec<Vec<f32>>
```

Python usage:
```python
sampler = PyVoxelSampler(grid_size=32, radius=2)
sampler.load_stl("path/to/geometry.stl", scale=40.0)
free_cells = sampler.free_cells()                          # list of (x,y,z)
positions = random.sample(free_cells, k=num_samples)
grids = sampler.sample_box_obs(positions, radius=2)        # List[List[float]]
```

This avoids the overhead of episode stepping (reset, action, reward) entirely.
A `PyVoxelSampler` is a stripped-down Rust struct that holds only the voxel
world and the box-obs extraction logic — no cursor state, no reward, no agents.

---

## Augmentation Pipeline

Augmentations are applied to the raw `local_grid` tensor (shape `(N, N, N)`,
binary float32) before feeding it to the encoder during pre-training. They
serve two purposes:

- **Robustness**: the encoder learns features that are invariant to
  viewpoint changes, minor geometric variation, and observation noise.
- **Data efficiency**: one episode of rollout data yields many distinct
  training samples via augmentation.

### Note on Rotational Diversity

**90° grid rotation and axis flip augmentations are not used.** Rotational
diversity is handled upstream at the STL level: before voxelizing, each
geometry is rotated by a random orientation sampled uniformly from SO(3). This
has two advantages over post-voxelization grid rotation:

- **Continuous coverage**: SO(3) covers every possible viewing angle, not just
  the 24 discrete orientations of the cubic group.
- **Clean voxelization**: rotating the mesh before voxelizing produces a
  proper binary occupancy grid for the rotated geometry. Rotating an already-
  voxelized grid at non-90° angles requires interpolation, introducing
  artefacts in a binary field.

See the `stl_list` sampler config (`rotations_per_geometry`) in the Data
Ingestion section for how this is configured.

### Augmentations

#### 1. Cutout (Box Dropout)

Zero out a random contiguous rectangular sub-volume of the grid. Forces the
encoder to not rely on any single region and to infer structure from context.
Complementary to masking in MAE (cutout zeros visible input; MAE masks input
tokens before the encoder sees them).

Config keys:
```yaml
cutout:
  count: 2          # number of cutout boxes per sample
  min_size: 1       # minimum side length in cells
  max_size: 2       # maximum side length in cells
```

For N=5 and `max_size=2`, each cutout removes at most 8 / 125 = 6.4% of
cells. With `count=2` up to ~13% of cells are zeroed.

#### 2. Geometry Paste

Cut a sub-block from one grid in the batch and paste it into a random
location of another grid. Splices geometry from different scenes together,
creating training samples that never appeared in rollout data. Teaches the
encoder to recognise partial geometric motifs regardless of surrounding
context.

Implementation: for a random pair (A, B) in a batch:
1. Sample a random sub-cube of size `paste_size × paste_size × paste_size`
   from B at position (px, py, pz).
2. Paste it into A at a random position, clamped to grid bounds (OR operation
   so geometry only grows).

Config keys:
```yaml
geometry_paste:
  probability: 0.3   # fraction of batch pairs to augment
  paste_size: 2      # side length of the extracted sub-cube
```

#### 3. Noise (Cell Flip)

Randomly flip individual cell values (0→1 or 1→0) with probability `p`.
Simulates sensor noise and imperfect voxelisation.

Config key: `noise_prob: 0.05`  (5% of cells flipped per sample)

#### 4. Translation Jitter

Shift the entire grid by ±1 cell along one or more axes, padding with zeros
at the boundary. Equivalent to the agent standing one step away from its
actual position — the encoder should extract the same features regardless of
sub-cell offset.

Config key: `translation_jitter: 1`  (max shift in cells, each axis
independently)

#### 7. Morphological Variation (Erosion / Dilation)

Erode or dilate the binary grid using a 3×3×3 structuring element. Erosion
shrinks solid regions (thinner walls); dilation expands them (thicker walls).
Simulates geometry scale variation without changing the scene topology.

Implementation: `scipy.ndimage.binary_erosion` /
`scipy.ndimage.binary_dilation`.

Config key: `morph_prob: 0.1`  (probability of applying erosion or dilation)

### Augmentation Composition

Augmentations are applied in the order listed above. Rotational diversity
comes from the STL-level SO(3) rotation in the data source, not from
post-hoc grid transforms. The remaining augmentations operate on the already-
voxelized (N, N, N) grid: cutout and paste first, then noise, then jitter.

```yaml
augmentation:
  cutout:
    count: 2
    min_size: 1
    max_size: 2
  geometry_paste:
    probability: 0.3
    paste_size: 2
  noise_prob: 0.05
  translation_jitter: 1
  morph_prob: 0.1
```

---

## Architecture 3: Tri-Planar 2D CNN (`voxel_triplanar_2dcnn`)

### Concept

Instead of Conv3d over the full cube or Conv2d with z-as-channels, extract
the three orthogonal center slices of the local grid and stack them as a
3-channel 2D image. A standard Conv2d encoder processes this (3, N, N) tensor.

```
local_grid (N, N, N)
  → XY slice at z = N//2  →  (N, N)  ← top-down:  floor/ceiling obstacles
  → XZ slice at y = N//2  →  (N, N)  ← front view: vertical walls ahead/behind
  → YZ slice at x = N//2  →  (N, N)  ← side view:  walls left/right

stack → (3, N, N)
```

This is the tri-planar projection technique from 3D medical imaging, adapted
for binary voxel grids.

### Why it is useful for pre-training

- **~8× cheaper** than Conv3d (2D kernels, no depth dimension in ops).
- **Interpretable**: each channel is a readable 2D map — easy to visualise
  what the encoder sees during pre-training.
- **Sufficient for navigation**: the agent needs to know what is directly
  ahead, above, and to the side. Center slices capture exactly these planes.
- **Off-center blind spot**: a wall at z = center+2 is invisible to the XZ
  slice. This is the key limitation vs. the 3D CNN.

### Architecture

```
Input: (B, 3, N, N)

Conv2d(3,  32, kernel_size=3, padding=1)  → ReLU → (B, 32, N, N)
Conv2d(32, 64, kernel_size=3, padding=1)  → ReLU → (B, 64, N, N)
Conv2d(64, 64, kernel_size=3, padding=1)  → ReLU → (B, 64, N, N)
AdaptiveAvgPool2d(1)                               → (B, 64)
Linear(64, latent_dim)                             → (B, latent_dim)
```

### Decoder (for AE pre-training)

```
z (B, latent_dim)
Linear(latent_dim, 64)                    → (B, 64)
Reshape                                   → (B, 64, 1, 1)
Upsample(size=(N, N))                     → (B, 64, N, N)
ConvTranspose2d(64, 64, 3, padding=1)     → ReLU → (B, 64, N, N)
ConvTranspose2d(64, 32, 3, padding=1)     → ReLU → (B, 32, N, N)
ConvTranspose2d(32,  3, 3, padding=1)     → Sigmoid → (B, 3, N, N)
```

Loss: BCE between each reconstructed slice and its corresponding input slice.

### MVM variant

Masking applies to each 2D slice independently — mask 75% of cells in each
(N, N) plane. The transformer decoder predicts all three masked planes from
the latent vector `z`. This is simpler than 3D MVM since attention operates
over N² positions (25 for N=5) rather than N³ (125).

### Comparison with existing architectures

| Property | `voxel_box_2dcnn` (z-as-channels) | `voxel_triplanar_2dcnn` | `voxel_box_3dcnn` |
|---|---|---|---|
| Input to conv | (B, N, N, N) | (B, 3, N, N) | (B, 1, N, N, N) |
| Depth coverage | All z-levels via channels | Center slice only | Full 3D |
| Ops per layer | N³ × k² | 3 × N² × k² | N³ × k³ |
| Interpretable slices | No | Yes | No |
| Off-center depth | Yes (via channels) | No | Yes |
| Recommended for | Lightweight RL policy | Pre-training inspection / fast sweep | Rich geometry tasks |

### YAML Config

```yaml
model_garden:
  name: triplanar_ae_v1
  architecture: voxel_triplanar_2dcnn
  approach: autoencoder           # autoencoder | vae | mvmencoder

  data:
    sources:
      - type: position_sample
        geometry:
          env:
            geometry_boxes:
              - [10, 10, 10, 22, 22, 22]
            grid_size: 32
        num_samples: 200000
    cache:
      path: runtime/garden/cache
      force_refresh: false
    split:
      val_fraction: 0.1
      seed: 42

  augmentation:
    cutout:
      count: 2
      min_size: 1
      max_size: 2
    noise_prob: 0.05
    translation_jitter: 1

  encoder:
    box_radius: 2
    conv_channels: [32, 64, 64]
    latent_dim: 128

  autoencoder:
    variant: ae

  training:
    epochs: 100
    batch_size: 256
    lr: 3.0e-4
    lr_scheduler: cosine
    val_fraction: 0.1
    early_stop_patience: 10
```

---

## Approach 1: Autoencoder (AE)

### Overview

Train an encoder–decoder pair to reconstruct the input voxel grid. After
pre-training, discard the decoder. The encoder maps a `(N, N, N)` binary grid
to a latent vector `z` of fixed size `latent_dim`.

```
input grid (N³) → [Encoder] → z (latent_dim,) → [Decoder] → reconstructed grid (N³)
```

### Architecture

**Encoder** — mirrors the `VoxelBox3DCNN` conv stack from `cnn-models.md`:

```
Input: (B, 1, N, N, N)
Conv3d(1,  32, 3, padding=1) → ReLU → (B, 32, N, N, N)
Conv3d(32, 64, 3, padding=1) → ReLU → (B, 64, N, N, N)
Conv3d(64, 64, 3, padding=1) → ReLU → (B, 64, N, N, N)
AdaptiveAvgPool3d(1)                 → (B, 64)
Linear(64, latent_dim)               → (B, latent_dim)   ← encoder output z
```

**Decoder** — symmetric, mirrors encoder in reverse:

```
z (B, latent_dim)
Linear(latent_dim, 64)               → (B, 64)
Reshape                              → (B, 64, 1, 1, 1)
Upsample(size=(N, N, N))             → (B, 64, N, N, N)
ConvTranspose3d(64, 64, 3, padding=1) → ReLU → (B, 64, N, N, N)
ConvTranspose3d(64, 32, 3, padding=1) → ReLU → (B, 32, N, N, N)
ConvTranspose3d(32,  1, 3, padding=1) → Sigmoid → (B, 1, N, N, N)
```

Sigmoid output is compared to the binary input grid.

### Loss

Binary cross-entropy between reconstructed and original grid:

```
L = BCE(reconstruction, input_grid)
```

Geometry voxels (always filled) and free space (always empty) dominate;
weighting by occupancy ratio is recommended when geometry_boxes are present
(geometry cells are <15% of grid for typical configs):

```
L = BCE(reconstruction, input_grid, pos_weight=neg_count/pos_count)
```

### VAE Variant

Add a KL divergence term to regularise the latent space:

```
Encoder outputs: mu (latent_dim,), log_var (latent_dim,)
z = mu + eps * exp(0.5 * log_var)   (reparameterisation trick)
L = BCE(reconstruction, input_grid) + beta * KL(N(mu, var) || N(0, I))
```

Config key: `variant: vae` with `beta: 1.0` (β-VAE). The structured latent
space makes interpolation and latent-space inspection possible.

### YAML Config

```yaml
model_garden:
  name: 3dcnn_ae_v1
  architecture: voxel_box_3dcnn   # voxel_box_3dcnn | voxel_box_2dcnn
  approach: autoencoder            # autoencoder | vae | mvmencoder

  data:
    sources:
      - type: position_sample
        geometry:
          env:
            geometry_boxes:
              - [10, 10, 10, 22, 22, 22]
            grid_size: 32
        num_samples: 200000
    cache:
      path: runtime/garden/cache
      force_refresh: false
    split:
      val_fraction: 0.1
      seed: 42

  augmentation:
    rotate_90: true
    flip_axes: true
    cutout:
      count: 2
      min_size: 1
      max_size: 2
    noise_prob: 0.05
    translation_jitter: 1

  encoder:
    box_radius: 2                  # N = 2*box_radius+1
    conv_channels: [32, 64, 64]
    latent_dim: 128

  autoencoder:
    variant: ae                    # ae | vae
    beta: 1.0                      # only for vae

  training:
    epochs: 100
    batch_size: 256
    lr: 3.0e-4
    lr_scheduler: cosine
    val_fraction: 0.1
    early_stop_patience: 10
```

---

## Approach 2: Masked Voxel Modeling (MVM)

### Overview

Randomly mask 75% of the local grid cells before they reach the encoder.
Train a lightweight transformer decoder to predict the values of all masked
cells from the encoder's latent representation. The encoder is forced to learn
global structure from sparse local cues.

```
input (masked, 25% visible) → [Encoder 3D CNN] → z → [Transformer Decoder] → predicted masked cells
```

### Why this works better than AE for navigation

An AE encoder receives the full grid and can reconstruct locally — it learns
local statistics. With 75% masking:

- The encoder sees only 31 of 125 cells (for N=5).
- It must infer whether the wall extends beyond its visible patch.
- Representations encode geometric context (concave corner, open corridor,
  box edge) rather than local cell patterns.

These structural features are exactly what a navigation policy needs.

### Architecture

**Input preparation**

```
local_grid (N³,)
  → reshape to (N, N, N)
  → sample mask M: 75% of positions set to mask token value (learnable scalar)
  → visible cells keep their original binary value
  → add positional encoding: each cell (i,j,k) gets a 3D sinusoidal embedding
```

**Encoder** — identical to the AE encoder (3D CNN). Receives the masked grid
as a standard `(B, 1, N, N, N)` tensor. The mask token is a learnable value
(initialised to 0.5) substituted at masked positions.

**Decoder** — lightweight 2-layer transformer:

```
z (B, latent_dim)
  → expand to (B, N³, latent_dim)  with positional embedding per cell
  → TransformerDecoderLayer(d_model=latent_dim, nhead=4, dim_feedforward=256)  × 2
  → Linear(latent_dim, 1) + Sigmoid
  → (B, N³)   ← predicted occupancy for all cells
```

**Loss** — BCE on masked cells only:

```
L = BCE(pred[M], target[M])
```

Unmasked cells are excluded from the loss — the encoder gets no gradient
signal for cells it already saw.

**At inference**: discard the decoder. Run the 3D CNN encoder on the
unmasked grid (all cells visible). The learned weights transfer directly.

### YAML Config

```yaml
model_garden:
  name: 3dcnn_mvm_v1
  architecture: voxel_box_3dcnn
  approach: mvmencoder

  data:
    sources:
      - type: position_sample
        geometry:
          env:
            geometry_boxes:
              - [10, 10, 10, 22, 22, 22]
            grid_size: 32
        num_samples: 200000
    cache:
      path: runtime/garden/cache
      force_refresh: false
    split:
      val_fraction: 0.1
      seed: 42

  augmentation:
    noise_prob: 0.05

  encoder:
    box_radius: 2
    conv_channels: [32, 64, 64]
    latent_dim: 128

  mvmencoder:
    mask_ratio: 0.75
    decoder_layers: 2
    decoder_dim: 64
    decoder_heads: 4

  training:
    epochs: 100
    batch_size: 256
    lr: 3.0e-4
    lr_scheduler: cosine
    val_fraction: 0.1
    early_stop_patience: 10
```

---

## Model Garden Store

### Directory layout

```
runtime/garden/
  3dcnn_ae_v1/
    encoder.pt              # encoder weights only (state_dict)
    meta.json               # architecture, training config, metrics
    loss_curve.json         # train/val loss per epoch
  3dcnn_ae_v1_vae/
    encoder.pt
    meta.json
    loss_curve.json
  3dcnn_mvm_v1/
    encoder.pt
    meta.json
    loss_curve.json
```

### `meta.json` schema

```json
{
  "name": "3dcnn_ae_v1",
  "status": "experimental",
  "approach": "autoencoder",
  "architecture": "voxel_box_3dcnn",
  "latent_dim": 128,
  "box_radius": 2,
  "conv_channels": [32, 64, 64],
  "num_pretrain_steps": 200000,
  "epochs_trained": 87,
  "final_val_loss": 0.043,
  "created_at": "2026-03-20T17:00:00Z",
  "certification": {
    "report": null,
    "failed_gates": [],
    "unrun_gates": ["stage_7/full_certification"]
  },
  "augmentation": { "cutout": {"count": 2, "min_size": 1, "max_size": 2}, "noise_prob": 0.05, "translation_jitter": 1 }
}
```

`status` is required for newly published checkpoints and has two allowed values:

- `experimental`: the checkpoint passes the interim publication requirements in
  [Standalone Voxel Encoder Pretraining](../subsystems/model-registry/contract/certification.md), but has
  failed or not yet run one or more final certification gates. It must not be selected
  as a default, and `meta.json` must list the failed and unrun gates.
- `validated`: the checkpoint passed the complete locked standalone certification
  suite. Only validated checkpoints are eligible to become defaults.

Existing garden entries without `status` are treated as `experimental` until they are
recertified. Training loss alone never promotes a checkpoint to `validated`.

---

## CLI Commands

All garden commands use `rich` for output: `Panel` for summaries,
`Table` for lists, `Progress` for long-running steps (data collection,
training epochs). Import path: `from rich.console import Console`,
`from rich.table import Table`, `from rich.panel import Panel`,
`from rich.progress import Progress`.

---

### `anysearch garden train <config>`

Pre-train an encoder from a YAML config file. Collects and caches observation
data, runs pre-training, saves checkpoint to `runtime/garden/<name>/`.

```bash
anysearch garden train usage/experiments/garden/3dcnn_ae.yaml
anysearch garden train usage/experiments/garden/3dcnn_mvm.yaml
```

Options:
```
--output-dir PATH    Override garden store location (default: runtime/garden)
--resume             Resume from last epoch checkpoint if interrupted
--device TEXT        torch device: cpu | cuda | cuda:0 (default: auto-detect)
```

Data collection shows a Rich progress bar per source:
```
Collecting data ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 60000/60000
  source 1  position_sample / stl_list              60000 samples  cached ✓
  source 2  training_run   / multi_agent_ppo_asha   12400 samples  cached ✓
```

Training shows epoch progress with live loss:
```
Training  epoch 87/100  ━━━━━━━━━━━━━━━━━━━━━━━━━ 87%  train 0.0441  val 0.0431
```

Completion panel:
```
╭─ Garden train complete ──────────────────────────────────────────────────╮
│  model            3dcnn_ae_v1                                            │
│  approach         autoencoder                                            │
│  epochs           87 / 100  (early stop, patience 10)                   │
│  final val loss   0.0431                                                 │
│  saved to         runtime/garden/3dcnn_ae_v1/encoder.pt                 │
│  use in RL        pretrained_encoder: 3dcnn_ae_v1                       │
╰──────────────────────────────────────────────────────────────────────────╯
```

---

### `anysearch garden extract <config>`

Run only the data collection step from a garden YAML — no training. Voxelizes
geometries, samples positions, and writes all observation `.npz` files to the
cache. Subsequent `garden train` calls on the same config skip collection
entirely and go straight to training.

Useful for:
- Pre-collecting a large dataset overnight before a training run
- Reusing one dataset across multiple model configs (different architecture,
  approach, or hyperparameters) without re-collecting
- Inspecting dataset size and coverage before committing to training

```bash
anysearch garden extract usage/experiments/garden/3dcnn_ae.yaml
anysearch garden extract usage/experiments/garden/dataset.yaml   # standalone data config
```

Options:
```
--cache-dir PATH     Override cache location (default: runtime/garden/cache)
--force-refresh      Re-collect and overwrite existing cache entries
--dry-run            Print what would be collected without writing anything
```

A garden YAML's `data:` block can also be factored into a **standalone data
config** and referenced by path. This lets multiple model configs share one
extracted dataset:

```yaml
# usage/experiments/garden/dataset.yaml — standalone, no model_garden key
data:
  sources:
    - type: position_sample
      geometry:
        sampler:
          type: stl_list
          dir: data/geometries/obstacles/
          scale: 40.0
          total_samples: 60000
          seed: 42
    - type: training_run
      run: multi_agent_ppo_asha:v3
      obs_key: local_grid
  cache:
    path: runtime/garden/cache
    force_refresh: false
  split:
    val_fraction: 0.1
    seed: 42
```

Reference it from model configs with a path instead of an inline `data:` block:

```yaml
model_garden:
  name: 3dcnn_ae_v1
  architecture: voxel_box_3dcnn
  approach: autoencoder
  data: usage/experiments/garden/dataset.yaml   # path to standalone data config
  ...
```

`garden train` resolves the path, checks the cache, and skips collection if
all sources are already cached.

**Dry-run output:**
```
╭─ Garden extract — dry run ───────────────────────────────────────────────╮
│  config       usage/experiments/garden/dataset.yaml                      │
│  cache dir    runtime/garden/cache                                        │
╰──────────────────────────────────────────────────────────────────────────╯

 #   Type             Geometry                    Samples   Cached
 ─── ──────────────── ──────────────────────────  ───────   ──────
 1   position_sample  stl_list (3 files, SO(3))   60000     no
 2   training_run     multi_agent_ppo_asha:v3      12400     yes

 Total  72400 samples  (60000 to collect, 12400 cached)
```

**Collection output:**
```
Extracting dataset ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

 Voxelizing  stepped_terrain.stl   rotation  1/20  ━━━━━━━━━━━ done
 Voxelizing  pipe_junction.stl     rotation  1/20  ━━━━━━━━━━━ done
 Sampling    source 1 / stl_list             60000 samples  → obs/c9a1f3.npz
 Loading     source 2 / training_run         12400 samples  → cached ✓

╭─ Garden extract complete ────────────────────────────────────────────────╮
│  total samples    72400                                                   │
│  train            65160  (90%)                                            │
│  val               7240  (10%)                                            │
│  worlds cached    40  (stepped_terrain × 20, pipe_junction × 20)         │
│  obs cached       runtime/garden/cache/obs/c9a1f3.npz                    │
╰──────────────────────────────────────────────────────────────────────────╯
```

---

### `anysearch garden add <run_ref>`

Register a completed RL training run as a `training_run` data source.
Extracts `local_grid` observations from all trajectory JSON files in the run
directory, caches them as an observation `.npz`, and writes an entry to
`runtime/garden/cache/runs.json` so the source can be referenced by name in
YAML data configs.

```bash
anysearch garden add multi_agent_ppo_asha:v3
anysearch garden add ppo-baseline:a1b2c3d4
```

Options:
```
--obs-key TEXT    Observation field to extract (default: local_grid)
--tag TEXT        Short label for this data source (default: run name)
```

Output:
```
╭─ Garden add ─────────────────────────────────────────────────────────────╮
│  run              multi_agent_ppo_asha:v3                                │
│  trajectories     14  files                                              │
│  observations     12400  local_grid samples extracted                    │
│  cached to        runtime/garden/cache/obs/f3a91c.npz                   │
│  use as source    type: training_run                                     │
│                   run: multi_agent_ppo_asha:v3                           │
╰──────────────────────────────────────────────────────────────────────────╯
```

---

### `anysearch garden list`

List all pre-trained encoder models in the garden store. The table includes the
`status` column so experimental artifacts cannot be mistaken for validated defaults.

```bash
anysearch garden list
```

Output (Rich `Table`):
```
 Name                 Status        Approach       Arch          Latent  Val loss  Created
 ─────────────────── ───────────── ─────────────  ────────────  ──────  ────────  ──────────
 3dcnn_ae_v1          experimental  autoencoder    3dcnn         128     0.0431    2026-03-20
 3dcnn_ae_v1_vae      experimental  vae            3dcnn         128     0.0389    2026-03-20
 3dcnn_mvm_v1         validated     mvmencoder     3dcnn         128     0.0521    2026-03-20
 triplanar_ae_v1      experimental  autoencoder    triplanar_2d  128     0.0612    2026-03-21
```

---

### `anysearch garden inspect <name>`

Print detailed metadata and per-epoch loss curve for a model, including its status and
failed or unrun certification gates.

```bash
anysearch garden inspect 3dcnn_mvm_v1
```

Output:
```
╭─ 3dcnn_mvm_v1 ───────────────────────────────────────────────────────────╮
│  status           validated                                              │
│  approach         mvmencoder                                             │
│  architecture     voxel_box_3dcnn                                        │
│  latent_dim       128                                                    │
│  box_radius       2                                                      │
│  conv_channels    [32, 64, 64]                                           │
│  pretrain steps   200000                                                 │
│  epochs           100                                                    │
│  final val loss   0.0521                                                 │
│  augmentation     cutout  noise_prob=0.05  translation_jitter=1          │
╰──────────────────────────────────────────────────────────────────────────╯

 Epoch   Train loss   Val loss
 ──────  ──────────   ────────
     10      0.1901     0.1843
     20      0.1188     0.1102
     30      0.0944     0.0891
    ...
    100      0.0559     0.0521
```

---

## Custom Encoder Models

In addition to the built-in `voxel_box_3dcnn`, `voxel_box_2dcnn`, and
`voxel_triplanar_2dcnn` architectures, any `torch.nn.Module` can be used as
the encoder by specifying `architecture: custom` and providing the class path.

### Contract

A custom encoder must:
1. Accept a single tensor input of shape `(B, ...)` matching the grid format
   for the chosen architecture — `(B, 1, N, N, N)` for 3D, `(B, 3, N, N)` for
   triplanar, or `(B, N, N, N)` for 2D.
2. Return a single tensor of shape `(B, latent_dim)`.
3. Be importable from the Python path at train time.

The garden pre-training system wraps the custom encoder with a decoder
automatically (AE) or transformer (MVM); the encoder just needs to produce
the latent vector.

### YAML Config

```yaml
model_garden:
  name: custom_encoder_v1
  architecture: custom
  approach: autoencoder

  custom_encoder:
    class: my_package.models.MySpatialEncoder   # importlib.import_module path
    kwargs:
      in_channels: 1
      latent_dim: 128
      depth: 4
```

`kwargs` are passed verbatim as `**kwargs` to the class constructor. The
`latent_dim` key must appear in `kwargs` and its value must match
`encoder.latent_dim` (used by the decoder).

### Loading logic

```python
import importlib

def load_encoder(cfg: dict) -> nn.Module:
    if cfg["architecture"] == "custom":
        module_path, class_name = cfg["custom_encoder"]["class"].rsplit(".", 1)
        cls = getattr(importlib.import_module(module_path), class_name)
        return cls(**cfg["custom_encoder"].get("kwargs", {}))
    # ... built-in architectures
```

---

## Integration with RL Training

### YAML

Add `pretrained_encoder` and `finetune_mode` to the `model_config` block of
any training experiment YAML:

```yaml
model_config:
  custom_model: voxel_box_3d_cnn
  pretrained_encoder: 3dcnn_ae_v1     # name from garden store
  finetune_mode: top_layer            # frozen | top_layer | full
  custom_model_config:
    box_radius: 2
    conv_channels: [32, 64, 64]
    fc_hiddens: [256]
```

### Fine-tune modes

| Mode | Frozen layers | Trainable layers | Use when |
|---|---|---|---|
| `frozen` | All encoder conv layers | Policy + value heads only | Encoder is strong; fast RL training |
| `top_layer` | All conv layers | Last linear projection + policy/value heads | Default; small fine-tune budget |
| `full` | None | All encoder layers + heads | Long RL runs; encoder needs task adaptation |

### Loading logic (in `VoxelBox3DCNN.__init__`)

```python
pretrained = model_config.get("pretrained_encoder")
if pretrained:
    garden_dir = Path(os.environ.get("ANYSEARCH_GARDEN", "runtime/garden"))
    ckpt = garden_dir / pretrained / "encoder.pt"
    state = torch.load(ckpt, map_location="cpu")
    self.encoder.load_state_dict(state)

finetune_mode = model_config.get("finetune_mode", "top_layer")
if finetune_mode == "frozen":
    for p in self.encoder.parameters():
        p.requires_grad_(False)
elif finetune_mode == "top_layer":
    for p in self.encoder[:-1].parameters():   # freeze all but last Linear
        p.requires_grad_(False)
# "full": all parameters remain trainable (default)
```

---

## Implementation Order

1. **`theseo_anysearch/garden/augment.py`** — augmentation functions for
   `(N, N, N)` numpy arrays: rotation, flip, cutout, paste, noise, jitter,
   morph. Each function takes a grid and config dict, returns a grid.

2. **`theseo_anysearch/core/src/bridge/py_bindings.rs`** — add
   `PyVoxelSampler` struct with `load_stl()`, `load_geometry_boxes()`,
   `free_cells()`, and `sample_box_obs(positions, radius)` methods. Exposes
   batch position-based observation extraction without episode overhead.

3. **`theseo_anysearch/garden/collect.py`** — collection pipeline:
   `PositionSampleCollector`, `TrainingRunCollector`. Each collector yields
   numpy arrays. `GeometrySampler` handles `random_boxes` and `stl_list`
   (with SO(3) rotation + two-level cache: `worlds/` for voxelized geometries,
   `obs/` for extracted observation arrays). `runs.json` registry maps run
   refs to cached observation paths for `type: training_run` sources.

4. **`theseo_anysearch/garden/dataset.py`** — `GardenDataset`
   (`torch.utils.data.Dataset`): loads cached `.npz` files from all sources,
   concatenates, shuffles, splits train/val, applies online augmentation per
   sample.

3. **`theseo_anysearch/garden/models/ae.py`** — `VoxelAE` and `VoxelVAE`
   PyTorch modules. Supports all three encoder architectures (`3dcnn`,
   `triplanar_2dcnn`, `2dcnn`). Decoder architecture mirrors encoder type.
   Decoder discarded after training.

4. **`theseo_anysearch/garden/models/mvm.py`** — `VoxelMVMEncoder` PyTorch
   module. For `triplanar_2dcnn`, masking and the transformer decoder operate
   over the flattened 2D slice positions (N² tokens per slice, 3 slices).
   For `3dcnn`, masking operates over N³ positions. Decoder discarded after
   training.

5. **`theseo_anysearch/garden/trainer.py`** — training loop, early stopping,
   checkpoint saving to garden store.

6. **`theseo_anysearch/garden/store.py`** — `GardenStore` class: `save()`,
   `load_encoder()`, `list()`, `inspect()`.

7. **`theseo_anysearch/garden/data_config.py`** — `DataConfig` Pydantic model
   for the standalone `data:` YAML. `resolve_data_config(path_or_inline)`
   helper: if the `data:` value is a string path, load and parse that file;
   if it is a dict, parse inline. Used by both `garden extract` and
   `garden train`.

8. **`theseo_anysearch/cli/commands/garden.py`** — `anysearch garden extract`,
   `train`, `add`, `list`, `inspect` CLI commands. All output via `rich`:
   `Panel` for summaries, `Table` for lists, `Progress` for world voxelization,
   data collection, and training epoch loops. Single `Console` instance; no
   `print()` calls.

8. **`theseo_anysearch/garden/encoder.py`** — `load_encoder(cfg)` factory
   function. Handles built-in architectures and `architecture: custom` via
   `importlib.import_module`. Called by both the garden trainer and the RL
   model loader.

9. **`theseo_anysearch/rllib/models/cnn.py`** — extend `VoxelBox3DCNN` and
   `VoxelBox2DCNN` to accept `pretrained_encoder` and `finetune_mode` from
   `custom_model_config`; call `load_encoder` for `architecture: custom`.

9. **`usage/experiments/garden/`** — reference YAML configs for AE and MVM
   pre-training.

---

## Limitations and Open Questions

- **Geometry diversity**: pre-training on a single `geometry_boxes` config
  produces an encoder specialised to box obstacles. Pre-training on a random
  mixture of box configs (varying sizes, positions, counts) yields more
  general features. A `geometry_sampler` option in `pretrain_data` is a
  future extension.
- **Tri-planar vs z-as-channels**: `voxel_triplanar_2dcnn` takes 3 center
  slices as a 3-channel image. `voxel_box_2dcnn` (z-as-channels) sees all N
  depth levels but mixes them through channel interactions rather than direct
  3D convolution. For most pre-training purposes, tri-planar is preferred
  because slices are interpretable and augmentation (rotation, cutout) maps
  cleanly to 2D ops.
- **Contrastive pre-training** (SimCLR-style) is a strong alternative to AE
  and MVM and may be added later. It requires two augmented views per sample
  and an NT-Xent loss but no decoder.
- **Transfer to multi-agent**: all agents share a single policy and therefore
  a single encoder. Pre-training is single-agent (simpler data collection);
  the learned encoder transfers directly to the shared policy.
