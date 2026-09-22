# Environment runtime design

The runtime separates framework integration from authoritative simulation. Python
constructs compliant adapters and orchestrates configurable behavior; Rust owns state
mutation and performance-sensitive transitions; PyO3 preserves values and failures
across the boundary.

On reset, Python resolves scenario and task state and invokes native reset. On step,
Python encodes an action, Rust performs the transition, and Python applies its ordered
lifecycle chain before returning the framework result.

Rust owns native agent state, collision outcomes, world access during a step, and
native reward/lifecycle data. Python owns scenario selection, framework agent lists,
spaces, and lifecycle composition. Conversion failures and native extension errors
surface at the bridge rather than becoming valid transitions.

Separate single- and multi-agent paths preserve incompatible framework semantics but
increase parity work. Python lifecycle hooks make composition accessible while native
termination supplies a fast baseline. Explicit task sources avoid the unbounded cost
of enumerating compiled worlds.

See [Python](python.md) and [Rust](rust.md) for the module maps.
