# Model Garden experiments

These experiments evaluate encoder architecture, training, retention, transfer, and
qualification. Their protocols and evidence belong to Model Garden even when the
implementation used a checkout of the Theseo Anysearch repository.

## Contained elements

```text
experiments/
|-- 1 README.md
|-- 1 SKILL.md
|-- 1 template/
`-- 0..* <experiment>/
```

Each experiment is an independently owned multi-file entry with one frozen protocol,
one consolidated source list, and zero or more ordered iterations. Copy
[template/](template/README.md), rename the copy, and apply [SKILL.md](SKILL.md).
Do not leave an experiment protocol in `legacy/` merely because its first version was
written there; retain the historical file as evidence and put the governing structured
record here.

## Current experiments

- [Perception encoder R0](perception-encoder-r0/README.md)
- [Local geometry encoder](local-geometry-encoder/README.md)
- [Compact encoder campaign](compact-encoder-campaign/README.md)
- [Encoder continuation and context](encoder-continuation-and-context/README.md)
