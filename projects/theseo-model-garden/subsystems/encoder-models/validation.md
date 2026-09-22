---
title: Encoder-model validation
status: draft
kind: subsystem-validation
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [contract/README.md]
---

# Encoder-model validation

This page maps encoder-model guarantees to checks present at Theseo Anysearch revision
`49fef5f4f9d3fb21325931e1ce1eed89e743cdcc`. Inspection was performed for this
retrospective pass; no implementation test command was run by this pass.

## Present evidence

| Behavior | Evidence | What it proves |
|---|---|---|
| Garden configuration rejects unsupported keys and resolves defaults | `tests/test_garden/test_unit/test_garden_data_config.py` | Parts of the Pydantic configuration surface are exercised. |
| Stored encoder state participates in garden artifact workflows | `tests/test_garden/test_unit/test_garden_store.py` | Store behavior is exercised, but not every architecture's checkpoint compatibility. |
| Architecture and objective treatments have empirical records | `experiments/compact-encoder-campaign/`, `experiments/local-geometry-encoder/`, and `experiments/perception-encoder-r0/` in this specs project | Particular experimental executions produced evidence; they are not general tensor-contract tests. |

## Missing decision-relevant coverage

No direct test under `tests/test_garden/` currently constructs every built-in encoder
and asserts its accepted input and latent output shapes. The following contract points
therefore lack focused regression coverage:

- unknown built-in architecture rejection;
- 3D, depth-as-channel, and tri-planar shape semantics;
- AE, VAE, and MVM output and loss behavior;
- multi-radius behavior for each architecture;
- `extract_encoder()` behavior, especially doubled VAE output width;
- custom import success and malformed-provider failures;
- the difference between custom full-model behavior and historical automatic wrapping;
- invalid radii, empty channels, mask ratios, or transformer head dimensions; and
- the inaccurate return annotation on `load_encoder_from_store()`.

## Recommended validation commands

After focused tests are added, run the smallest suite first:

```powershell
pytest tests/test_garden/test_unit
```

Broader policy-integration validation belongs to the consuming Anysearch subsystem and
should not substitute for direct model-contract tests here.
