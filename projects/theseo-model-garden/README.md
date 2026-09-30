# Theseo Model Garden

Theseo Model Garden is an optional downloadable addition to Theseo. It owns voxel
representation datasets, encoder architectures, pretraining and evaluation, and the
versioned registry of reusable encoder artifacts. Theseo Anysearch consumes published
artifacts through an integration contract but does not own this project's lifecycle.

## Specification map

- [Specification structure](SPECS.md)
- [Architecture](architecture/README.md)
- [Subsystems](subsystems/README.md)
- [Experiments](experiments/README.md)
- [Research](research/README.md)
- [Python implementation rules](implementation/python/README.md)
- [Historical source records](legacy/README.md)

Each category owns its local template and authoring skill where entries are repeatable.
[SPECS.md](SPECS.md) defines their structures, cardinalities, and authority boundaries;
templates from peer projects are examples for those projects, not Model Garden
authoring contracts.

The compact inference slice now resides in
[`theseo-model-garden`](https://github.com/amadou-6e/theseo-model-garden/tree/756e5dd18251ae877ed3277a37f39e16f4b90764).
Training, collection, the legacy registry, and AnySearch's CLI/consumer adapter
remain in `theseo-anysearch`. The [repository-extraction plan](architecture/repository-extraction.md)
pins both sources and distinguishes the delivered slice from the remaining migration.
