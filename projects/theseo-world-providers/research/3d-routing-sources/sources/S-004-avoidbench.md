# S-004 — AvoidBench

## Material

- Canonical URL: [AvoidBench repository](https://github.com/tudelft/AvoidBench)
- Source type: Unity/ROS flight benchmark
- Evidence class: primary
- Accessed by originating inventory: 2026-09-13
- Rights: not resolved by the originating inventory

## Relevance and inspected material

AvoidBench publishes indoor and forest trials, seeded map/goal parameters, simulator
interfaces, sensor topics, and native flight metrics. Its runner and published task
contract were reviewed; raw collision-mesh access was not verified.

## Claims used

- It is most defensible as an external benchmark through its native interface.
- A saved point cloud is an observation, not certified solid occupancy.

## Limitations

The setup is operationally heavy, and extracted-voxel tasks would be derived tasks.
Genuine 3D route-choice coverage still requires verification.
