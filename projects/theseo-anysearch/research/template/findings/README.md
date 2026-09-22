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

| ID | Finding | Classification | Status | Confidence | Sources |
| --- | --- | --- | --- | --- | --- |
| [F-001](F-001-sparse-hierarchy.md) | Sparse hierarchies avoid allocating uniform regions voxel by voxel | External source claim | Supported | High | [S-001](../sources/S-001-openvdb-overview.md) |

Keep this table synchronized with the records in this directory. Its source links must
match each finding record's **Supporting sources** section.
