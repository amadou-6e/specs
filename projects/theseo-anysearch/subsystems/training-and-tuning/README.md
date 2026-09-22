---
title: Training and tuning orchestration
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Training and tuning orchestration

This subsystem turns a resolved experiment into a bounded RLlib training run or Tune
search. It owns algorithm construction, staged execution, deterministic evaluation,
resource declarations, checkpoints, pretraining handoff, stopping, and run artifacts.
It does not own environment dynamics, model internals, metric meaning, or scientific
conclusions.

The specification was audited at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; tests were inspected but not executed.
RLlib version compatibility and Ray-backed integration remain explicit boundaries.

The normal lifecycle is: resolve configuration, build registered environment/model/
algorithm, optionally restore or pretrain, repeat training and deterministic
evaluation, normalize results, write artifacts/checkpoints, and stop at a configured
gate or hard iteration maximum. Tune wraps that lifecycle in validated sampling and
resource-isolated trials.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Configuration](contract/configuration.md)
- [Extension points](contract/extensions.md)
- [Design](design/README.md)
- [Guide](guides/README.md)
- [Validation](validation.md)
