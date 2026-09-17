# Finding registry

## Contained elements

```text
findings/
├── 1 README.md
└── 1..* <finding-id>-<concise-name>.md
```

Assign stable identifiers such as `F-001`. Each file owns one bounded finding and
classifies it as an external source claim, directly verified fact, synthesis,
project-specific inference, or recommendation. A finding cites `1..*` characterized
source records and records confidence, applicability, limitations, counterevidence,
and status.

## Index

| ID | Finding | Classification | Status | Confidence |
| --- | --- | --- | --- | --- |
| [F-001](F-001-sparse-hierarchy.md) | Sparse hierarchies avoid allocating uniform regions voxel by voxel | Source claim | Supported | High |
