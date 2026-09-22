# Consolidated sources

## Historical design source

- [RL training diversity](imported-protocol.md): unmodified imported design and
  implementation checklist. It entered the specs repository in commit
  `0bfcdd1f0233320338351252680a7e69f1726241` (2026-09-01) and currently hashes as Git
  blob `eaa966bd9b33d4ea4caac1d9e25988c2ed69d6a8`. It is evidence of proposed design,
  not of a frozen protocol or executed experiment.

## Current contracts

- [Training and tuning subsystem](../../subsystems/training-and-tuning/README.md):
  current execution boundary. It can constrain a future run but does not establish
  that a historical run occurred.
- [World-provider subsystem](../../../theseo-world-providers/subsystems/world-providers/README.md):
  external and generated world-identity boundary. This belongs to the optional peer
  provider package and does not by itself define the study's train/evaluation split.

## Implementation evidence

- Theseo AnySearch commit `2ce103bde6b41fdee6063d1b4ff068043bece012`
  (2026-04-06, `Model garden and geometry pools`): earliest repository commit found
  for `GeometryPool`, extraction, and diverse-training example paths. It shows that
  design mechanisms entered implementation; it is not run evidence.
- Theseo AnySearch `origin/develop` at
  `72a413a2f10ba1aeb9430c8e3412bffc30d1e68c` was inspected retrospectively. Relevant
  implementation is characterized below. These mutable paths are discovery aids; a
  future iteration must pin the exact files and content identities it uses.

| Imported design mechanism | Current implementation evidence | Boundary or limitation |
|---|---|---|
| Offline geometry-pool extraction | `theseo_anysearch/cli/commands/extract.py`; `usage/extract/highres.yaml`; `usage/extract/lowres.yaml` | Confirms an extractor and examples exist, not that the historical commands ran or produced a retained pool. |
| Reset-time pool sampling | `theseo_anysearch/environments/geometry_pool.py`; `theseo_anysearch/environments/gymnasium/voxel_env.py`; `theseo_anysearch/environments/pettingzoo/multi_voxel_env.py` | Both environment paths sample pool entries. This does not establish balanced sampling, a study split, or generalization. |
| Reset-time box augmentation | `paste_boxes()` in `theseo_anysearch/environments/geometry_pool.py`, called by both environment reset paths | The operation changes occupancy. Its effect on task difficulty is uncontrolled unless validation and a prospective sampling policy are enabled. |
| Feasibility and difficulty validation | `GeometryValidationConfig` in `theseo_anysearch/settings/environment/geometry.py`; single-agent reset validation in `theseo_anysearch/environments/gymnasium/voxel_env.py`; integration coverage in `tests/test_geometry/test_integration/test_geometry_feasibility.py` | Current single-agent validation can reject invalid or infeasible samples and report descriptors. The multi-agent reset path does not apply the same validation loop, so parity must not be assumed. |
| Runtime STL scale sampling | `scale_range` handling in the single- and multi-agent reset paths | Applies to configured STL input, not to an already voxelized pool entry. It must be treated as a separate factor from pool sampling. |
| Example PPO treatment and ASHA search | `usage/experiments/train/ppo_diverse.yaml`; `usage/experiments/tune/ppo_diverse_asha.yaml` | These are executable examples, not a frozen experiment protocol or evidence that a run completed. |

The imported checklist is intentionally preserved unchanged even where later code now
implements an item or uses a different configuration shape. This table records the
retrospective comparison without rewriting the historical source.

## Missing evidence

No run identifier, command transcript, seed list, environment manifest, checkpoint,
TensorBoard or MLflow record, evaluation report, hardware record, or artifact hash is
registered for this study. No literature source or prior comparative experiment is
cited by the imported design. Until such evidence is registered under an iteration,
results and replication claims are unavailable.
