---
title: Historical Future voxel observations
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

> Historical source; not an authoritative current specification.

# Voxel Observation Candidates — Future Consideration

Brainstorm of additional observation modes beyond the implemented `scalar`, `box`, and `radial`.
Not yet specced in detail. Review before next observation sprint.

---

## Compact structural (cheap, always useful)

### `face_neighbors`
6 binary values for the 6 cardinal-adjacent cells (+x/-x/+y/-y/+z/-z): is each face-neighbor filled?
- Size: 6 floats ∈ {0, 1}
- Cost: 6 hash-map lookups, no ray marching
- Strictly a subset of `radial` (26 directional rays, axis-aligned only) — 4× smaller
- Rust: trivial, no new data structures
- Best for: any task; extremely cheap sensor

---

## Spatial context (medium cost, high information)

### `coarse_density_map`
Downsample the full 32³ cursor grid to NxNxN (e.g. 4³=64 or 8³=512) by averaging fill fraction per sub-cube.
- Size: 64–512 floats ∈ [0, 1]
- Gives global structure at low resolution without 32³=32768 cost
- Rust: iterate over WorldState HashMap once per step; group by sub-cube
- Best for: tasks requiring awareness of the full volume, not just local neighborhood

### `hierarchical_box`
Box obs at two radii simultaneously (e.g. r=1 tight and r=4 coarse), concatenated.
- Size: (2r1+1)³ + (2r2+1)³ e.g. 3³+9³ = 27+729 = 756 floats
- Small box: precise local state; large box: structural context
- Config: `box_radii: [1, 4]` — list of radii to concatenate
- Rust: call `box_obs` multiple times with different radii
- Best for: structured growth requiring both fine and coarse awareness

---

## Agent self-awareness

### `cursor_trajectory`
Last N cursor positions as normalized (x, y, z) coords.
- Size: N×3 floats (N=4 → 12 floats)
- Helps policy avoid revisiting the same location without external memory
- Rust: ring buffer of last N cursor coords stored in `PyVoxelEnv`
- Config: `trajectory_len: int` (default 4)
- Best for: avoiding repetitive place/remove cycles

### `last_action`
One-hot of the previous action: [+X, -X, +Y, -Y, +Z, -Z].
- Size: 6 floats ∈ {0, 1}
- Lets policy condition on what it just did (e.g. avoid oscillating back and forth)
- Rust: store `last_action: i32` in `PyVoxelEnv`; reset to -1 on reset()
- Best for: reducing oscillation; virtually free

---

## Goal-directed

### `target_distance`
Direction + distance to the nearest unfilled goal cell.
- Size: 4 floats: (dx, dy, dz) normalized unit vector + scalar distance normalized by grid size
- Acts as a compass toward the next target cell
- Rust: iterate over goal cells; find nearest unfilled; O(goal_size) per step
- Best for: navigation-style tasks; compact goal-directed signal

---

## Implementation Priority (suggested order when ready)

1. `face_neighbors` — trivial Rust, no new data; just 6 hash lookups
2. `progress_ratio` + `signed_overshoot` — pure Python, computed from existing obs fields
3. `last_action` — one field in PyVoxelEnv, zero query cost
4. `coarse_density_map` — one Rust method, valuable global context
5. `cursor_trajectory` — ring buffer in PyVoxelEnv
6. `target_distance` — direction + distance to nearest unfilled goal cell; compact goal signal
7. `hierarchical_box` — just multiple box_obs calls; trivial after box is implemented
