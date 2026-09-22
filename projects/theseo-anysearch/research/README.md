# Research

Research is an expandable collection of multi-file exploratory topic entries.
Research is informative rather than normative.

## Contained elements

```text
research/
├── 1 README.md
├── 1 SKILL.md
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

## Topic registry

There are currently no active AnySearch-owned research topics. Add a row when a topic
folder is created and remove it only when the topic is moved to another owning project
or archived with an explicit replacement.

| Topic | Question boundary | Status |
| --- | --- | --- |
| _None_ | _No active AnySearch research topic_ | — |

The [template](template/README.md) demonstrates the topic structure; it is not part of
this registry and its OpenVDB example is not an AnySearch research conclusion.

## Ownership redirects

World-source and routing-dataset research is owned by the peer
[Theseo World Providers](../../theseo-world-providers/research/README.md) project.
Anysearch research entries should address questions owned by the consumer runtime,
policy, training, or UI rather than provider acquisition.

Model and perception-encoder research is owned by the peer
[Theseo Model Garden](../../theseo-model-garden/research/README.md) project. Experiments
that evaluate AnySearch training behavior remain experiments rather than becoming
research topics solely because their results are exploratory.
