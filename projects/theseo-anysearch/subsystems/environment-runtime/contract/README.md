# Environment runtime contract

This page defines observable episode behavior shared by the supported adapters.
Framework-specific shapes are in [interfaces.md](interfaces.md), while selectors are
in [configuration.md](configuration.md).

## Reset

Single-agent `reset(seed=..., options=...)` selects or validates scenario, geometry,
and task state before resetting the native environment. It returns the initial
observation and scenario information. Equal deterministic inputs and seeds reproduce
runtime-controlled selection; external providers retain their own determinism rules.

A compiled world must have an explicit episode source. Missing task state fails rather
than triggering an unbounded scan for start and goal positions.

## Step

Each step validates and encodes the action, executes the native transition, collects
native reward and its breakdown, applies ordered Python lifecycle rules, then returns
the observation, total reward, lifecycle flags, and diagnostics. Invalid actions fail
explicitly rather than being silently remapped.

## Termination and truncation

Success and a configured collision limit terminate an episode. The maximum step count
truncates it. If both apply to one transition, termination takes precedence. Python
lifecycle rules may combine or override outcomes, but the final result preserves this
termination-dominance invariant. `info` exposes `termination_reason` and relevant
diagnostics so consumers do not infer cause from reward alone.

## Action masks

When enabled, a legal-action mask is derived from the same native bounds and occupancy
predicates used for execution. Its ordering follows the selected action mode. Predicate
or native mask failures surface immediately and never become an all-legal mask.

## Multi-agent behavior

PettingZoo runtimes accept and return per-agent mappings. Heterogeneous agents may
have distinct spaces. A single-agent observation key or lifecycle callback is not
guaranteed to exist unchanged in a multi-agent runtime.

## Non-guarantees

The runtime does not discover providers, guarantee that valid geometry has a reachable
task, or own policy-facing observation content beyond consistency with the wrapper's
declared observation space.
