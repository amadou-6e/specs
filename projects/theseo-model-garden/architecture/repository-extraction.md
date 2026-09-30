# Standalone Model Garden extraction

Status: partial extraction for [theseo-anysearch #501](https://github.com/amadou-6e/theseo-anysearch/issues/501) and [specs #134](https://github.com/amadou-6e/specs/issues/134). The standalone repository's [PR #2](https://github.com/amadou-6e/theseo-model-garden/pull/2) merged as `756e5dd18251ae877ed3277a37f39e16f4b90764`: it contains the compact inference slice, not the entire garden. The remaining implementation source is `theseo-anysearch` `exp/perception-encoder` commit `88e220ccdbca8c87c56875b5d742427eb7947540` (99 tracked `theseo_anysearch/garden/` files at that snapshot). `spec.json` names the standalone repository as this project's source, without claiming the extraction is complete.

## Migration strategy and ownership

Stage the new repository against this pinned experimental snapshot. Do **not** extract from `develop` alone, silently merge `exp/perception-encoder` into `develop`, or reinterpret frozen experiment runs. Maintain a source-file and commit-provenance map for the initial import; record later experiment-line changes as explicit synchronization decisions. AnySearch's `develop` integration is a separate reviewed consumer change that selectively adopts accepted interfaces and their dependencies.

The standalone distribution owns reusable encoder architectures, preprocessing, dataset abstractions, training and evaluation, artifact publication and integrity, and its own CLI. AnySearch owns environment sampling, trajectory reading, RLlib policy construction, and the adapter that supplies the Garden encoder to a policy. The extracted core must not import AnySearch, Ray/RLlib, or native runtime packages merely to import a model or load an artifact. Native collection and Ray tuning belong behind optional extras/adapters; the minimal inference install needs only the dependencies required to construct and run its encoder and verify an artifact.

Historical experiment records remain immutable in the specs repository. Their source and artifact identities are not rewritten when code moves. New experiments identify the new repository revision and any cross-repository adapter revision explicitly.

## Specification ownership after the split

Model Garden owns this project's dataset-pipeline, encoder-models, pretraining-and-qualification, and model-registry specifications, plus its research and experiment records. The compact package's artifact format and inference behavior are Model Garden contracts. The older GardenStore and training pages remain here as **staged migration specifications** describing code still hosted in AnySearch; location does not transfer their product ownership.

AnySearch continues to own the consumer-facing specifications: [observations and models](../../theseo-anysearch/subsystems/observations-and-models/README.md), [RLlib models and policies](../../theseo-anysearch/implementation/rllib/models-and-policies.md), [RLlib checkpoints](../../theseo-anysearch/implementation/rllib/checkpoints.md), and its [Python module ownership](../../theseo-anysearch/implementation/python/module-ownership.md). These govern environment observation shape, policy construction, checkpoint compatibility, and host adapters, not Model Garden artifact publication. AnySearch's experiment-line run records remain pinned to their original source revisions.

## Existing compact artifact contract

At the pinned source, `theseo_anysearch/garden/compact_package.py` defines `compact-spatial-code-v1`. It validates a manifest payload hash, per-file SHA-256, restored encoder and head state hashes, and a fixed seed set. The input is binary `B x 33 x 33 x 33` occupancy plus a matching boolean unknown mask; the frozen encoder returns a normalized 729-dimensional code with latent shape `(1, 9, 9, 9)`. The loader also returns a separate trainable native head. The contract itself says `status: experimental` and `promotion_eligible: false`. Extraction must preserve those fields and checks; package relocation is not a qualification decision.

The older `GardenStore` `encoder.pt`/`meta.json` path remains a distinct artifact path. Do not present it as interchangeable with the compact package or invent an implicit converter. Define an explicit compatibility reader or migration command if either path changes, with tests for both existing artifacts and malformed/tampered inputs. Inference must reject incompatible preprocessing, tensor shape, architecture, format version, seed, or hash rather than silently falling back to a new encoder.

## Compatibility and migration policy

The merged standalone slice does **not** replace `theseo_anysearch.garden` imports, `anysearch garden` commands, AnySearch configuration keys, `GardenStore` paths, or existing experiment artifacts. Those paths still belong to the AnySearch implementation until a consumer migration is reviewed. Through AnySearch `0.x`, keep existing import, CLI, and config paths functional or provide tested aliases with equivalent behavior; removal requires a reviewed major-version migration with a documented command or mechanical mapping. Do not silently reinterpret a historical artifact or run configuration.

The new `theseo_model_garden` compact loader accepts only its versioned compact package. There is no automatic `GardenStore` conversion, name-registry lookup, or compatibility claim for legacy `encoder.pt`/`meta.json`. A future converter must specify source and destination identities, preserve originals, reject unsupported metadata, and prove a round trip and tamper failure. Adapter tests must cover compatible and incompatible observation/preprocessing shapes. These are migration requirements, not claims that an AnySearch adapter or converter already ships.

## Cross-repository handoff

1. The initial standalone inference slice is merged at `756e5dd18251ae877ed3277a37f39e16f4b90764`; preserve its source-provenance record and `compact-spatial-code-v1` round trip. Extract remaining training, tuning, and data code from the pinned experimental line only through separately reviewed changes.
2. Verify an installed minimal inference wheel loads a test artifact without AnySearch, Ray/RLlib, or a native wheel. Keep model weights and raw experiment stores out of source Git unless a separately reviewed distribution decision authorizes specific fixtures.
3. Add an AnySearch adapter that consumes the new distribution. Test artifact loading and policy construction against compatible observation spaces, while keeping existing configuration/import paths working through a documented deprecation window or explicit migration utility.
4. Review a separate `develop` integration PR. It must list the selected accepted source commits and dependencies; it must not merge the experimental integration branch wholesale.

Open decisions before full extraction: the standalone training CLI name, distribution of already tracked pretrained `.pt` assets, and the exact accepted experimental features exposed to `develop`. The old-path support window is specified above; #501 and linked implementation PRs must implement and test it. Extraction alone does not make every experimental component production-ready.
