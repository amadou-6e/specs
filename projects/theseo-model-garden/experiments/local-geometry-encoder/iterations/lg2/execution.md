# LG2 execution

## Resolved execution

- Study: `voxel-encoder-local-geometry-v1-lg2`.
- Registration: `7bf27e903a90bf1149c75dad80ea9dc88900e0e72e447957cd7ea1b32b393c25`.
- Protocol revision: `ee173bc2a61064386ee8669f77bad9ddf016b709`.
- Executable revision: `b230fab29bec8959267e20b9d3328f907bf901dc`;
  pre-data publication `af472eb`.
- Arms/seeds: occupancy, ESDF, and joint; seeds 0, 1, and 2; nine CUDA runs.
- Work: 9,216 encoder updates and 61,440 probe updates across 120 fits; 192 fresh
  disjoint geometries, radius 8 and 20% masking.
- Hardware/runtime: RTX 3060 Ti, deterministic FP32, PyTorch 2.13.0+cu126;
  444.5 seconds total, 335.858 seconds in encoder loops.
- Termination: every arm completed before assessment.

The explicit preregistered deviation from LG1 made covariance and correlation rank
diagnostic after development-only fixtures demonstrated scale sensitivity. Exact
invocation and wall-clock timestamps are unavailable; no evaluation-guided rerun is
reported.
