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

A planned experiment has one overview, protocol, and source list. An executed
experiment additionally has an execution record, results, and evidence. A replicated
experiment adds a replication record. Experiment results are evidence and do not
promote a subsystem or model without a decision.

Copy [template/](template/README.md) to create an entry. The template itself is not an
experiment entry.
