# Model Garden subsystems

Model Garden is decomposed into four owned boundaries rather than represented as an
extension of an Anysearch observation subsystem.

## Contained elements

```text
subsystems/
|-- 1 README.md
|-- 1 template/
`-- 1..* <subsystem>/
```

Each child entry owns one behavioral and contractual boundary. Copy
[template/](template/README.md), rename the copy, and follow its
[SKILL.md](template/SKILL.md). A mature entry contains an overview, contract, design,
and validation map; optional interface, configuration, guide, extension, and migration
pages exist only when their subject is real.

## Current subsystems

| Subsystem | Owned boundary |
| --- | --- |
| [Dataset pipeline](dataset-pipeline/README.md) | Geometry sampling, dataset identity, augmentation, and cached examples |
| [Encoder models](encoder-models/README.md) | Encoder architectures, latent contracts, and model extension points |
| [Pretraining and qualification](pretraining-and-qualification/README.md) | Training recipes, evaluation gates, and promotion evidence |
| [Model registry](model-registry/README.md) | Artifact metadata, versions, storage, discovery, and consumer compatibility |
