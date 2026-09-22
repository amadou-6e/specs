# Consolidated sources

The files below are preserved migration sources. Canonical navigation and bounded
interpretation live in this experiment entry. External implementation assessments and
artifact hashes are recorded in the corresponding iteration evidence manifests.

| Role | Preserved source | Limitation |
| --- | --- | --- |
| D0-D2 protocol/result | [Protocol](../../legacy/python/perception-encoder-diagnostics.md), [evidence](../../legacy/python/perception-encoder-diagnostics-evidence.md) | Development diagnostic; large artifacts remain external |
| Checkpoint protocol/result | [Protocol](../../legacy/python/perception-encoder-checkpoint-diagnostic.md), [evidence](../../legacy/python/perception-encoder-checkpoint-evidence.md) | Development diagnostic only |
| Reference protocol/result | [Protocol](../../legacy/python/perception-reference-refinement.md), [evidence](../../legacy/python/perception-reference-refinement-evidence.md) | Single-seed screen followed by fresh confirmation |
| Continuation protocol/result | [Protocol](../../legacy/python/perception-encoder-continuation.md), [combined evidence](../../legacy/python/perception-encoder-continuation-evidence.md) | Combined evidence also reports distance retention |
| Retention protocol | [Distance retention](../../legacy/python/perception-distance-retention.md) | Its result is in the combined continuation evidence |
| Transfer protocol/result | [Protocol](../../legacy/python/perception-family-transfer.md), [evidence](../../legacy/python/perception-family-transfer-evidence.md) | Procedural families, not real-world transfer |
| 17-to-33 protocol/result | [Protocol](../../legacy/python/perception-context-scale.md), [evidence](../../legacy/python/perception-context-scale-evidence.md) | Central-query pilot, not full-volume accuracy |
| 33-to-65 protocol/result | [Protocol](../../legacy/python/perception-context-65.md), [evidence](../../legacy/python/perception-context-65-evidence.md) | Local resource measurements |
| Tiled protocol/result | [Protocol](../../legacy/python/perception-context-tiles.md), [evidence](../../legacy/python/perception-context-tiles-evidence.md) | Sampled central-49 output |

Implementation provenance is the `theseo-anysearch` experiment branches and commits
listed per iteration. Specification issues range from specs#35 through specs#51;
implementation issues range from theseo-anysearch#360 through #376.
