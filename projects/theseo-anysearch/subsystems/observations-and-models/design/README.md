# Observation and model design

## Contained elements

```text
design/
├── 1 README.md
└── 1 python.md
```

Python currently owns observation assembly exposed to RLlib and Torch model
definitions. Native world queries may produce spatial inputs, but do not own the
learning-model contract.
