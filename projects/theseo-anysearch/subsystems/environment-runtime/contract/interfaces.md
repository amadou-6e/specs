# Environment interfaces

The native environment is exposed through PyO3 and adapted to Gymnasium for
single-agent use and PettingZoo ParallelEnv for multi-agent use. RLlib consumes those
standard Python interfaces rather than native objects directly.

## Imported sources

- [Python environments](../../../python/environments-python.md)
- [Native bridge](../../../rust/bridge.md)
