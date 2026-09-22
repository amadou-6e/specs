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
| [RL training diversity study](rl-training-diversity/README.md) | `planned`; historical design imported, no registered execution | No registered iteration |

“Migration index” means the entry organizes existing protocols and evidence without
replacing their pinned identities or creating a new aggregate scientific conclusion.

Encoder-pretraining experiments are owned by the peer
[Theseo Model Garden](../../theseo-model-garden/experiments/README.md) project.

## Maintenance

Apply [SKILL.md](SKILL.md) when creating, reconstructing, or revising an experiment.
The skill requires protocol, execution, evidence, and results to remain separate and
for incomplete historical records to disclose their gaps. Do not infer an experiment
from the existence of an example configuration or implementation feature alone.
