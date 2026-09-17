# Experiments

Experiments is an expandable collection of multi-file research entries. Each entry
answers bounded questions under an explicit protocol and preserves intended design,
actual execution, evidence, results, and replication status separately.

## Contained elements

```text
experiments/
├── 1 README.md
├── 1 template/
└── 0..* <experiment>/ entries
```

A planned experiment has one overview, protocol, and source list. It may own multiple
ordered iterations. Each iteration groups its execution, evidence, results, and any
replication record so separate attempts cannot be mistaken for one aggregate run.
Experiment results are evidence and do not promote a subsystem or model without a
decision.

Copy [template/](template/README.md) to create an entry. The template itself is not an
experiment entry.

## Current experiment entries

| Experiment | Status | Iteration structure |
| --- | --- | --- |
| [Perception encoder R0](perception-encoder-r0/README.md) | Complete migration index | One registered run |
| [Local-geometry encoder study](local-geometry-encoder/README.md) | Complete migration index | LG1, LG2, LG3 |
| [Encoder continuation and context studies](encoder-continuation-and-context/README.md) | Complete migration index | Diagnostics, continuation/transfer, context scaling |
| [Compact perception-encoder campaign](compact-encoder-campaign/README.md) | Complete migration index | Engineering screens, optimization, qualification, collision readout |
| [RL training diversity study](rl-training-diversity/README.md) | Draft; not executed here | No registered iteration |

“Migration index” means the entry organizes existing protocols and evidence without
replacing their pinned identities or creating a new aggregate scientific conclusion.
