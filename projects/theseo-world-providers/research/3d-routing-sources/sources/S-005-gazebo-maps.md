# S-005 — Gazebo maps

## Material

- Canonical URL: [Gazebo maps repository](https://github.com/engcang/gazebo_maps)
- Source type: simulator scene assets
- Evidence class: primary
- Accessed by originating inventory: 2026-09-13
- Rights: audit required

## Relevance and inspected material

The `3d_maze.tar.xz` archive was inspected and contains Gazebo world/model files with
box collision geometry. The inspected maze is large, open-topped, and has no packaged
route queries.

## Claims used

- The source supplies geometry but not a ready routing task.
- A roof, endpoint pair, or vehicle radius defines a separately identified derived
  world or task.

## Limitations

The vertical tunnel was not inspected. Connectivity, clearance, overflight prevention,
and whether tasks require vertical motion must be independently verified.

## Related findings

- [F-001](../findings/F-001-geometry-is-not-a-task.md)
