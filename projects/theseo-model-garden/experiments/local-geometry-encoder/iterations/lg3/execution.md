# LG3 execution

## Resolved execution

- Study: `voxel-encoder-local-geometry-v1-lg3`.
- Registration/checkpoint contract:
  `722f883c542eb74af862b68d067d92c6fbaa860f205fbcb14bffee5b3bc055ee`.
- Protocol revision: `082f5b7e8979fe8e9fdf840087fa93df7c430dc2`.
- Executable revision: `21d1ea2c8f03d7def5dc5619d36d1dae5cdf2b9f`;
  publication `b465dc4`.
- Inputs: three frozen LG2 joint encoders and three saved probe artifacts, pinned by
  six file hashes; all loaded states were checked before new data generation.
- Data/work: 48 fresh probe-fitting and 48 fresh evaluation geometries; 48 probe fits,
  24,576 probe updates, zero encoder updates; separate zero-shot diagnostics.
- Hardware/runtime: RTX 3060 Ti, deterministic float32, PyTorch 2.13.0+cu126;
  42.829 seconds.
- Termination: confirmation run completed; no failed family or threshold was changed.

Exact invocation and timestamps are unavailable in the preserved evidence.
