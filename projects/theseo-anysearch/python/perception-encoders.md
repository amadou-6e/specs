# Research: Scalable 3D Voxel Perception Encoders

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-01
Tracking issue: [specs#5](https://github.com/amadou-6e/specs/issues/5)
Governing specification: [Model Garden](model-garden.md)
Related implementation issues:
[theseo-anysearch#16](https://github.com/amadou-6e/theseo-anysearch/issues/16),
[theseo-anysearch#17](https://github.com/amadou-6e/theseo-anysearch/issues/17), and
[theseo-anysearch#178](https://github.com/amadou-6e/theseo-anysearch/issues/178)

## Research question

Which perception architecture can be pretrained on 3D voxel observations, stored in
the model garden, frozen during path-finding training, and reused with a small
trainable policy or heuristic head across observation radii from 2 through 512?

This document reviews relevant evidence and defines a candidate to benchmark. It does
not accept that candidate as the production architecture. Acceptance requires the
comparative experiments described below.

## Desired outcome

The encoder should learn goal-independent geometry. A downstream head should combine
the frozen geometry representation with goal, agent, and search state. This split
should:

- reduce the amount of RL or imitation data needed by each planner;
- make one checkpoint useful to multiple path-finding algorithms;
- preserve exact local obstacle detail while adding progressively wider context;
- avoid memory growth proportional to the full dense volume at radius 512;
- expose a stable latent contract that can be versioned in the model garden; and
- support frozen, top-layer, and full fine-tuning without changing observation
  semantics.

## Project constraints

### Radius is a field-of-view parameter

For radius `r`, a dense centered observation has side `2r + 1` and contains
`(2r + 1)^3` cells. Increasing radius is therefore cubic, before any intermediate
activations are allocated.

| Radius | Side | Cells | One FP32 channel | 32 FP16 activation channels |
|---:|---:|---:|---:|---:|
| 2 | 5 | 125 | <0.01 MiB | 0.01 MiB |
| 4 | 9 | 729 | <0.01 MiB | 0.04 MiB |
| 8 | 17 | 4,913 | 0.02 MiB | 0.30 MiB |
| 16 | 33 | 35,937 | 0.14 MiB | 2.19 MiB |
| 32 | 65 | 274,625 | 1.05 MiB | 16.76 MiB |
| 64 | 129 | 2,146,689 | 8.19 MiB | 131.02 MiB |
| 128 | 257 | 16,974,593 | 64.75 MiB | 1,036.05 MiB |
| 256 | 513 | 135,005,697 | 515.01 MiB | 8,240.09 MiB |
| 512 | 1,025 | 1,076,890,625 | 4,108.01 MiB | 65,728.19 MiB |

These figures exclude gradients, optimizer state, later layers, allocator overhead,
and additional input channels. A dense radius-512 tensor is therefore not a viable
input to a normal 3D CNN. Padding every radius to the largest cube has the same
failure mode.

### Occupancy is not just a sparse surface

Path planning distinguishes occupied, traversable, unknown, and out-of-observation
space. A sparse representation that stores only occupied cells can lose the topology
of known free space. Every candidate must preserve these semantics explicitly, either
as dense multiresolution channels or as features on a sparse hierarchy.

### The frozen boundary must be goal-independent

Goal coordinates and planner state should enter the trainable head, not the frozen
perception encoder. Otherwise a checkpoint becomes specific to a goal convention or
policy. Planning-derived labels may supervise pretraining, but inference through the
encoder must require geometry and observation metadata only.

## Evidence from 2D work

| Work | Relevant evidence | Consequence for Theseo |
|---|---|---|
| [ResNet](https://arxiv.org/abs/1512.03385) and [pre-activation ResNet](https://arxiv.org/abs/1603.05027) | Identity shortcuts improve optimization of deep feature hierarchies; pre-activation improves signal propagation. | Use residual stages as the default convolutional building block. |
| [Inception](https://arxiv.org/abs/1409.4842) | Parallel branches capture multiple receptive-field sizes while controlling cost with bottlenecks. | Multi-scale context is useful, but full 3D parallel branches need a cost ablation. |
| [Feature Pyramid Networks](https://arxiv.org/abs/1612.03144) | A hierarchy can expose semantically strong features at several spatial scales without independently processing a full image pyramid. | Preserve scale-specific features and fuse them instead of flattening one huge volume. |
| [EfficientNet](https://arxiv.org/abs/1905.11946) | Depth, width, and resolution should be scaled jointly for a fixed resource budget. | Define capacity families, but do not treat voxel radius as ordinary image resolution. |
| [RegNet](https://arxiv.org/abs/2003.13678) | Simple, regular stage-width rules can outperform heavily customized scaling at similar FLOPs. | Prefer a small explicit model family that can be benchmarked over ad hoc per-radius networks. |
| [Masked Autoencoders](https://arxiv.org/abs/2111.06377) | A lightweight decoder and a heavily masked input can make self-supervised pretraining efficient while the decoder is discarded for transfer. | Use patch masking and disposable pretraining decoders; do not require the policy to load them. |
| [Value Iteration Networks](https://arxiv.org/abs/1602.02867) and [Gated Path Planning Networks](https://arxiv.org/abs/1806.06408) | Planning structure can be represented by differentiable convolutional or recurrent computation; the gated variant also reports optimization advantages. | Add planning-aware proxy tasks, but keep iterative planning in the downstream head or planner. |

The 2D literature supports residual multi-scale encoders and masked pretraining. It
does not establish that a direct 3D translation will be efficient: a 3D kernel and
dense feature map have a much larger memory and compute footprint.

## Evidence from 3D work

| Family | Representative work | Strength | Risk for this project |
|---|---|---|---|
| Dense voxel CNN | [VoxelNet](https://arxiv.org/abs/1711.06396) | Regular kernels, mature GPU support, and direct voxel feature learning. | Cubic memory makes large radii infeasible. |
| Submanifold sparse CNN | [Submanifold Sparse Convolutional Networks](https://arxiv.org/abs/1706.01307) and [Minkowski convolutions](https://arxiv.org/abs/1904.08755) | Compute follows active coordinates and can support deep residual U-Nets. | Free/unknown semantics and coordinate construction must be designed; performance depends on occupancy density and sparse-kernel support. |
| Octree CNN | [OctNet](https://arxiv.org/abs/1611.05009) and [O-CNN](https://arxiv.org/abs/1712.01537) | Allocates resolution hierarchically and has demonstrated high-resolution 3D analysis. | More complex data structures, batching, kernels, and checkpoint contracts. |
| Point encoder | [PointNet](https://arxiv.org/abs/1612.00593) and [KPConv](https://arxiv.org/abs/1904.08889) | Avoids a full grid and handles irregular geometry or density. | Conversion from known-free voxel observations to points can discard occupancy topology or become dense itself. |
| Contrastive 3D pretraining | [PointContrast](https://arxiv.org/abs/2007.10985) and [DepthContrast](https://arxiv.org/abs/2101.02691) | Demonstrates transfer of self-supervised 3D features across tasks, datasets, and input formats. | Augmentations must preserve navigation-relevant distinctions and positive-pair construction can dominate results. |
| Masked voxel pretraining | [Occupancy-MAE](https://arxiv.org/abs/2206.09900) | Predicts masked voxel occupancy and reports transfer to several downstream 3D tasks. | Raw occupancy reconstruction can be dominated by empty cells and may not encode connectivity. |

No reviewed work directly validates a frozen, goal-independent encoder for Theseo's
voxel path-finding observations over the full radius range. The closest evidence
supports sparse or hierarchical spatial processing plus masked or contrastive
pretraining. This is a transfer hypothesis that must be tested on planner outcomes.

## Architecture candidates

### A. Dense residual 3D CNN

Use a pre-activation 3D ResNet on the exact `(2r + 1)^3` observation.

- Best role: correctness baseline for radii 2 through 32.
- Advantages: simplest implementation, deterministic shapes, strong kernel support.
- Rejection condition: do not extend it by padding to radius 512.

### B. Sparse residual 3D CNN

Encode occupied boundaries and explicitly sampled known-free/unknown coordinates with
submanifold sparse residual blocks, downsampling only at stage transitions.

- Best role: high-resolution candidate when active coordinates remain sparse.
- Advantages: preserves exact coordinates without allocating empty feature maps.
- Risks: sparse input policy changes semantics; active count can approach dense count;
  deployment inherits a specialized sparse-convolution dependency.

### C. Octree residual encoder

Build an adaptive octree, retain fine leaves near obstacle boundaries and the agent,
and pool homogeneous free or occupied regions.

- Best role: long-term candidate for extremely large or irregular environments.
- Advantages: resolution follows geometric complexity rather than bounding volume.
- Risks: greatest implementation and batching cost; requires an octree-aware
  observation and checkpoint schema.

### D. Tri-planar or multi-view 2D encoder

Project or slice the voxel volume onto orthogonal planes and reuse a 2D backbone.

- Best role: low-cost baseline and ablation against the existing tri-planar model.
- Advantages: efficient, well-supported, and easy to initialize from 2D work.
- Risks: occlusion and projection collisions remove 3D topology; center slices miss
  obstacles away from the planes.

### E. Fixed-grid multiresolution residual encoder

Sample several centered 33 x 33 x 33 grids at powers-of-two voxel strides, encode
each grid with shared residual stages, and fuse one token per scale.

- Best role: recommended first scalable candidate.
- Advantages: bounded tensor dimensions, ordinary dense PyTorch operations, exact
  local detail, logarithmic growth in the number of scale levels, and shared weights.
- Risks: coarse cells can hide thin barriers unless aggregation is conservative;
  direct multistride sampling must be added to the environment boundary.

## Residual and Inception decision

### Residual connections: use by default

Use pre-activation residual blocks with identity skips wherever the spatial and
channel shapes agree. Use a projected skip only at a stage transition. This makes
depth ablations practical and keeps the backbone compatible with both dense and
sparse convolutions.

Use GroupNorm rather than BatchNorm in the initial experiments. GroupNorm avoids
running-statistics drift between pretraining and small-batch RL inference, and its
behavior is stable when the encoder is frozen. This is a project constraint rather
than a claim from the papers above and must be tested against the current model.

### Full Inception modules: do not make them the default

The motivation for parallel receptive fields is sound, but literal 3D Inception
branches duplicate large activation volumes and `k x k x k` kernels grow cubically.
The proposed observation pyramid already supplies explicit receptive-field scales.

Benchmark one lightweight alternative only after the residual baseline exists:

- replace the middle convolution in selected residual blocks with parallel
  dilation-1 and dilation-2 3 x 3 x 3 branches;
- bottleneck each branch to at most one quarter of the stage width;
- sum projected branch outputs instead of concatenating them; and
- keep the variant only if the downstream gain is significant at matched latency,
  peak memory, and parameter count.

This isolates whether within-scale branching contributes information beyond the
multiresolution input. An unbudgeted Inception stack should be rejected.

## Proposed benchmark architecture

Working name: `voxel_pyramid_resnet_3d`. This is a hypothesis for issue #5, not yet
an accepted model-garden architecture.

### Input contract

Each level is a centered 33 x 33 x 33 tensor with these logical channels:

1. `occupied`: at least one occupied source voxel contributes to the cell;
2. `known_free`: every represented source voxel is observed and free;
3. `unknown`: any represented source region is outside observation or unknown; and
4. `valid`: the cell lies inside the requested radius and environment bounds.

The exact channel encoding may be packed in storage, but it must be expanded without
ambiguity before the encoder. Occupied and unknown must never be silently converted
to free.

### Scale construction

Use voxel strides `1, 2, 4, 8, 16, 32`. A 33-cell side covers plus or minus 16 cells,
so the final level reaches radius 512. For requested radius `r`, expose levels through
the smallest stride `s` where `16s >= r`; mask cells beyond `r` with `valid = 0`.

| Requested radius | Active strides | Widest covered radius |
|---:|---|---:|
| 2, 4, 8, 16 | 1 | 16 |
| 32 | 1, 2 | 32 |
| 64 | 1, 2, 4 | 64 |
| 128 | 1, 2, 4, 8 | 128 |
| 256 | 1, 2, 4, 8, 16 | 256 |
| 512 | 1, 2, 4, 8, 16, 32 | 512 |

This supports the power-of-two presets directly. Arbitrary even radii up to 512 use
the same next-covering level and a validity mask; they do not require new weights.
At radius 512 the six input grids contain 215,622 cells in total, versus
1,076,890,625 cells in one dense cube, a roughly 4,994-fold reduction before
channels. This comparison does not include the cost of constructing the pyramid.

Coarsening must be conservative:

- occupancy uses `any`/max aggregation;
- known-free uses `all`/min aggregation;
- unknown and out-of-bounds propagate explicitly; and
- no thin occupied barrier may disappear because its bin contains mostly free space.

The Rust/Python observation boundary should sample or aggregate each stride directly.
It must not allocate the dense radius-512 cube and downsample it afterward.

### Shared per-scale backbone

The base candidate uses one shared pre-activation 3D ResNet:

| Stage | Width | Blocks | First-block stride |
|---|---:|---:|---:|
| Stem | 24 | 1 convolution | 1 |
| 1 | 24 | 2 | 1 |
| 2 | 48 | 2 | 2 |
| 3 | 96 | 3 | 2 |
| 4 | 192 | 2 | 2 |

Each block uses GroupNorm, SiLU, 3 x 3 x 3 convolutions, and an identity or projected
skip. Global average and max pooling produce one feature vector per scale. A learned
embedding of `log2(stride)`, requested radius, and valid fraction is added to each
scale token.

Process scales sequentially during the first implementation so peak activation
memory is bounded by one 33-cube backbone pass. Batched scale processing is an
optional throughput optimization only after memory measurements exist.

### Scale fusion and output

A two-layer, four-head token transformer or gated attention pool fuses at most six
scale tokens. Missing levels use an attention mask. The encoder returns:

- `global_embedding`: a fixed 256-dimensional vector for the current model-garden
  and RL integration;
- `scale_embeddings`: optional per-scale vectors for spatial or search-specific
  heads; and
- metadata containing active strides and validity fractions.

The first implementation may expose only `global_embedding` to maintain the existing
garden contract, but checkpoints must record whether scale tokens are available.

### Capacity families

Radius changes field of view by adding levels; it does not automatically increase
parameter count. Capacity changes through explicit families:

| Family | Stem width | Blocks per stage | Global dimension | Intended use |
|---|---:|---|---:|---|
| Tiny | 16 | 1, 1, 2, 1 | 192 | CPU and high-throughput baseline |
| Base | 24 | 2, 2, 3, 2 | 256 | default experiment |
| Large | 32 | 2, 3, 4, 3 | 384 | data-scaling experiment |

Stage widths double at downsampling transitions. A family can be promoted only when
its frozen downstream quality improves at a declared latency and memory budget.
EfficientNet-style compound scaling is an experiment over width, depth, and the fixed
per-level grid size; it must not mean constructing the full dense radius cube.

## Pretraining objectives

### Required geometric objectives

1. **Masked occupancy modeling**: mask contiguous 3D patches, encode visible input,
   and reconstruct occupied/free/unknown classes with a lightweight decoder. Compute
   loss on masked valid cells and class-balance it so empty space cannot dominate.
2. **Truncated clearance or signed-distance prediction**: regress distance to the
   nearest obstacle up to a declared truncation. This makes corridor width and local
   safety margin observable in the latent space.
3. **Cross-scale consistency**: require compatible representations for the same
   physical region observed at adjacent strides while retaining a scale embedding.

### Planning-aware auxiliary objectives

Generate labels with the exact planner, then discard these auxiliary heads after
pretraining:

- binary reachability between sampled free-cell pairs;
- binned or normalized geodesic distance;
- local path-mask prediction for sampled start/goal pairs; and
- bottleneck or minimum-clearance prediction along the reference path.

These tasks should teach connectivity and obstacle consequences without injecting a
specific runtime goal into the frozen encoder interface.

### Optional contrastive objective

Use two views of the same physical neighborhood with rotations, translations within
the validity region, masking, and observation noise. Positive pairs must preserve
occupancy topology. Do not apply elastic warps, cutouts, or aggressive pooling that
can open or close a corridor unless the label is changed accordingly.

Start with geometric objectives plus one reachability head. Add contrastive loss only
as an ablation because large negative batches and augmentation design add complexity.

## Frozen-head integration

The runtime policy path is:

```text
multiresolution voxel observation -> frozen geometry encoder -> geometry embedding
goal + agent/search state -------------------------------> trainable planner head
```

For `finetune_mode: frozen`:

- load the encoder in evaluation mode;
- set all encoder parameters to `requires_grad = false`;
- compute the encoder path under `no_grad`;
- keep normalization behavior independent of mutable running statistics; and
- train only the goal/state projection, fusion, policy, value, heuristic, or search
  head.

The head must receive the requested radius and active-stride mask, either through the
encoder metadata or the encoded scale embeddings. It must not infer radius from tensor
padding.

## Model-garden checkpoint contract

Add these fields to metadata before publishing this architecture:

- architecture name and semantic version;
- capacity family, stage widths, stage depths, and latent dimension;
- logical input channel names and unknown/out-of-bounds policy;
- per-level side length, supported strides, and maximum radius;
- aggregation rule for every logical channel;
- normalization and activation types;
- pretraining objectives and weights;
- geometry corpus, split, sampler version, and dataset hash;
- coordinate frame, rotation augmentation, and voxel-size conventions;
- whether optional scale embeddings are stored; and
- benchmark results for frozen, top-layer, and full fine-tuning.

Loading must fail with a clear compatibility error when observation semantics,
channel order, scale construction, or latent dimension differs. Silent partial loads
are not allowed.

## Evaluation plan

### Baselines

Benchmark at least:

1. the current dense `VoxelEncoder3D` at feasible radii;
2. the existing tri-planar 2D encoder;
3. a plain dense 3D CNN with matched parameters;
4. the dense residual baseline;
5. `voxel_pyramid_resnet_3d`; and
6. one sparse residual candidate if the dependency and sampler are available.

The octree candidate enters only after the fixed-grid pyramid has established that
large-radius context improves planner outcomes.

### Geometry probes

With the encoder frozen, train small linear or two-layer heads for:

- masked occupancy class accuracy and occupied-class IoU;
- clearance mean absolute error;
- reachability AUROC and balanced accuracy;
- geodesic-distance error; and
- local path-mask precision, recall, and IoU.

Probe data must include held-out geometry families, rotations, obstacle densities,
and radii. Report per-radius results rather than only an aggregate.

### Downstream planner measures

At a fixed training budget and over at least three seeds, report:

- success rate and collision rate;
- path-length ratio or SPL against the reference planner;
- minimum path clearance;
- environment steps and wall time to a declared success threshold;
- inference p50/p95 latency at batch size 1;
- peak CPU and accelerator memory; and
- performance on unseen radii and geometry distributions.

Compare random initialization, frozen pretraining, top-layer fine-tuning, and full
fine-tuning. A reconstruction score alone is not sufficient evidence for adoption.

### Required ablations

- plain blocks versus pre-activation residual blocks;
- residual baseline versus the budgeted two-branch dilation variant;
- single-scale versus multiresolution input;
- shared versus per-scale backbone weights;
- masked occupancy alone versus clearance and reachability auxiliaries;
- global embedding alone versus optional scale tokens; and
- max radius 32, 64, 128, 256, and 512 at matched local resolution.

### Acceptance gates

The candidate can move from discovery to review only when:

- no code path constructs a dense cube larger than 33 per pyramid level;
- radius-512 inference completes inside the declared deployment memory budget;
- conservative aggregation passes thin-wall and narrow-corridor tests;
- frozen transfer improves planner sample efficiency or final quality over the
  current encoder on held-out geometry without an unacceptable latency regression;
- results include variance across seeds and per-radius breakdowns; and
- checkpoint compatibility failures are tested.

The implementation issue must set numerical memory, latency, and quality thresholds
for the target hardware before the benchmark begins.

## Risks and open decisions

- **Information loss at coarse scales**: conservative occupancy protects barriers but
  can make coarse space look overly blocked. Clearance and occupancy-fraction channels
  are candidate additions, subject to semantics tests.
- **Shared weights across strides**: weight sharing controls parameters but local
  patterns can have different meaning at different physical scales. Scale embeddings
  may be insufficient; compare per-stage adapters before duplicating the backbone.
- **Global vector bottleneck**: one vector fits the current policy contract but may
  discard spatial correspondence needed by search. Optional scale tokens preserve an
  upgrade path.
- **Synthetic-to-real transfer**: box obstacles alone are not adequate. The corpus
  should mix procedural scenes, imported geometry, narrow passages, and held-out
  topology families.
- **Rotation handling**: cube rotations are cheap augmentations, but full SO(3)
  equivariance is not part of the first candidate. Measure orientation sensitivity.
- **Dynamic obstacles**: this review covers static 3D observations. Time should be a
  separate encoder or explicit temporal extension, not an undocumented extra channel.
- **Sparse backend portability**: sparse and octree variants remain candidates until
  their Windows/Linux training and inference support is demonstrated.

## Recommended next experiment

Implement only the data contract, dense radius-32 residual baseline, and Tiny/Base
fixed-grid pyramid first. Pretrain with masked occupancy, clearance, and reachability;
freeze the encoders; then compare identical planner heads on held-out geometries at
radii 16, 32, 64, 128, 256, and 512. This experiment determines whether wider context
and the frozen boundary help before investing in sparse kernels, octrees, or a larger
capacity family.
