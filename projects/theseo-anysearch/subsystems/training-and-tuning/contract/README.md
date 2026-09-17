# Training and tuning contract

## Contained elements

```text
contract/
├── 1 README.md
└── 1 configuration.md
```

The contract owns deterministic experiment loading, stage completion semantics,
evaluation separation, Tune parameter activation, resource declarations, checkpoint
identity, pretraining reuse boundaries, and artifact locations.

## Imported sources

- [Experiment system](../../../experiments.md)
- [RLlib integration](../../../python/rllib.md)
- [Tune](../../../python/tune.md)
- [Training diversity](../../../python/rl-training-diversity.md)
