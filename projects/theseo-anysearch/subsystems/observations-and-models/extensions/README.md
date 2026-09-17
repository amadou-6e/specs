# Observation and model extensions

## Contained elements

```text
extensions/
├── 1 README.md
└── 0..* <extension>/
```

These extensions optionally augment the observations/models subsystem through the
points defined by [the extension contract](../contract/extensions.md). They are not
peer subsystems and must leave the base subsystem usable when absent.

## Current extensions

- [Model Garden](model-garden/README.md)
