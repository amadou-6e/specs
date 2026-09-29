---
title: Historical CNN models
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

> Historical source; not an authoritative current specification.

# CNN Models for VoxelEnv Box Observation Mode

## Motivation

When `obs_mode: "box"` is active, the agent receives `local_grid` — a flattened binary
3D voxel grid of side N = 2*box_radius+1. The default `fcnet` model concatenates all
observation keys and processes them with fully-connected layers, discarding the spatial
structure of `local_grid`.

Two CNN custom models exploit that spatial structure explicitly:

- **`VoxelBox2DCNN`** — treats the depth axis (z) as channels and applies 2D convolutions
  over the XY plane independently per depth level.
- **`VoxelBox3DCNN`** — treats the full grid as a 3D volume and applies 3D convolutions.

Both models follow the RLlib legacy API stack custom model contract
(`TorchModelV2`) and produce logits + a value estimate from a shared trunk.

---

## Prerequisites

- `obs_mode: "box"` set in the environment config.
- `box_radius` must match between the environment config and `custom_model_config`.
- RLlib legacy API stack: `api_stack(enable_rl_module_and_learner=False, enable_env_runner_and_connector_v2=False)`.
- PyTorch backend: `.framework("torch")`.

---

## Observation Inputs (box mode)

| Key | Shape | Dtype | Description |
|---|---|---|---|
| `steps_remaining` | `(1,)` | float32 | Normalised steps remaining ∈ [0, 1] |
| `voxel_count` | `(1,)` | float32 | Absolute filled voxel count ∈ [0, ∞) |
| `cursor_pos` | `(3,)` | float32 | (x, y, z) normalised to [0, 1] within 32³ grid |
| `local_grid` | `(N³,)` | float32 | Flattened binary 3D grid, N = 2*box_radius+1 |

**Scalar features** (concatenated after CNN): `steps_remaining` (1) + `voxel_count` (1) +
`cursor_pos` (3) = **5 values total**.

**Grid sizes by radius:**

| `box_radius` | N | N³ (flat) |
|---|---|---|
| 2 | 5 | 125 |
| 3 | 7 | 343 |
| 4 | 9 | 729 |

---

## Model 1: `VoxelBox2DCNN`

### Concept

Reshape the flat `(N³,)` grid into `(N, N, N)` and interpret the **z-axis as channels**.
The result is a multi-channel 2D image of shape `(C=N, H=N, W=N)`. Standard `Conv2d`
layers then learn spatial filters over each XY plane, with cross-plane interaction
mediated by the channel mixing in subsequent layers.

This is the more parameter-efficient model and trains faster than the 3D variant.

### Reshape

Storage order in the Rust `box_obs` method is x-outer, y-mid, z-inner:

```
local_grid : (N³,)  — layout: x*N*N + y*N + z
    → reshape(N, N, N)              # (x, y, z)
    → permute(2, 0, 1)              # (z, x, y) = (C=N, H=N, W=N)
    → add batch dim: (B, N, N, N)
```

For N=5: input tensor shape `(B, 5, 5, 5)`.
For N=7: input tensor shape `(B, 7, 7, 7)`.

### Architecture

```
Input: (B, C=N, H=N, W=N)

Conv2d(in_channels=N,  out_channels=32, kernel_size=3, padding=1)  → (B, 32, N, N)
ReLU
Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)  → (B, 64, N, N)
ReLU
Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1)  → (B, 64, N, N)
ReLU
AdaptiveAvgPool2d(output_size=(1, 1))                               → (B, 64, 1, 1)
Flatten                                                              → (B, 64)

Concatenate scalar features (B, 5)                                  → (B, 69)

Linear(69, 256)                                                     → (B, 256)
ReLU
```

**Policy head** (logits):
```
Linear(256, num_outputs)   → (B, num_outputs)
```

**Value head** (separate linear, no activation):
```
Linear(256, 1)             → (B, 1)
```

### Shape table (N=5, default config)

| Layer | Output shape |
|---|---|
| Input (CNN branch) | (B, 5, 5, 5) |
| Conv2d #1 | (B, 32, 5, 5) |
| Conv2d #2 | (B, 64, 5, 5) |
| Conv2d #3 | (B, 64, 5, 5) |
| AdaptiveAvgPool2d | (B, 64, 1, 1) |
| Flatten | (B, 64) |
| Concat scalars | (B, 69) |
| Linear + ReLU | (B, 256) |
| Policy head | (B, num_outputs) |
| Value head | (B, 1) |

The 2D model is **N-invariant at the CNN level** because `AdaptiveAvgPool2d` pools to a
fixed `(1, 1)` output regardless of spatial extent. Only the first `Conv2d` `in_channels`
changes with N.

---

## Model 2: `VoxelBox3DCNN`

### Concept

Reshape the flat `(N³,)` grid into a single-channel 3D volume `(1, N, N, N)` and apply
`Conv3d` layers. This preserves the full 3D spatial structure and allows the network to
learn filters that span all three axes simultaneously.

### Reshape

```
local_grid : (N³,)
    → reshape(N, N, N)              # (x, y, z)
    → unsqueeze(0)                   # (1, N, N, N) = (C=1, D=N, H=N, W=N)
    → add batch dim: (B, 1, N, N, N)
```

For N=5: input tensor shape `(B, 1, 5, 5, 5)`.
For N=7: input tensor shape `(B, 1, 7, 7, 7)`.

### Architecture

```
Input: (B, C=1, D=N, H=N, W=N)

Conv3d(in_channels=1,  out_channels=32, kernel_size=3, padding=1)  → (B, 32, N, N, N)
ReLU
Conv3d(in_channels=32, out_channels=64, kernel_size=3, padding=1)  → (B, 64, N, N, N)
ReLU
Conv3d(in_channels=64, out_channels=64, kernel_size=3, padding=1)  → (B, 64, N, N, N)
ReLU
AdaptiveAvgPool3d(output_size=(1, 1, 1))                            → (B, 64, 1, 1, 1)
Flatten                                                              → (B, 64)

Concatenate scalar features (B, 5)                                  → (B, 69)

Linear(69, 256)                                                     → (B, 256)
ReLU
```

**Policy head** (logits):
```
Linear(256, num_outputs)   → (B, num_outputs)
```

**Value head** (separate linear, no activation):
```
Linear(256, 1)             → (B, 1)
```

---

## Design Notes: Pooling vs Flatten

Both models use `AdaptiveAvgPool` rather than `Flatten → Linear` after the conv stack.

| Property | AdaptiveAvgPool | Flatten → Linear |
|---|---|---|
| N-invariance | Yes — same FC weights for N=5 and N=7 | No — FC input size changes with N |
| Parameter count | Same regardless of N | Grows with N² (2D) or N³ (3D) |
| Recommendation | Default | Only if a fixed N is guaranteed |

`pool_type: "max"` is supported as an alternative (preserves peak activations).

---

## Comparison: 2D vs 3D CNN

| Property | `VoxelBox2DCNN` | `VoxelBox3DCNN` |
|---|---|---|
| Conv type | `torch.nn.Conv2d` | `torch.nn.Conv3d` |
| Input shape to conv | `(B, N, N, N)` | `(B, 1, N, N, N)` |
| Kernel size | `3×3` | `3×3×3` |
| Parameters (conv stack, N=5, channels=[32,64,64]) | ~70k | ~560k |
| Inductive bias | XY spatial; Z-as-channel mixing | Full 3D volumetric |
| Training speed | Faster (2D ops) | Slower (~8× more ops per kernel) |
| Recommended starting point | Yes — lower cost, good baseline | When 3D geometry matters |

---

## Python Class Interface

### Location

```
theseo_anysearch/rllib/models/cnn.py
```

### Class signatures

```python
class VoxelBox2DCNN(TorchModelV2, nn.Module):
    def __init__(
        self,
        obs_space: gym.Space,
        action_space: gym.Space,
        num_outputs: int,
        model_config: dict,
        name: str,
    ) -> None: ...

    def forward(
        self,
        input_dict: dict,
        state: list,
        seq_lens: torch.Tensor,
    ) -> tuple[torch.Tensor, list]: ...
        # Returns (logits of shape (B, num_outputs), state=[])

    def value_function(self) -> torch.Tensor: ...
        # Returns shape (B,)


class VoxelBox3DCNN(TorchModelV2, nn.Module):
    # Same interface as VoxelBox2DCNN; only internal conv layers differ.
    ...
```

### `custom_model_config` keys

| Key | Type | Default | Description |
|---|---|---|---|
| `box_radius` | `int` | `2` | Must match `VoxelEnv` config `box_radius`; N = 2*box_radius+1 |
| `conv_channels` | `list[int]` | `[32, 64, 64]` | Out-channels for each conv layer |
| `fc_hiddens` | `list[int]` | `[256]` | Hidden units for each FC layer before policy/value heads |
| `pool_type` | `str` | `"avg"` | Pooling after conv stack: `"avg"` or `"max"` |

### Internal state

Both classes store `self._value_out: torch.Tensor` (shape `(B, 1)`) in `forward()` so
that `value_function()` returns `self._value_out.squeeze(1)` without recomputing.

---

## Registration

### `register_voxel_cnn_models()` function

```python
# theseo_anysearch/rllib/models/cnn.py

def register_voxel_cnn_models() -> None:
    """Register VoxelBox2DCNN and VoxelBox3DCNN with ModelCatalog."""
    from ray.rllib.models import ModelCatalog
    ModelCatalog.register_custom_model("voxel_box_2d_cnn", VoxelBox2DCNN)
    ModelCatalog.register_custom_model("voxel_box_3d_cnn", VoxelBox3DCNN)
```

### `theseo_anysearch/rllib/models/__init__.py`

Export `register_voxel_cnn_models` so callers can trigger registration explicitly:

```python
from theseo_anysearch.rllib.models.cnn import register_voxel_cnn_models

__all__ = ["register_voxel_cnn_models"]
```

Registration is NOT called automatically on import — trainers call it explicitly before
building the algorithm, keeping the `ray` import deferred.

---

## Trainer Integration

### Detection logic in all trainers

When `model_cfg` carries a `custom_model` key, pass it through to RLlib instead of the
fcnet shorthand:

```python
if model_cfg.custom_model:
    from theseo_anysearch.rllib.models import register_voxel_cnn_models
    register_voxel_cnn_models()
    rllib_model = {
        "custom_model": model_cfg.custom_model,
        "custom_model_config": model_cfg.custom_model_config or {},
    }
else:
    rllib_model = {
        "fcnet_hiddens": model_cfg.hidden_sizes,
        "fcnet_activation": model_cfg.activation,
    }
```

This block replaces the existing `rllib_model = {...}` assignment in `ppo.py`, `sac.py`,
`dqn.py`, and `rainbow.py`. SAC passes `rllib_model` as both `policy_model_config` and
`q_model_config`; CNN custom models apply to both in that context.

### `ModelConfig` extension (`theseo_anysearch/models.py`)

Two new optional fields on `ModelConfig`:

| Field | Type | Default | Description |
|---|---|---|---|
| `custom_model` | `str \| None` | `None` | RLlib model key, e.g. `"voxel_box_3d_cnn"` |
| `custom_model_config` | `dict \| None` | `None` | Passed verbatim to the model `__init__` |

When `custom_model` is `None` the fcnet path is used (backward-compatible). The
`ModelConfig` validator must allow `None` for both fields and not reject the extra
`custom_model_config` dict contents.

---

## YAML Configuration

### Example: 3D CNN with box obs (box_radius=2)

```yaml
env:
  stl_path: usage/geometries/stepped_terrain.stl
  scale: 40.0
  agent_count: 1
  max_steps: 200
  seed: 0
  obs_mode: "box"
  box_radius: 2

training:
  algorithm: ppo
  iterations: 500
  checkpoint_interval: 50

algorithm_config:
  lr: 3.0e-4
  train_batch_size: 4096
  clip_param: 0.2
  num_sgd_iter: 10

model_config:
  custom_model: "voxel_box_3d_cnn"
  custom_model_config:
    box_radius: 2
    conv_channels: [32, 64, 64]
    fc_hiddens: [256]
    pool_type: "avg"
```

### Constraint

`box_radius` in `custom_model_config` must equal `box_radius` in the `env` block.
The model reads N from `custom_model_config["box_radius"]` at `__init__` time. If they
mismatch, `forward()` will raise a shape error on the first batch.

---

## Testing

### Unit tests (no Ray, no Rust)

**File:** `tests/unit/test_cnn_models.py`

Instantiate model classes directly, bypassing RLlib. Call `forward()` with dummy tensors.

#### Test class: `TestVoxelBox2DCNN`

| Test | Assertion |
|---|---|
| `test_forward_output_shape_radius2` | logits shape `(1, 3)` for `num_outputs=3` |
| `test_forward_output_shape_radius3` | logits shape `(1, 3)` for N=7 input |
| `test_value_function_shape` | `value_function()` shape `(1,)` |
| `test_batch_size_2` | logits `(2, 3)`, value `(2,)` |
| `test_logits_are_finite` | no NaN or Inf |
| `test_value_is_finite` | no NaN or Inf |
| `test_custom_channels` | `conv_channels=[16, 32]` — forward succeeds |
| `test_two_fc_hiddens` | `fc_hiddens=[128, 64]` — forward succeeds |
| `test_max_pool_variant` | `pool_type="max"` — forward succeeds |

#### Test class: `TestVoxelBox3DCNN`

Same matrix as above. Additional test:

| Test | Assertion |
|---|---|
| `test_3d_vs_2d_same_output_dim` | both models produce logits `(B, num_outputs)` |

#### Test class: `TestModelRegistration`

| Test | Assertion |
|---|---|
| `test_register_function_runs` | `register_voxel_cnn_models()` does not raise |
| `test_both_keys_registered` | `ModelCatalog._REGISTERED_CONFIGS` contains both keys after registration |

---

### Integration tests (Ray + Rust wheel required)

**File:** `tests/integration/test_cnn_models_ray.py`

Marked `pytestmark = pytest.mark.ray`. Uses session-scoped `ray_session` fixture.
Uses small `conv_channels=[8, 16]` and `fc_hiddens=[64]` to keep tests fast.

| Test | Assertion |
|---|---|
| `test_ppo_2d_cnn_trains_one_iter` | `train()` returns one `TrainResult` with finite `episode_reward_mean` |
| `test_ppo_3d_cnn_trains_one_iter` | same |
| `test_ppo_3d_cnn_radius3_trains` | N=7 grid (box_radius=3); train succeeds |
| `test_cnn_checkpoint_and_restore` | checkpoint after iter 1; restore; train iter 2 without error |

---

## Implementation Order

1. **`theseo_anysearch/models.py`** — add `custom_model: str | None = None` and
   `custom_model_config: dict | None = None` to `ModelConfig`.

2. **`theseo_anysearch/rllib/models/cnn.py`** (new file) — implement `VoxelBox2DCNN`,
   `VoxelBox3DCNN`, and `register_voxel_cnn_models()`.

3. **`theseo_anysearch/rllib/models/__init__.py`** — export `register_voxel_cnn_models`.

4. **All trainers** (`ppo.py`, `sac.py`, `dqn.py`, `rainbow.py`) — replace the
   `rllib_model = {...}` block with the detection logic above.

5. **`tests/unit/test_cnn_models.py`** (new file) — unit tests; no Ray, no Rust.

6. **`tests/integration/test_cnn_models_ray.py`** (new file) — Ray integration tests.

7. **`usage/experiments/train/ppo_3d_cnn.yaml`** (new file) — reference config for users.

---

## Limitations

- **`radial` and `scalar` obs modes**: Both CNN models require `local_grid` in the obs
  dict. Using them with `obs_mode: "radial"` or `obs_mode: "scalar"` will raise
  `KeyError` in `forward()`. The YAML author is responsible for ensuring consistency.
- **SAC Q-network**: SAC passes the same `rllib_model` dict as both `policy_model_config`
  and `q_model_config`. CNN custom models work for the policy; if the Q-network also
  uses a CNN, both will share the same class. A dedicated `VoxelBox3DCNNQModel` is out
  of scope.
- **GPU**: Standard `torch.nn` layers — moves to GPU automatically if `num_gpus=1`.
- **Multi-agent**: `VoxelEnv` is single-agent; no weight-sharing policy changes needed.
