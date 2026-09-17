# Subsystems

Subsystems is an expandable collection of multi-file specification entries. Each
entry is a functionally cohesive part of Theseo with one stable behavioral and
contractual boundary.

## Contained elements

```text
subsystems/
├── 1 README.md
├── 1 template/
└── 0..* <subsystem>/ entries
```

Each mature subsystem entry contains one overview, one `contract/`, one `design/`, and
one `validation.md`. It may additionally contain consumer `guides/` and active
`migrations.md`. Contract details, language mappings, and diagnostics remain grouped
under their owning area rather than appearing as unrelated root-level files.
Subsystems may depend on other subsystems but must not silently share ownership of one
contract.

Copy [template/](template/README.md) to create an entry. The template itself is not a
subsystem entry.

## Current subsystem entries

| Subsystem | Owned boundary | Migration state |
| --- | --- | --- |
| [Worlds and geometry](worlds-and-geometry/README.md) | World representation, coordinates, occupancy, persistence, and geometry ingestion | Draft; imported Rust generations require reconciliation |
| [Environment runtime](environment-runtime/README.md) | Reset/step lifecycle, actions, rewards, agents, masks, and standard environment APIs | Draft migration index |
| [Observations and policy models](observations-and-models/README.md) | Observation schemas, preprocessing, encoders, policy/value model interfaces | Draft; experimental encoder evidence remains separate |
| [Training and tuning orchestration](training-and-tuning/README.md) | Experiment loading, RLlib/Tune execution, stages, evaluation, resources, checkpoints | Draft migration index |
| [World providers](world-providers/README.md) | Provider discovery, conversion/generation, verification, manifests, previews, registration | Draft; proposed and implemented generations require reconciliation |
| [Trajectory and replay](trajectory-and-replay/README.md) | Trajectory schema, replay, rendering, regional visualization, and camera behavior | Draft; UI Draw.io authority remains separate |
| [Model garden](model-garden/README.md) | Reusable representation packages, identities, certification, caching, and loading | Draft; research protocols require experiment migration |
| [Experiment tracking](experiment-tracking/README.md) | Searchable run parameters, metrics, identities, statuses, and artifact references | Draft migration index |
| [Policy explainability](policy-explainability/README.md) | Policy restoration, attribution, action comparison, and explanation artifacts | Draft migration index |

These entries classify existing specifications without declaring every imported claim
current. Each entry records unresolved reconciliation work at its ownership boundary.
