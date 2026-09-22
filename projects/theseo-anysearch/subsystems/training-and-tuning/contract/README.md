# Training and tuning contract

This page defines execution guarantees shared by training and tuning. Configuration
details are separated into [configuration.md](configuration.md).

`training.iterations` is a hard maximum, not a stage duration estimate. Each completed
iteration trains, evaluates when scheduled, normalizes metrics, and persists required
state. Missing upstream metrics are omitted rather than logged as zero.

Evaluation disables exploration, uses fresh environments and a stable seed sequence,
synchronizes policy weights, and sorts seed-labelled results before aggregation.
Parallel evaluation may report a snapshot one learner update behind; checkpoint
selection and comparisons must account for that lag.

Staged training applies ordered tasks whose overrides are recursively merged relative
to the base experiment. Algorithm, model, and policy-contract fields are immutable
across stages. Every completion-condition tree requires a finite cap. A transition may
rebuild state while transferring weights or preserve an eligible checkpoint. Replay-
preserving transitions are rejected for replay-based algorithms rather than pretending
their replay state is compatible.

Tune samples only validated aliases and configuration fields, assigns declared Ray
resources, and persists trial histories, status, and checkpoints. Trials finish as
completed, pruned, or failed; failure is never recast as a low metric. Stop criteria
may use iteration, environment steps, wall time, or success conditions.

Pretraining cache reuse requires identity equivalence for architecture and all model
inputs. Heterogeneous models do not share an incompatible pretrained policy.
