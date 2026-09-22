# Protocol status

This is a retrospective protocol scaffold, not a frozen protocol. The imported
[RL training diversity](imported-protocol.md) document was already present before this
experiment entry was reconstructed, and the repository subsequently implemented some
of its mechanisms. No evidence shows that decision rules were fixed before results
were observed. Consequently, no execution may cite this file as a governing frozen
protocol in its current form.

## Apparent design preserved from the imported source

The historical design varies three broad factors:

- geometry identity through a pre-generated geometry pool;
- voxel scale through fixed or sampled scale settings; and
- reset-time obstacle augmentation through pasted boxes.

It proposes fixed-geometry behavior as backward compatibility, but it does not define
an experimental control, factorial comparison, held-out population, or attribution
method. Its YAML snippets and implementation checklist are design examples, not
registered treatments or evidence of execution.

## Required protocol before activation

Before this study can move from `planned` to `running`, a prospective revision must
pin all of the following before decision-bearing observations:

1. bounded research questions and falsifiable hypotheses;
2. treatments, controls, baselines, and permitted combinations of the three factors;
3. the unit of generalization and the train, validation, and test selection policy
   for worlds, geometry identities, routes, and tasks; any required disjointness,
   permitted overlap, labels, and leakage checks must be stated explicitly rather
   than assuming that a world may appear in only one split;
4. seeds, sample sizes, algorithms, model architecture, initialization, checkpoint
   handling, and training budget;
5. geometry-pool identities, generation settings, augmentation feasibility policy,
   and evaluation-world identities;
6. primary and secondary metrics, aggregation, uncertainty analysis, thresholds, and
   evaluation points;
7. stop conditions, decision gates, permitted adaptations, and forbidden post-hoc
   changes;
8. hardware, dependency, code, configuration, and governing-spec revisions; and
9. threats to validity, especially difficulty imbalance, correlated variants from one
   source mesh, infeasible pasted obstacles, repeated routes within a shared world,
   and compute confounding.

The split policy must match the claim being tested. For example, a route-generalization
claim may permit one world in several populations when their task identities or route
labels are distinct, whereas a world-generalization claim requires held-out world
identities. The protocol must not silently strengthen one claim into the other.

Any execution must receive its own ordered iteration with an execution record and
evidence manifest. Later protocol changes must authorize a new iteration rather than
rewriting an earlier execution.

## Current disposition

Unevaluable. There are no registered observations against which to apply a gate and
no preregistered gate to apply.
