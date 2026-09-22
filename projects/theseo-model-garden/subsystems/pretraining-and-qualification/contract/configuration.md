---
title: Pretraining and qualification configuration
status: draft
kind: subsystem-configuration
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md, interfaces.md]
---

# Pretraining and qualification configuration

This page documents the training and Tune portions of `GardenConfig`. Architecture
fields belong to encoder models, while data collection and augmentation have separate
owners even though all sections share one YAML model.

## Training fields

| Field | Default | Live effect |
|---|---:|---|
| `training.epochs` | `100` | Maximum epoch number. |
| `training.batch_size` | `256` | Batch size; single-radius training drops the last incomplete train batch. |
| `training.lr` | `3e-4` | Adam learning rate. |
| `training.lr_scheduler` | `cosine` | `cosine` uses `CosineAnnealingLR`; `constant` adds no scheduler. |
| `training.early_stop_patience` | `10` | Consecutive non-improving epochs before return. |
| `training.pos_weight_factor` | `0.0` | Positive fixes AE class weight; zero estimates it from data. |
| `training.focal_gamma` | `0.0` | Passed to AE loss; zero requests ordinary weighted BCE behavior. |

Unknown fields are rejected. The schema does not impose positivity on the numeric
fields, so semantic failures can occur after parsing.

## Tune fields

| Field | Default | Live effect |
|---|---:|---|
| `tune.num_samples` | `20` | Ray Tune sample count. |
| `tune.max_concurrent` | `4` | Concurrent trial limit and GPU-fraction denominator. |
| `tune.grace_period` | `5` | Minimum ASHA epochs before pruning. |
| `tune.reduction_factor` | `3` | ASHA reduction factor. |
| `tune.search_space` | `{}` | Nested section/field sampler declarations. |

```yaml
tune:
  num_samples: 12
  max_concurrent: 2
  grace_period: 5
  reduction_factor: 3
  search_space:
    encoder:
      latent_dim: {choice: [32, 64, 128]}
    training:
      lr: {loguniform: [0.0001, 0.001]}
```

Tune keys are not restricted to an allow-list before merging. They must form a valid
`GardenConfig` after sampling or the trial fails validation.

## Identity implications

Training and Tune settings affect learned weights, histories, and selection and must
be recorded for reproducibility. Current `meta.json` records architecture,
augmentation, source data, epoch count, and best loss, but omits optimizer settings,
scheduler, patience, Tune search space, winning sampled configuration, code revision,
dataset hash, and random seeds. Registry metadata is therefore insufficient to
reconstruct a run without its original configuration and Ray artifacts.
