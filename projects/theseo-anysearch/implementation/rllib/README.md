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

## Draft guidance and investigation

The following pages are not yet accepted implementation rules. They retain
their pinned-source evidence and unresolved test gaps:

- [RLlib object investigation](integration.md)
- [Algorithm adapters and support evidence](algorithms.md)
- [Models, policies, and observation adaptation](models-and-policies.md)
- [RLlib checkpoint integration](checkpoints.md)
- [Environment registration and RLlib adaptation](environment-integration.md)
- [Compatibility, support evidence, and upgrade testing](compatibility-and-testing.md)
- [RLlib test placement and evidence](testing.md)

The training lifecycle, curriculum, evaluation, checkpoint, Tune, and artifact
ownership map belongs to the [training-and-tuning subsystem](../../subsystems/training-and-tuning/design/README.md).

The former `legacy-module-spec.md` has moved to the [legacy archive](../../legacy/rllib-module-spec.md).
Its abstract-trainer and algorithm roadmap claims are not current guidance.
