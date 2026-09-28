# RLlib implementation

## Contained elements

```text
implementation/rllib/
├── 1 README.md
└── 0..* RLlib implementation documents
```

Each additional document owns one bounded contributor rule or local workflow. This
partition is fixed; documents do not create nested implementation categories.

This fixed partition owns contributor guidance for the RLlib integration and its
local workflows.

## Scope

- Supported RLlib versions and compatibility boundaries.
- Environment, model, and callback registration.
- Observation, action, checkpoint, and policy-mapping integration.
- RLlib trainer, evaluation, pretraining handoff, and Tune API adaptation.
- RLlib EnvRunner and vectorization configuration APIs; Ray worker execution,
  scheduling, and resource effects belong under [Ray](../ray/README.md).
- Metrics and diagnostic integration.
- RLlib-specific tests, upgrades, and known framework hazards.

Implementation guidance links to subsystem contracts and must not redefine their
observable behavior.

## Investigation queue

The following draft pages are investigation plans, not accepted implementation
rules. Each must be resolved against a pinned product revision and test evidence
before its plan is replaced with contributor guidance:

- [RLlib integration boundaries](integration.md)
- [Training development workflow](training-workflow.md)
- [RLlib checkpoint and policy-scoring adapter](explain-backend.md)

The former `legacy-module-spec.md` has moved to the [legacy archive](../../legacy/rllib-module-spec.md).
Its abstract-trainer and algorithm roadmap claims are not current guidance.
