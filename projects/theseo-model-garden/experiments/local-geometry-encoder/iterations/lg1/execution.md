# LG1 execution

## Resolved execution

- Study: `voxel-encoder-local-geometry-v1-lg1`.
- Registration: `866c88717973894bec6982aea35d459256987379fa315d28c26d419116c43ec6`.
- Protocol revision: `062acdd3964c50c9d9c588734073d340a21ccf2e`.
- Executable revision: `26ab4f18dafd1dcdd16f4e44f2d7db551c2892ec`;
  pre-data publication `fc682d2`.
- Arms/seeds: occupancy and ESDF, seeds 0 and 1; four CUDA encoder runs.
- Data: 96 training, 48 probe, and 48 evaluation geometries; radius 8; 20% masking.
- Hardware/runtime: RTX 3060 Ti, deterministic FP32, PyTorch 2.13.0+cu126,
  206.328 seconds.
- Termination: all four runs and frozen-feature assessments completed.

The machine report records geometry/query identities, artifact hashes, training
curves, controls, intervals, and sufficient statistics. Exact invocation and start/end
timestamps are unavailable in the preserved record; they are not reconstructed.
No deviation from the frozen gates is reported.
