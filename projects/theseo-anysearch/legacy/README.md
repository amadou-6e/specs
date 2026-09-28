# Legacy

Legacy is an expandable collection of single-document historical entries. Every entry
is explicitly non-authoritative and exists only while it retains evidential value.

## Contained elements

```text
legacy/
├── 1 README.md
├── 1 template.md
└── 0..* <historical-topic>.md entries
```

Each entry identifies what it formerly described, when its authority ended, and one
or more active replacements. Active migration instructions remain in the owning
subsystem rather than only in this archive.

Copy [template.md](template.md) to create an entry. The template itself is not a legacy
record.

## Imported Rust and RLlib migration (#110)

These files retain the original pre-taxonomy text below an archive notice. Their
original paths remain recoverable in Git history, but they are not alternate current
contracts. Each current owner below is the starting point for new work; unresolved
historical details require validation before being incorporated.

| Former document | Historical entry | Current owner |
| --- | --- | --- |
| `rust/bridge.md` | [Bridge](rust-bridge.md) | [Architecture](../architecture/README.md) and [Rust implementation](../implementation/rust/README.md) |
| `rust/environment.md` | [Environment](rust-environment.md) | [Environment runtime](../subsystems/environment-runtime/README.md) |
| `rust/ingest.md` | [Ingest](rust-ingest.md) | [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) |
| `rust/rendering.md` | [Rendering](rust-rendering.md) | [Trajectory and replay](../subsystems/trajectory-and-replay/README.md) |
| `rust/testing.md` | [Testing](rust-testing.md) | [Rust implementation](../implementation/rust/README.md) and subsystem validation pages |
| `rust/voxel-spec.md` | [Voxel renderer](rust-voxel-spec.md) | [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) and [Trajectory and replay](../subsystems/trajectory-and-replay/README.md) |
| `rust/world.md` | [World](rust-world.md) | [Worlds and geometry](../subsystems/worlds-and-geometry/README.md) |
| `rllib/explain/README.md` | [Explain overview](rllib-explain-overview.md) | [Policy explainability](../subsystems/policy-explainability/README.md) |
| `rllib/explain/backend.md` | [Explain backend](rllib-explain-backend.md) | [Python design](../subsystems/policy-explainability/design/python.md) |
| `rllib/explain/cli.md` | [Explain CLI](rllib-explain-cli.md) | [Interfaces](../subsystems/policy-explainability/contract/interfaces.md) |
| `rllib/explain/policy-attribution.md` | [Policy attribution](rllib-policy-attribution.md) | [Explainability contract](../subsystems/policy-explainability/contract/README.md) |
| `implementation/rllib/legacy-module-spec.md` | [RLlib module proposal](rllib-module-spec.md) | [RLlib object investigation](../implementation/rllib/integration.md) and [training-and-tuning design](../subsystems/training-and-tuning/design/README.md) |

The migration is a classification and authority cleanup, not a new audit of the
product implementation. These candidate details remain deliberately unpromoted:

- The archived [bridge DTO/function catalog](rust-bridge.md) needs comparison with
  current PyO3 exports before any detail is added to architecture or interfaces.
- The archived [SurfaceEnv behavior](rust-environment.md), [STL ingestion limits](rust-ingest.md),
  and [renderer milestones](rust-rendering.md) require focused current-code and test
  evidence in their owning subsystems.
- The archived [test inventory](rust-testing.md) must be checked against current
  native tests before becoming contributor guidance or validation evidence.
- The archived [SHAP proposal](rllib-policy-attribution.md) and
  [backend plan](rllib-explain-backend.md) should not replace the current
  grouped-occlusion contract without a separately reviewed methodology change.
