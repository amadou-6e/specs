---
title: Historical Torch architectures
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

> Historical source; not an authoritative current design.

# Torch Architectures

All neural network models in AnySearch. Two families: **garden** (self-supervised
pre-training on voxel geometry) and **policy** (RL via RLlib). Both share common
building blocks.

---

## Building Blocks

All shared primitives live in `theseo_anysearch/garden/models/ae.py` and
`theseo_anysearch/rllib/models/cnn.py`.

---

### `_ResBlock3D`

**File:** `theseo_anysearch/garden/models/ae.py`

ResNet-style 3D block with optional spatial downsampling. Used in `VoxelEncoder3D`.

```
Input: (B, in_ch, D, H, W)

body:
  Conv3d(in_ch, out_ch, 3, stride, pad=1, bias=False)
  BatchNorm3d(out_ch)
  ReLU
  Conv3d(out_ch, out_ch, 3, stride=1, pad=1, bias=False)
  BatchNorm3d(out_ch)

skip:
  if in_ch != out_ch or stride != 1:
    Conv3d(in_ch, out_ch, 1, stride, bias=False)
    BatchNorm3d(out_ch)
  else:
    Identity

Output: ReLU(body(x) + skip(x))  →  (B, out_ch, D/stride, H/stride, W/stride)
```

**Parameters:**

| Param | Type | Description |
|---|---|---|
| `in_ch` | int | Input channels |
| `out_ch` | int | Output channels |
| `stride` | int (default 1) | `stride=2` halves all spatial dimensions |

**Notes:**
- `bias=False` throughout — BN handles bias.
- Skip path is a learned 1×1×1 projection whenever channels or spatial size change.
- Two convolutions per block (pre-activation style body, post-activation output).

---

### `_UpsampleBlock3D`

**File:** `theseo_anysearch/garden/models/ae.py`

Trilinear upsample + Conv3D + BN + ReLU. Used in `VoxelDecoder3D`. Preferred over
`ConvTranspose3d` because it avoids checkerboard artefacts.

```
Input: (B, in_ch, D, H, W)

  Upsample(scale_factor=2, mode="trilinear", align_corners=False)   → (B, in_ch, 2D, 2H, 2W)
  Conv3d(in_ch, out_ch, 3, padding=1, bias=False)
  BatchNorm3d(out_ch)
  ReLU

Output: (B, out_ch, 2D, 2H, 2W)
```

---

### `_ConvBlock2D`

**File:** `theseo_anysearch/garden/models/ae.py`

Plain 2D conv block. Used in the 2D and triplanar garden encoder variants.

```
Conv2d(in_ch, out_ch, 3, padding=1)
ReLU
```

---

### Helper stacks in `cnn.py`

**File:** `theseo_anysearch/rllib/models/cnn.py`

Three `nn.Sequential` builders shared by all RL policy models:

```python
_build_conv2d_stack(in_channels, channels)  -> (Sequential, last_c)
_build_conv3d_stack(channels, in_channels=1) -> (Sequential, last_c)
_build_fc_stack(in_features, hiddens)       -> (Sequential, last_d)
```

Each layer in the conv stacks is `Conv(k=3, pad=1) + ReLU`.
Each layer in the FC stack is `Linear(d, h) + ReLU`.
No BN — these are used for online RL where small batch sizes make BN noisy.

---

## Garden Pre-training Models

Pre-training learns geometry representations from raw voxel grids. Only the encoder
is kept after training; the decoder is discarded.

**Files:**
- `theseo_anysearch/garden/models/ae.py` — AE / VAE
- `theseo_anysearch/garden/models/mvm.py` — Masked Voxel Modeling

All garden models accept `(B, N, N, N)` float32 binary grids where N = 2*box_radius+1.

---

### `VoxelEncoder3D`

**Location:** `theseo_anysearch/garden/models/ae.py`
**Used by:** `VoxelAE`, `VoxelVAE`, `VoxelMVMEncoder`, `VoxelBox3DCNNPretrained`

3D ResNet encoder. Produces a fixed-length latent vector regardless of grid size.

```
Input: (B, N, N, N)   →   unsqueeze(1)   →   (B, 1, N, N, N)

channels = [c0, c1, ..., ck]
strides  = [1,  2,  ..., 2 ]   # first block stride=1, rest stride=2

Block 0: _ResBlock3D(1,  c0, stride=1)   →  (B, c0, N,   N,   N  )
Block 1: _ResBlock3D(c0, c1, stride=2)   →  (B, c1, N/2, N/2, N/2)
Block 2: _ResBlock3D(c1, c2, stride=2)   →  (B, c2, N/4, N/4, N/4)
...

AdaptiveAvgPool3d(1)   →   (B, ck, 1, 1, 1)
Flatten                →   (B, ck)
Linear(ck, latent_dim) →   (B, latent_dim)
```

**Spatial sizes for N=5 (box_radius=2):**

| channels | strides | sizes after each block |
|---|---|---|
| [32, 64] | [1, 2] | 5 → 3 |
| [32, 64, 64] | [1, 2, 2] | 5 → 3 → 2 |
| [64, 128, 128] | [1, 2, 2] | 5 → 3 → 2 |
| [64, 128, 128, 128] | [1, 2, 2, 2] | 5 → 3 → 2 → 1 |

`AdaptiveAvgPool3d(1)` collapses whatever spatial size remains to a single value per channel, so the depth of the `channels` list does not change the output shape.

**Constructor:**

```python
VoxelEncoder3D(n: int, channels: list[int], latent_dim: int)
```

---

### `VoxelDecoder3D`

**Location:** `theseo_anysearch/garden/models/ae.py`
**Used by:** `VoxelAE`, `VoxelVAE`
**Discarded after pre-training.**

Progressive trilinear decoder. Doubles spatial size at each block, then upsizes to N.

```
Input: (B, latent_dim)

Linear(latent_dim, rev[0])      →  (B, rev[0])
reshape                          →  (B, rev[0], 1, 1, 1)

rev = list(reversed(channels))

_UpsampleBlock3D(rev[0], rev[1])   →  (B, rev[1], 2, 2, 2)
_UpsampleBlock3D(rev[1], rev[2])   →  (B, rev[2], 4, 4, 4)
...

Upsample(size=(N,N,N), trilinear)   →  (B, rev[-1], N, N, N)
Conv3d(rev[-1], 1, 3, padding=1)    →  (B, 1, N, N, N)
Sigmoid                             →  (B, 1, N, N, N)  ∈ [0, 1]
```

**Constructor:**

```python
VoxelDecoder3D(n: int, channels: list[int], latent_dim: int)
```

---

### `VoxelEncoder2D`

2D CNN treating the z-axis as channels. Lighter than 3D, loses volumetric depth.

```
Input: (B, N, N, N)  →  permute(0,3,1,2)  →  (B, N, N, N)  (z-as-channel)

ch = [N, c0, c1, ..., ck]
_ConvBlock2D(ch[i], ch[i+1]) for each pair
AdaptiveAvgPool2d(1)   →  (B, ck)
Linear(ck, latent_dim) →  (B, latent_dim)
```

---

### `VoxelEncoderTriplanar`

Takes three orthogonal center slices and stacks them as channels.

```
Input: (B, N, N, N)
  xy = x[:, :, :, N//2]    # (B, N, N)
  xz = x[:, :, N//2, :]    # (B, N, N)
  yz = x[:, N//2, :, :]    # (B, N, N)
  stack → (B, 3, N, N)

ch = [3, c0, c1, ..., ck]
_ConvBlock2D stack + AdaptiveAvgPool2d(1) + Linear
```

---

### `VoxelAE`

**Location:** `theseo_anysearch/garden/models/ae.py`
**Approach:** `autoencoder`

Standard deterministic autoencoder. Loss is focal BCE (or weighted BCE) between
reconstruction and input.

```
Encoder: VoxelEncoder3D / VoxelEncoder2D / VoxelEncoderTriplanar
           (B, N, N, N) → (B, latent_dim)

Decoder: VoxelDecoder3D / VoxelDecoder2D
           (B, latent_dim) → (B, 1, N, N, N)  ∈ [0,1]
```

**Loss:**

```python
def loss(x, pos_weight=None, focal_gamma=0.0):
    recon, _ = self(x)
    target = x.unsqueeze(1)          # (B, 1, N, N, N)

    if focal_gamma > 0:
        bce = F.binary_cross_entropy(recon, target, weight=pos_weight, reduction="none")
        p_t = recon * target + (1 - recon) * (1 - target)
        return ((1 - p_t) ** focal_gamma * bce).mean()
    return F.binary_cross_entropy(recon, target, weight=pos_weight)
```

`pos_weight` is auto-computed from batch fill rate: `(1 - fill) / fill`. At ~10% fill
this is ~9:1 weighting toward occupied voxels, preventing the model from collapsing to
predicting all-zero.

`focal_gamma=2` further down-weights easy empty predictions and focuses gradient on
hard boundary voxels. Best empirical value from tuning.

---

### `VoxelVAE`

**Location:** `theseo_anysearch/garden/models/ae.py`
**Approach:** `vae`

β-VAE variant. Encoder projects to `2 × latent_dim` (mu + log_var). Reparameterisation
trick samples z. Loss is BCE + β × KL divergence.

```
Encoder: build_encoder(..., latent_dim * 2)
  → out.chunk(2, dim=-1)  →  mu, log_var   each (B, latent_dim)

z = mu + exp(0.5 * log_var) * N(0,1)        reparameterisation

Decoder: VoxelDecoder3D(z)  →  (B, 1, N, N, N)

Loss: BCE(recon, target) + beta * KL
  KL = -0.5 * mean(1 + log_var - mu² - exp(log_var))
```

---

### `VoxelMVMEncoder`

**Location:** `theseo_anysearch/garden/models/mvm.py`
**Approach:** `mvmencoder`

Masked Voxel Modeling (MAE-style). 75% of voxels are replaced with a learnable scalar
mask token. The encoder produces a latent from the corrupted grid. A transformer decoder
attends from all N³ positions to the latent and predicts all cell values. Only masked
cell loss is back-propagated.

```
Input: (B, N, N, N)

_apply_mask:
  flatten → (B, N³)
  replace 75% of positions with mask_token (learnable scalar)
  reshape → (B, N, N, N)   [masked_grid]

encoder = build_encoder(architecture, n, channels, latent_dim)
  masked_grid → z   (B, latent_dim)

latent_proj: Linear(latent_dim, decoder_dim) → memory  (B, 1, decoder_dim)

pos_embed: Embedding(N³, decoder_dim) → queries  (B, N³, decoder_dim)

TransformerDecoder (decoder_layers × TransformerDecoderLayer):
  d_model = decoder_dim
  nhead   = decoder_heads
  ffn_dim = decoder_dim * 4
  norm_first = True
  batch_first = True
  (B, N³, decoder_dim) queries attend to (B, 1, decoder_dim) memory

head: Linear(decoder_dim, 1) → Sigmoid → preds  (B, N³)

Loss: BCE(preds[mask], target[mask])   # masked positions only
```

**Constructor:**

```python
VoxelMVMEncoder(
    architecture: str,      # "voxel_box_3dcnn" | "voxel_box_2dcnn" | ...
    n: int,
    channels: list[int],
    latent_dim: int,
    mask_ratio: float = 0.75,
    decoder_layers: int = 2,
    decoder_dim: int = 64,
    decoder_heads: int = 4,
)
```

---

## Garden Loss Summary

| Approach | Loss function | Notes |
|---|---|---|
| `autoencoder` | Focal BCE (γ) + pos_weight | γ=2, pos_weight auto from fill rate |
| `vae` | BCE + β × KL | β=1.0 default |
| `mvmencoder` | BCE on masked positions only | No pos_weight (masks make it balanced) |

---

## RL Policy Models

All policy models implement the RLlib legacy API (`TorchModelV2`) and produce
`(logits, state=[])` from `forward()` and a scalar value from `value_function()`.

**File:** `theseo_anysearch/rllib/models/cnn.py`

**Observation inputs (box obs mode):**

| Key | Shape | Description |
|---|---|---|
| `local_grid` | `(N³,)` | Flattened binary 3D voxel grid |
| `steps_remaining` | `(1,)` | Normalised ∈ [0,1] |
| `voxel_count` | `(1,)` | Absolute filled voxel count |
| `cursor_pos` | `(3,)` | (x,y,z) normalised ∈ [0,1] |

Scalars (5 total) are always concatenated with CNN output before the FC trunk.

---

### `VoxelBox2DCNN`

**Key:** `voxel_box_2d_cnn`

Interprets z-axis as channels and applies 2D convolutions over the XY plane.

```
local_grid (B, N³)
  → view(B, N, N, N)
  → permute(0, 3, 1, 2)          →  (B, z=N, x=N, y=N)

_build_conv2d_stack([N, c0, c1, ..., ck]):
  Conv2d(N,  c0, 3, pad=1) + ReLU
  Conv2d(c0, c1, 3, pad=1) + ReLU
  ...

AdaptiveAvgPool2d(1)  →  (B, ck, 1, 1)  →  flatten  →  (B, ck)
cat scalars           →  (B, ck + 5)
_build_fc_stack       →  (B, fc_out)
policy head           →  (B, num_outputs)
value head            →  (B, 1)
```

**Config keys:**

| Key | Default | Description |
|---|---|---|
| `box_radius` | 2 | Must match env. N = 2*box_radius+1 |
| `conv_channels` | [32, 64, 64] | Out-channels per Conv2d layer |
| `fc_hiddens` | [256] | FC hidden sizes |
| `pool_type` | "avg" | "avg" or "max" |

---

### `VoxelBox3DCNN`

**Key:** `voxel_box_3d_cnn`

Full 3D volumetric convolutions. Heavier than 2D but captures all spatial axes.

```
local_grid (B, N³)
  → view(B, 1, N, N, N)

_build_conv3d_stack([1, c0, c1, ..., ck]):
  Conv3d(1,  c0, 3, pad=1) + ReLU
  Conv3d(c0, c1, 3, pad=1) + ReLU
  ...

AdaptiveAvgPool3d(1)  →  (B, ck)
cat scalars           →  (B, ck + 5)
_build_fc_stack       →  (B, fc_out)
policy/value heads
```

Same `custom_model_config` keys as `VoxelBox2DCNN`.

**Note:** These conv stacks use plain `Conv + ReLU` without BN or residuals — suitable
for RL where batches are small and BN statistics are unreliable. The garden encoder uses
`_ResBlock3D` + BN because it trains on large fixed datasets.

---

### `VoxelHierarchicalBox3DCNN`

**Key:** `voxel_hierarchical_box_3d_cnn`

Multi-scale observation: two or more local grids at different radii are stacked as
channels and processed together by one 3D CNN.

```
local_grid (B, sum_i n_i³)   # concatenation of all scales

for each radius r_i (n_i = 2*r_i + 1):
  seg = grid[:, offset:offset + n_i³]  →  view(B, n_i, n_i, n_i)
  centre-pad to N_max × N_max × N_max

stack all padded volumes  →  (B, n_radii, N_max, N_max, N_max)

_build_conv3d_stack(channels, in_channels=n_radii)
AdaptiveAvgPool3d(1)
cat scalars
_build_fc_stack
policy/value heads
```

**Config keys:**

| Key | Default | Description |
|---|---|---|
| `box_radii` | [1, 4] | Radii in the same order as the observation |
| `conv_channels` | [32, 64, 64] | |
| `fc_hiddens` | [256] | |
| `pool_type` | "avg" | |

**Observation requirement:** `obs_mode: hierarchical_box` with matching `box_radii` in env.

---

### `VoxelBox3DCNNPretrained`

**Key:** `voxel_box_3d_cnn_pretrained`

Loads a garden-trained `VoxelEncoder3D` from the store and uses it as a frozen (or
fine-tunable) feature extractor. No conv layers are built from scratch.

```
At __init__:
  GardenStore.resolve_ref(encoder_ref)  →  model_dir
  read meta.json  →  box_radius, latent_dim, conv_channels
  VoxelEncoder3D(n, conv_channels, latent_dim)
  load encoder.pt weights
  if freeze: encoder.eval(), requires_grad_(False)

forward:
  local_grid  →  view(B, N, N, N)
  encoder(grid)  →  z  (B, latent_dim)    [no_grad if frozen]
  cat scalars    →  (B, latent_dim + 5)
  _build_fc_stack
  policy/value heads
```

**Config keys:**

| Key | Default | Description |
|---|---|---|
| `pretrained_encoder` | required | Garden model `name[:tag]` |
| `freeze_encoder` | true | False = fine-tune encoder during RL |
| `fc_hiddens` | [256, 256] | FC trunk on top of latent |

**Notes:**
- `box_radius` is read from the stored `meta.json`, not from `custom_model_config`.
  The env `box_radius` must match the value the garden encoder was trained with.
- With `freeze_encoder: false` the encoder gradients flow and Adam updates all weights.
  Best empirical result from v2 tune used `freeze_encoder: false`.

---

## Registration

```python
# theseo_anysearch/rllib/models/cnn.py

def register_voxel_cnn_models() -> None:
    from ray.rllib.models import ModelCatalog
    ModelCatalog.register_custom_model("voxel_box_2d_cnn",               VoxelBox2DCNN)
    ModelCatalog.register_custom_model("voxel_box_3d_cnn",               VoxelBox3DCNN)
    ModelCatalog.register_custom_model("voxel_hierarchical_box_3d_cnn",  VoxelHierarchicalBox3DCNN)
    ModelCatalog.register_custom_model("voxel_box_3d_cnn_pretrained",    VoxelBox3DCNNPretrained)
```

Registration is lazy — trainers call `register_voxel_cnn_models()` only when
`model_config.custom_model` is set, keeping the `ray` import deferred.

---

## Model Comparison

### Garden encoders

| Model | Spatial hierarchy | BN | Residuals | Decoder |
|---|---|---|---|---|
| `VoxelEncoder3D` | Yes — stride=2 blocks | Yes | Yes (`_ResBlock3D`) | `VoxelDecoder3D` (upsample+conv) |
| `VoxelEncoder2D` | No | No | No | `VoxelDecoder2D` |
| `VoxelEncoderTriplanar` | No | No | No | `VoxelDecoder2D` |

### RL policy models

| Model | Input | Conv type | BN | Pretrained |
|---|---|---|---|---|
| `VoxelBox2DCNN` | local_grid | Conv2d | No | No |
| `VoxelBox3DCNN` | local_grid | Conv3d | No | No |
| `VoxelHierarchicalBox3DCNN` | local_grid (multi-scale) | Conv3d | No | No |
| `VoxelBox3DCNNPretrained` | local_grid | — (uses garden encoder) | Yes (from garden) | Yes |

### Why no BN in RL policy models?

RL training uses small on-policy batches (often 64–256 per update). BatchNorm statistics
computed over such small batches are noisy and can destabilise training. The garden
encoder trains on large fixed datasets (2000+ samples, batch 64–256 across many epochs)
where BN converges reliably.

---

## Parameter Counts (approximate, N=5)

### Garden encoder `VoxelEncoder3D`

| channels | latent_dim | Encoder params |
|---|---|---|
| [32, 64] | 64 | ~55k |
| [32, 64, 64] | 64 | ~170k |
| [64, 128] | 128 | ~215k |
| [64, 128, 128] | 128 | ~850k |

Each `_ResBlock3D` body = two Conv3d layers. Stride-2 blocks also have a 1×1 skip conv.

### RL models

| Model | conv_channels | fc_hiddens | Approx params |
|---|---|---|---|
| `VoxelBox2DCNN` | [32, 64, 64] | [256] | ~75k |
| `VoxelBox3DCNN` | [32, 64, 64] | [256] | ~570k |
| `VoxelBox3DCNNPretrained` | (from garden) | [256, 256] | garden encoder + ~200k |

---

## Source Files

| File | Contents |
|---|---|
| `theseo_anysearch/garden/models/ae.py` | `_ResBlock3D`, `_UpsampleBlock3D`, `_ConvBlock2D`, `VoxelEncoder3D/2D/Triplanar`, `VoxelDecoder3D/2D`, `VoxelAE`, `VoxelVAE`, `build_encoder` |
| `theseo_anysearch/garden/models/mvm.py` | `VoxelMVMEncoder` |
| `theseo_anysearch/garden/encoder.py` | `build_model` — dispatches to AE / VAE / MVM |
| `theseo_anysearch/rllib/models/cnn.py` | `_build_conv2d_stack`, `_build_conv3d_stack`, `_build_fc_stack`, `VoxelBox2DCNN`, `VoxelBox3DCNN`, `VoxelHierarchicalBox3DCNN`, `VoxelBox3DCNNPretrained`, `register_voxel_cnn_models` |
