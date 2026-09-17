# Configuration architecture

Status: draft. Tracks [specs#101](https://github.com/amadou-6e/specs/issues/101).
Last reviewed: 2026-09-17.

## Purpose

Theseo configuration currently mixes experiment orchestration, environment runtime
settings, geometry ingestion, procedural generation, routing tasks, task-feasibility
checks, generated-world provenance, and dataset-role assignment. This section records
the implementation as it exists and defines a target boundary among those concerns.

The main experiment YAML remains the composition root. Supporting YAML files are an
extraction mechanism for reusable or complex definitions, not a separate configuration
language. An inline definition and its file-backed equivalent must validate against the
same typed schema and resolve to the same normalized configuration.

## Documents

- [Current state](current-state.md): behavior and limitations in the implementation on
  `develop` at merge commit `72a413a2f10ba1aeb9430c8e3412bffc30d1e68c`.
- [Target state](target-state.md): proposed ownership boundaries, composed YAML shape,
  migration direction, and acceptance criteria.
- [Experiment configuration](experiment/README.md): responsibilities retained by the
  main experiment YAML.
- [Geometry configuration](geometries/README.md): source adapters, verified worlds,
  procedural generation, compilation, and runtime residency.
- [Task configuration](tasks/README.md): fixed task catalogs, generated episode tasks,
  labels, and train/validation/evaluation selection.

## Governing distinctions

1. **Geometry** describes occupied/free space and how it is obtained.
2. **Task** describes the objective presented to an agent in that geometry.
3. **Experiment use** decides which tasks are used for training, validation, and final
   evaluation and how they are sampled or enumerated.
4. **Verification and provenance** record how an artifact or task was derived and what
   was checked. They are generated evidence, not ordinary user-authored task fields.
5. **Runtime configuration** controls observations, actions, rewards, episode limits,
   streaming, and compute. It does not redefine immutable source artifacts.

The same world may be used with different routes in training and evaluation. This is a
valid familiar-geometry/unseen-route experiment. Whole-world holdout is a different
experimental claim. Theseo must record overlap sufficiently to audit the claim but must
not impose one universal holdout policy.

## Related specifications

- [Installable voxel-world providers and worlds CLI](../world-provider-cli.md)
- [3D routing asset and integration inventory](../routing-asset-inventory.md)
- [3D routing geometry integration roadmap](../routing-geometry-integration-roadmap.md)
- [Python settings](../python/settings.md)

Where those documents conflict with this draft, the conflict remains unresolved until
this specification is accepted and the affected document is explicitly updated.
