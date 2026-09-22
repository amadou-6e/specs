---
title: Train and tune an encoder
status: draft
kind: subsystem-guide
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [../README.md, ../contract/configuration.md]
---

# Train and tune an encoder

This guide explains the supported local workflows for producing an experimental
encoder artifact. It assumes Theseo AnySearch and model-garden dependencies are
installed, referenced data sources are available, and the reader understands that
completion does not establish navigation qualification.

## Train a configured model

Use a YAML path, registered configuration name, or built-in preset:

```text
anysearch garden train r2 --tag v1
anysearch garden train path/to/garden.yaml --output-dir runtime/garden --device auto
```

The expected result is `model.pt`, `encoder.pt`, `meta.json`, and `loss_curve.json`
under the selected garden directory. Add `--resume` only when the model family's
`_checkpoint.pt` belongs to this exact configuration; the checkpoint is not tag-scoped
and compatibility is not validated.

Preserve the original resolved YAML and execution environment outside the current
registry metadata if reproduction matters. The printed best validation loss is not a
qualification result and may not describe the final saved weights.

## Tune hyperparameters

Add a `tune` block described in [configuration](../contract/configuration.md), then run:

```text
anysearch garden tune path/to/garden.yaml --output-dir runtime/garden/tune
```

By default, Tune retrains the winning sampled configuration and saves that fresh run.
Use `--no-save-best` to retain only Ray trial results. The saved retraining is not
guaranteed to reproduce the winning trial because seeds are not locked or compared.

## Conduct qualification

There is no general qualification command. Use an experiment entry with a frozen
protocol, run its probes and controls, and record evidence under that experiment. The
historical [compact encoder campaign](../../../experiments/compact-encoder-campaign/README.md)
shows the distinction between engineering screens, collision readout, optimization,
and bounded qualification. A checkpoint remains experimental unless a governing
contract and recorded evidence explicitly establish a stronger status.
