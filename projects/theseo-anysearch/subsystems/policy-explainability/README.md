---
title: Policy explainability
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related: []
---

# Policy explainability

This subsystem restores a trained policy, reconstructs an identified decision state,
compares the chosen action with safe alternatives, and measures sensitivity to grouped
feature occlusion. It produces diagnostic evidence about the evaluated policy; it does
not prove causal correctness or explain an abstract network independently of its
checkpoint and preprocessing.

The specification was audited at product revision
`72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`; tests were inspected but not run. A
cursor-field conflict in the generic trace collector remains unresolved, so status is
draft.

Supported policies are saved RLModules for DQN and PPO with discrete voxel actions.
Sources may be a replayed trajectory, a validated environment scenario, or a strictly
validated fictional observation. The pipeline restores, selects states, scores,
group-occludes features, and writes reproducible report artifacts.

## Reading map

- [Contract](contract/README.md)
- [Interfaces](contract/interfaces.md)
- [Request configuration](contract/configuration.md)
- [Design](design/README.md)
- [Guide](guides/README.md)
- [Validation](validation.md)
