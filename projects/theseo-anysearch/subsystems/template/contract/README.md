# Behavior and guarantees

## Contained elements

```text
contract/
├── 1 README.md
├── 0..1 interfaces.md
├── 0..1 configuration.md
└── 0..1 extensions.md
```

This folder is the sole authority for the subsystem's observable contract. Interfaces,
configuration, and extension points refine that contract and cannot contradict the
behavior and guarantees stated here.

Document supported use cases, inputs and outputs, state transitions, lifecycle,
determinism, error and fallback behavior, resource guarantees, invariants, and
unsupported behavior. Describe what consumers can observe, not internal mechanics.
