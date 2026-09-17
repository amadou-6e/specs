# Research

Research is an expandable collection of multi-file exploratory topic entries.
Research is informative rather than normative.

## Contained elements

```text
research/
├── 1 README.md
├── 1 template/
└── 0..* <topic>/ entries
```

Each topic owns one bounded investigation, a reproducible method, `1..*` individually
characterized sources, and `1..*` individually reviewable findings. The topic overview
synthesizes those findings without hiding attribution, uncertainty, disagreement, or
limitations. Research may motivate experiments or decisions and may inform subsystem
specifications.

Copy [template/](template/README.md) to create an entry. The template itself is not a
research entry. Existing root-level research documents predate this structure and
should be migrated separately rather than rewritten incidentally.

## Current topics

- [3D routing environment and asset sources](3d-routing-sources/README.md)
- [Medical geometry and centerline datasets](medical-routing-datasets/README.md)

These initial topics structurally migrate source characterizations from existing
research documents. Their linked legacy syntheses remain in place until findings are
fully migrated and reviewed.
