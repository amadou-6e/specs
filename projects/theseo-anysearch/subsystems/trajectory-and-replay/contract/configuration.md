# Trajectory and replay configuration

This page describes settings that determine what gets recorded and viewed without
turning viewer-only controls into experiment YAML requirements.

Training configuration controls trajectory cadence and whether the best-so-far
episode is retained. Reporting code in
`theseo_anysearch/rllib/trainer/reporting/trajectories.py` uses those settings when
choosing snapshot iterations and final artifacts.

Replay selection and viewer controls are command/UI state. Camera, playback,
regional-view, overview, and diagnostic-display choices do not redefine the training
environment or trajectory identity. A world reference, overlay sequence, and ordered
steps do affect replay identity and correctness.
