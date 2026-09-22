# Observation and model contract

This page states the invariants connecting environment observations to policy models.
Exact mode schemas are tabulated in [interfaces.md](interfaces.md).

Every observation returned by a wrapper must match its declared Gymnasium/PettingZoo
space in keys, shape, dtype, and bounds. Single-agent numeric arrays are presented as
`float32`; an optional `action_mask` is `int8`. Box observations preserve normalized
voxel kind rather than collapsing occupancy to a boolean. Radial observations preserve
both normalized hit distance and normalized categorical hit kind.

Goal-conditioned modes expose normalized `goal_distance` and a unit
`goal_direction`. Absolute cursor position, remaining time, and `voxel_count` are not
part of the current single-agent policy schema. Hierarchical-box mode concatenates the
configured local boxes without discarding their scale ordering.

Custom CNN models treat `local_grid` as spatial input and concatenate all remaining
non-mask keys as auxiliary input. Spatial features reach the fully connected heads;
the legacy pool setting does not reintroduce global pooling. An action mask is applied
to final logits or action values and must not contaminate the learned encoder input.

Unknown shapes, missing required fields, and action-head cardinality mismatches fail
at construction or inference. Older checkpoints built for removed fields require
retraining or an explicitly versioned adapter.
