# Standalone Model Garden extraction

Status: staged boundary for [theseo-anysearch #501](https://github.com/amadou-6e/theseo-anysearch/issues/501) and [specs #134](https://github.com/amadou-6e/specs/issues/134). Current implementation source authority is `theseo-anysearch` `origin/exp/perception-encoder` commit `88e220ccdbca8c87c56875b5d742427eb7947540` (99 tracked `theseo_anysearch/garden/` files). The new [theseo-model-garden repository](https://github.com/amadou-6e/theseo-model-garden) now exists. Its [PR #2](https://github.com/amadou-6e/theseo-model-garden/pull/2) stages only the compact inference slice; the remaining implementation still lives in AnySearch. `spec.json` names the new project repository, not the historical implementation source.

## Migration strategy and ownership

Stage the new repository against this pinned experimental snapshot. Do **not** extract from `develop` alone, silently merge `exp/perception-encoder` into `develop`, or reinterpret frozen experiment runs. Maintain a source-file and commit-provenance map for the initial import; record later experiment-line changes as explicit synchronization decisions. AnySearch's `develop` integration is a separate reviewed consumer change that selectively adopts accepted interfaces and their dependencies.

The standalone distribution owns reusable encoder architectures, preprocessing, dataset abstractions, training and evaluation, artifact publication and integrity, and its own CLI. AnySearch owns environment sampling, trajectory reading, RLlib policy construction, and the adapter that supplies the Garden encoder to a policy. The extracted core must not import AnySearch, Ray/RLlib, or native runtime packages merely to import a model or load an artifact. Native collection and Ray tuning belong behind optional extras/adapters; the minimal inference install needs only the dependencies required to construct and run its encoder and verify an artifact.

Historical experiment records remain immutable in the specs repository. Their source and artifact identities are not rewritten when code moves. New experiments identify the new repository revision and any cross-repository adapter revision explicitly.

## Existing compact artifact contract

At the pinned source, `theseo_anysearch/garden/compact_package.py` defines `compact-spatial-code-v1`. It validates a manifest payload hash, per-file SHA-256, restored encoder and head state hashes, and a fixed seed set. The input is binary `B x 33 x 33 x 33` occupancy plus a matching boolean unknown mask; the frozen encoder returns a normalized 729-dimensional code with latent shape `(1, 9, 9, 9)`. The loader also returns a separate trainable native head. The contract itself says `status: experimental` and `promotion_eligible: false`. Extraction must preserve those fields and checks; package relocation is not a qualification decision.

The older `GardenStore` `encoder.pt`/`meta.json` path remains a distinct artifact path. Do not present it as interchangeable with the compact package or invent an implicit converter. Define an explicit compatibility reader or migration command if either path changes, with tests for both existing artifacts and malformed/tampered inputs. Inference must reject incompatible preprocessing, tensor shape, architecture, format version, seed, or hash rather than silently falling back to a new encoder.

## Cross-repository handoff

1. Create the standalone repository from the pinned snapshot with a source-provenance manifest. Separate importable inference core from optional training, tuning, native sampling, and AnySearch trajectory/environment adapters. Preserve tests and the `compact-spatial-code-v1` round trip.
2. Publish a minimal-install test artifact and verify loading without AnySearch, Ray/RLlib, or a native wheel. Keep model weights and raw experiment stores out of source Git unless a separately reviewed distribution decision authorizes specific fixtures.
3. Add an AnySearch adapter that consumes the new distribution. Test artifact loading and policy construction against compatible observation spaces, while keeping existing configuration/import paths working through a documented deprecation window or explicit migration utility.
4. Review a separate `develop` integration PR. It must list the selected accepted source commits and dependencies; it must not merge the experimental integration branch wholesale.

Open decisions before release: package and CLI names, support window for old Python imports and aliases, distribution of already tracked pretrained `.pt` assets, and the exact accepted experimental features exposed to `develop`. Resolve these in #501 and linked implementation PRs, not by assuming extraction makes every experimental component production-ready.
