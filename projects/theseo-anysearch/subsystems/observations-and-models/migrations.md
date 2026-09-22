# Observation schema migration

This page records active compatibility consequences of the current observation
contract. It is not a promise to adapt old checkpoints automatically.

Current single-agent observations removed absolute cursor/time/count fields, changed
goal direction to a unit vector, and preserve voxel kinds in box observations. These
changes alter model inputs and invalidate checkpoints trained against older schemas.
Affected models must be retrained or loaded through an explicitly versioned adapter.

New configuration belongs under `env.observation`. Legacy flat aliases remain readable
during migration, but callers must not specify both nested and legacy forms because
the intended authority would be ambiguous.
