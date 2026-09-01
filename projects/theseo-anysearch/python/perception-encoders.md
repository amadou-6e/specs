# Research: Scalable 3D Voxel Perception Encoders

Status: discovery
Owner: amadou-6e
Last reviewed: 2026-09-01
Tracking issue: [specs#5](https://github.com/amadou-6e/specs/issues/5)
Literature revision: [specs#9](https://github.com/amadou-6e/specs/issues/9)
Pretraining methodology: [specs#11](https://github.com/amadou-6e/specs/issues/11)
Governing specification: [Model Garden](model-garden.md)
Direction pilots: [Voxel Encoder Direction-Finding Pilots](perception-encoder-pilots.md)
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

This split is analogous to the task/reward separation in
[successor features](https://arxiv.org/abs/1606.05312), but it is not a successor-
feature model. Successor features are policy-conditioned expectations of future
feature occupancy. This encoder describes current observed geometry and has no policy,
transition model, discount, or future-occupancy semantics. The analogy justifies a
reusable goal-independent boundary; it does not justify calling its latent a successor
feature.

## Evidence from 2D work

| Work | Relevant evidence | Consequence for Theseo |
|---|---|---|
| [ResNet](https://arxiv.org/abs/1512.03385) and [pre-activation ResNet](https://arxiv.org/abs/1603.05027) | Identity shortcuts improve optimization of deep feature hierarchies; pre-activation improves signal propagation. | Use residual stages as the default convolutional building block. |
| [Inception](https://arxiv.org/abs/1409.4842) | Parallel branches capture multiple receptive-field sizes while controlling cost with bottlenecks. | Multi-scale context is useful, but full 3D parallel branches need a cost ablation. |
| [Feature Pyramid Networks](https://arxiv.org/abs/1612.03144) | A hierarchy can expose semantically strong features at several spatial scales without independently processing a full image pyramid. | Preserve scale-specific features and fuse them instead of flattening one huge volume. |
| [EfficientNet](https://arxiv.org/abs/1905.11946) | Depth, width, and resolution should be scaled jointly for a fixed resource budget. | Define capacity families, but do not treat voxel radius as ordinary image resolution. |
| [RegNet](https://arxiv.org/abs/2003.13678) | Simple, regular stage-width rules can outperform heavily customized scaling at similar FLOPs. | Prefer a small explicit model family that can be benchmarked over ad hoc per-radius networks. |
| [Masked Autoencoders](https://arxiv.org/abs/2111.06377) | A lightweight decoder and a heavily masked input can make self-supervised pretraining efficient while the decoder is discarded for transfer. | Use patch masking and disposable pretraining decoders; do not require the policy to load them. |
| [SparK](https://arxiv.org/abs/2301.03580) and [ConvNeXt V2/FCMAE](https://arxiv.org/abs/2301.00808) | ConvNet masked modeling uses a sparse visible-input hierarchy and disposable dense decoder; ordinary dense convolution over filled mask cells does not provide the same isolation or efficiency. | Masked residual candidates require a sparse or explicitly mask-aware encoder path and leakage tests. |
| [Value Iteration Networks](https://arxiv.org/abs/1602.02867) and [Gated Path Planning Networks](https://arxiv.org/abs/1806.06408) | Planning structure can be represented by differentiable convolutional or recurrent computation; the gated variant also reports optimization advantages. | Add planning-aware proxy tasks, but keep iterative planning in the downstream head or planner. |
| [Cognitive Mapping and Planning](https://arxiv.org/abs/1702.03920) and [Neural A*](https://arxiv.org/abs/2009.07476) | Learned spatial maps or guidance fields can be coupled to explicit planning computation. | Preserve dense local features, but keep mapping memory and search outside the reusable observation encoder. |
| [SwAV](https://arxiv.org/abs/2006.09882), [DINO](https://arxiv.org/abs/2104.14294), [DenseCL](https://arxiv.org/abs/2011.09157), [PixPro](https://arxiv.org/abs/2011.10043), and [VADeR](https://arxiv.org/abs/2011.05499) | Cross-view agreement can be learned globally or at corresponding dense locations; dense methods preserve spatial correspondence that global instance objectives can discard. | Align local voxel features over known physical overlap, not just whole-observation vectors. |

The 2D literature supports residual multi-scale encoders and masked pretraining. It
does not establish that a direct 3D translation will be efficient: a 3D kernel and
dense feature map have a much larger memory and compute footprint.

### Evidence for frozen embodied encoders

[R3M](https://arxiv.org/abs/2203.12601),
[MVP](https://arxiv.org/abs/2203.06173),
[PVR](https://arxiv.org/abs/2203.03580),
[VIP](https://arxiv.org/abs/2210.00030), and
[VC-1](https://arxiv.org/abs/2303.18240) provide direct precedent for placing a
pretrained visual encoder behind a frozen boundary and training a small task-specific
module. The evidence is mixed rather than universal: VC-1 reports that no single
representation dominates every embodied task, and
[Hansen et al.](https://arxiv.org/abs/2212.05749) find that in-domain training from
scratch can be competitive and that fine-tuning often closes domain gaps. MVP also
shows that masked pretraining can scale to a large frozen encoder reused by multiple
robot tasks.

For Theseo, frozen transfer is therefore a hypothesis with a strong systems benefit,
not an assumed quality win. Standalone probes must beat raw-grid and random-feature
controls before downstream use, and later comparisons must include frozen, adapted,
fully fine-tuned, and from-scratch variants at equal data and compute.

## Evidence from 3D work

| Family | Representative work | Strength | Risk for this project |
|---|---|---|---|
| Dense voxel CNN | [VoxelNet](https://arxiv.org/abs/1711.06396) | Regular kernels, mature GPU support, and direct voxel feature learning. | Cubic memory makes large radii infeasible. |
| Submanifold sparse CNN | [Submanifold Sparse Convolutional Networks](https://arxiv.org/abs/1706.01307) and [Minkowski convolutions](https://arxiv.org/abs/1904.08755) | Compute follows active coordinates and can support deep residual U-Nets. | Free/unknown semantics and coordinate construction must be designed; performance depends on occupancy density and sparse-kernel support. |
| Octree CNN | [OctNet](https://arxiv.org/abs/1611.05009) and [O-CNN](https://arxiv.org/abs/1712.01537) | Allocates resolution hierarchically and has demonstrated high-resolution 3D analysis. | More complex data structures, batching, kernels, and checkpoint contracts. |
| Octree transformer | [OctFormer](https://arxiv.org/abs/2305.03045) | Uses octree-ordered windows to scale attention with occupied structure. | Octree construction and custom kernels increase implementation and deployment cost. |
| Point encoder | [PointNet](https://arxiv.org/abs/1612.00593) and [KPConv](https://arxiv.org/abs/1904.08889) | Avoids a full grid and handles irregular geometry or density. | Conversion from known-free voxel observations to points can discard occupancy topology or become dense itself. |
| Serialized point transformer | [Point Transformer V3](https://arxiv.org/abs/2312.10035) | Scales point attention using serialization and reports a favorable accuracy/efficiency tradeoff. | Known-free volume still needs an explicit, potentially large tokenization. |
| Tri-plane representation | [TPVFormer](https://arxiv.org/abs/2302.07817) | Represents 3D context on three 2D planes and recovers dense occupancy efficiently. | Projection is learned for semantic occupancy; thin-barrier topology must be independently validated. |
| Implicit field | [Occupancy Networks](https://arxiv.org/abs/1812.03828), [DeepSDF](https://arxiv.org/abs/1901.05103), [Convolutional Occupancy Networks](https://arxiv.org/abs/2003.04618), and [iSDF](https://arxiv.org/abs/2204.02296) | Continuous occupancy or distance queries avoid allocating a dense output grid and support geometric interpolation. | Query cost, local-detail fidelity, and unknown-space semantics can be poor fits for repeated discrete planning queries. |
| Contrastive 3D pretraining | [PointContrast](https://arxiv.org/abs/2007.10985) and [DepthContrast](https://arxiv.org/abs/2101.02691) | Demonstrates transfer of self-supervised 3D features across tasks, datasets, and input formats. | Augmentations must preserve navigation-relevant distinctions and positive-pair construction can dominate results. |
| Masked hierarchical pretraining | [Point-M2AE](https://arxiv.org/abs/2205.14401), [Occupancy-MAE](https://arxiv.org/abs/2206.09900), and [Voxel-MAE](https://arxiv.org/abs/2207.00531) | Multi-scale masking and voxel reconstruction transfer to frozen or fine-tuned 3D tasks; Voxel-MAE explicitly distinguishes empty from non-empty voxels. | Raw occupancy reconstruction can be dominated by empty cells and may not encode connectivity. |
| Distance-field mapping | [Voxblox](https://arxiv.org/abs/1611.03631) and [FIESTA](https://arxiv.org/abs/1903.02144) | Truncated Euclidean signed-distance fields are practical mapping products for collision checking and planning. | A learned approximation must preserve conservative obstacle boundaries and cannot replace exact collision checks. |

No reviewed work directly validates a frozen, goal-independent encoder for Theseo's
voxel path-finding observations over the full radius range. The closest evidence
supports sparse or hierarchical spatial processing, geometry-aware masked objectives,
and physically aligned dense consistency. The checkpoint must first pass standalone
geometric certification; planner outcomes are a separate post-certification test.

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
  deployment inherits a specialized sparse-convolution dependency such as
  [TorchSparse](https://arxiv.org/abs/2204.10319) or `spconv`, whose supported devices,
  operating systems, and serialization behavior must be demonstrated.

### C. Octree residual encoder

Build an adaptive octree, retain fine leaves near obstacle boundaries and the agent,
and pool homogeneous free or occupied regions.

- Best role: long-term candidate for extremely large or irregular environments.
- Advantages: resolution follows geometric complexity rather than bounding volume.
- Risks: greatest implementation and batching cost; requires an octree-aware
  observation and checkpoint schema. OctFormer is the required modern comparison if
  this family advances beyond paper analysis.

### D. Tri-planar or multi-view 2D encoder

Project or slice the voxel volume onto orthogonal planes and reuse a 2D backbone.

- Best role: low-cost baseline and ablation against the existing tri-planar model.
- Advantages: efficient, well-supported, and easy to initialize from 2D work.
- Risks: occlusion and projection collisions remove 3D topology; center slices miss
  obstacles away from the planes. TPVFormer motivates a learned tri-plane baseline,
  but does not remove this topology risk.

### E. Fixed-grid multiresolution residual encoder

Sample several centered 33 x 33 x 33 grids at powers-of-two voxel strides, encode
each grid with shared residual stages, and fuse one token per scale.

- Best role: recommended first scalable candidate.
- Advantages: bounded tensor dimensions, ordinary dense PyTorch operations, exact
  local detail, logarithmic growth in the number of scale levels, and shared weights.
- Risks: coarse cells can hide thin barriers unless aggregation is conservative;
  direct multistride sampling must be added to the environment boundary. Published
  precedent for this exact centered, fixed-grid construction is thin. Its closest
  analogues are feature pyramids, [Multigrid Neural Memory](https://arxiv.org/abs/1906.05948),
  and local/global map hierarchies such as
  [Active Neural SLAM](https://arxiv.org/abs/2004.05155); it remains an engineering
  hypothesis that must win the ablation.

### F. Octahedral-equivariant residual pyramid

Replace ordinary convolutions in candidate E with cube-rotation-equivariant group
convolutions, following [G-CNNs](https://arxiv.org/abs/1602.07576) and
[CubeNet](https://arxiv.org/abs/1804.04458), or benchmark a
continuous alternative derived from
[3D Steerable CNNs](https://arxiv.org/abs/1807.02547).

- Best role: an orientation-robust candidate if augmentation leaves a material
  worst-orientation gap.
- Advantages: encodes right-angle rotation structure by construction and can reduce
  augmentation burden.
- Risks: orientation channels multiply activation cost and complicate checkpoint
  compatibility. The primary discrete group is the 24 proper cube rotations. The 48
  elements of the full octahedral group include reflections and are allowed only when
  input channels, coordinate handedness, and downstream semantics are reflection
  symmetric.

## Residual and Inception decision

### Residual connections: use by default

Use pre-activation residual blocks with identity skips wherever the spatial and
channel shapes agree. Use a projected skip only at a stage transition. This makes
depth ablations practical and keeps the backbone compatible with both dense and
sparse convolutions.

Use [GroupNorm](https://arxiv.org/abs/1803.08494) rather than BatchNorm in the initial
experiments. GroupNorm avoids mutable running statistics and remains well defined for
small batches. Benchmark [LayerNorm](https://arxiv.org/abs/1607.06450) at matched
capacity because token-based and sparse variants may prefer per-sample normalization.
The choice is not certified until the frozen-probe and latency comparison is complete.

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

Weight sharing is the default, but scale conditioning must be stronger than adding a
token after pooling. Benchmark a small FiLM adapter at every residual stage: an MLP
maps `log2(stride)`, requested radius, and valid fraction to per-channel affine
parameters. Compare shared weights, shared weights plus FiLM, bottleneck residual
adapters, and independent per-scale weights in that order.

Process scales sequentially during the first implementation so peak activation
memory is bounded by one 33-cube backbone pass. Batched scale processing is an
optional throughput optimization only after memory measurements exist.

### Scale fusion and output

A two-layer, four-head token transformer or gated attention pool fuses at most six
scale tokens. Missing levels use an attention mask. The encoder returns:

- `global_embedding`: a fixed 256-dimensional vector for the current model-garden
  and RL integration;
- `scale_embeddings`: per-scale vectors before fusion;
- `local_feature_volume`: a stride-1 feature volume matching the finest input side
  (`33 x 33 x 33` by default), formed by an FPN/U-Net-style lightweight lateral
  decoder over that level's stages and returned with its validity mask for coordinate
  and dense heads; and
- metadata containing active strides and validity fractions.

The first model-garden integration may expose only `global_embedding` to an existing
consumer, but the encoder API and checkpoint metadata must define all three outputs.
This prevents the global vector from becoming an irreversible bottleneck for dense
geometry and search heads.

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

1. **Truncated Euclidean signed-distance prediction**: regress signed distance to the
   nearest obstacle, clipped to a declared physical truncation. This is the primary
   dense target because it exposes boundary location, corridor width, and safety
   margin while remaining grounded in practical ESDF mapping work.
2. **Masked semantic occupancy modeling**: mask contiguous, nonempty 3D patches and
   reconstruct occupied/free/unknown classes with a lightweight decoder. Bias patch
   selection toward obstacle boundaries and frontiers, report surface-only loss, and
   compare class-balanced cross-entropy with focal loss so empty space cannot dominate.
   A convolutional encoder must remove hidden coordinates and use sparse visible-cell
   convolutions, or pass the mask-aware dense fallback and hidden-region intervention
   tests in the standalone pretraining plan. Zero-filled dense convolution is invalid.
3. **Physically aligned cross-scale consistency**: transform both views into the same
   world or agent-centered coordinate frame, compute their exact valid overlap, pool
   fine local features into coarse cells with the declared conservative mapping, and
   compare only corresponding valid locations. Use a stop-gradient teacher or VICReg
   variance/covariance terms to prevent collapse. Global latent cosine is diagnostic,
   not the training target, unless the architecture defines its transformation law.

### Planning-aware auxiliary objectives

Generate labels with the exact planner, then discard these auxiliary heads after
pretraining:

- binary reachability between sampled free-cell pairs;
- binned or normalized geodesic distance;
- local path-mask prediction for sampled start/goal pairs; and
- bottleneck or minimum-clearance prediction along the reference path.

These tasks should teach connectivity and obstacle consequences without injecting a
specific runtime goal into the frozen encoder interface.

Learned reachability and distance functions have precedents in
[Semi-parametric Topological Memory](https://arxiv.org/abs/1803.00653),
[Search on the Replay Buffer](https://arxiv.org/abs/1906.05253), and
[Sparse Graphical Memory](https://arxiv.org/abs/2003.06417). Those systems learn
task- or policy-dependent graph relations; Theseo uses their evidence only to motivate
frozen geometric probes and exact offline labels, not to place a policy in the encoder.
[Universal Value Function Approximators](https://arxiv.org/abs/1506.02438) provide
the broader goal-conditioned value precedent, with the same boundary caveat.

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
- shapes, strides, masks, and dtypes for the global embedding, scale embeddings, and
  local feature volume;
- benchmark results for frozen, top-layer, and full fine-tuning.

Loading must fail with a clear compatibility error when observation semantics,
channel order, scale construction, or latent dimension differs. Silent partial loads
are not allowed.

## Evaluation plan

Standalone encoder certification is governed by
[Standalone Voxel Encoder Pretraining](perception-encoder-pretraining.md). That plan
freezes the encoder and excludes all policy, reward, RLlib, and end-to-end navigation
metrics. The downstream measures below apply only after a checkpoint passes the
standalone gates and are not part of model-garden pretraining validation.

### Baselines

Benchmark at least:

1. raw conservative multiscale grids consumed directly by the same capacity-limited
   probe or downstream head, with no learned encoder;
2. the current dense `VoxelEncoder3D` at feasible radii;
3. the existing tri-planar 2D encoder;
4. a plain dense 3D CNN with matched parameters;
5. the dense residual baseline;
6. `voxel_pyramid_resnet_3d`; and
7. one sparse residual candidate if the dependency and sampler are available.

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
Include an exact full-observability planner as an oracle ceiling and a classical
[frontier explorer](https://doi.org/10.1109/CIRA.1997.613851) as a non-learned
partial-observability reference. Report SPL using the definition from
[Anderson et al.](https://arxiv.org/abs/1807.06757). These are post-certification
references only; none enters standalone encoder acceptance.

### Required ablations

- plain blocks versus pre-activation residual blocks;
- residual baseline versus the budgeted two-branch dilation variant;
- single-scale versus multiresolution input;
- per-level sides `17`, `33`, and `65`, with scale count held fixed;
- one, two, four, and all available scales, with per-level side held fixed;
- shared weights versus per-stage FiLM, residual adapters, and per-scale weights;
- GroupNorm versus LayerNorm;
- augmentation-only rotations versus the octahedral-equivariant candidate;
- masked occupancy alone versus clearance and reachability auxiliaries;
- global embedding alone versus scale tokens and the dense local feature volume; and
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
  may be insufficient; compare per-stage FiLM and residual adapters before duplicating
  the backbone.
- **Global vector bottleneck**: one vector fits the current policy contract but may
  discard spatial correspondence needed by search. Scale tokens and the required local
  feature volume preserve an upgrade path.
- **Synthetic-to-real transfer**: box obstacles alone are not adequate. The corpus
  should mix procedural scenes, imported geometry, narrow passages, and held-out
  topology families.
- **Rotation handling**: cube rotations are cheap augmentations, but full SO(3)
  equivariance is not part of the first candidate. Report mean, dispersion, and
  worst-case probe quality over all 24 proper cube rotations. Benchmark discrete
  octahedral equivariance if the worst-case gap exceeds the certification limit.
- **Frozen transfer can fail**: domain mismatch or a sufficiently large in-domain
  training set can make from-scratch or fine-tuned encoders competitive. Publication
  requires raw-grid, random-feature, adapted, and from-scratch controls rather than an
  assumption that freezing is beneficial.
- **Dynamic obstacles**: this review covers static 3D observations. Time should be a
  separate encoder or explicit temporal extension, not an undocumented extra channel.
- **Sparse backend portability**: sparse and octree variants remain candidates until
  their Windows/Linux training and inference support is demonstrated.

## Recommended next experiment

Implement only the data contract, raw-grid control, dense radius-32 residual baseline,
and Tiny fixed-grid pyramid first. Pretrain with truncated ESDF, frontier-biased
masked occupancy, and physically aligned cross-scale consistency; freeze the encoders;
then run the standalone probe plan. Screen per-level sides `17`, `33`, and `65` and
the number of scales before scaling radius or capacity. No planner experiment starts
until one checkpoint passes standalone certification.
