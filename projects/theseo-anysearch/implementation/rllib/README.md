# RLlib implementation

This fixed partition owns contributor guidance for the RLlib integration and its
local workflows.

## Scope

- Supported RLlib versions and compatibility boundaries.
- Environment, model, and callback registration.
- Observation, action, checkpoint, and policy-mapping integration.
- Training, evaluation, pretraining handoff, and Tune behavior.
- CPU and GPU resource declarations.
- Metrics and diagnostic integration.
- RLlib-specific tests, upgrades, and known framework hazards.

Implementation guidance links to subsystem contracts and must not redefine their
observable behavior.
