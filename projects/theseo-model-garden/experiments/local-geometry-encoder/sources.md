# Consolidated sources

## Frozen protocol provenance

| Iteration | Preserved source | Frozen specification commit | Role and limitation |
| --- | --- | --- | --- |
| LG1 | [Legacy protocol](../../legacy/python/perception-encoder-local-geometry.md) | `062acdd3964c50c9d9c588734073d340a21ccf2e` | Prospective protocol and immutable LG1 authority. |
| LG2 | [Legacy protocol](../../legacy/python/perception-encoder-local-geometry-lg2.md) | `ee173bc2a61064386ee8669f77bad9ddf016b709` | Prospective LG2 protocol; changes LG1 rank handling only for LG2. |
| LG3 | [Legacy protocol](../../legacy/python/perception-encoder-local-geometry-lg3.md) | `082f5b7e8979fe8e9fdf840087fa93df7c430dc2` | Prospective frozen-checkpoint transfer protocol. |

The local [canonical protocol](protocol.md) is the current reading surface. These
legacy documents preserve historical wording and immutable identities; they are not
required to understand the experiment's design.

## Result and machine-evidence provenance

| Iteration | Assessment | Machine report | Role and limitation |
| --- | --- | --- | --- |
| LG1 | [Assessment](../../legacy/python/perception-encoder-local-geometry/lg1-assessment.md) | [JSON](../../legacy/python/perception-encoder-local-geometry/lg1-report.json) | Direct completion evidence; generated weights and tensors are external. |
| LG2 | [Assessment](../../legacy/python/perception-encoder-local-geometry/lg2-assessment.md) | [JSON](../../legacy/python/perception-encoder-local-geometry/lg2-report.json) | Direct completion evidence; includes control and interval statistics. |
| LG3 | [Assessment](../../legacy/python/perception-encoder-local-geometry/lg3-assessment.md) | [JSON](../../legacy/python/perception-encoder-local-geometry/lg3-report.json) | Direct completion evidence; fresh-probe and zero-shot paths must remain distinct. |

LG2's [rank fixtures](../../legacy/python/perception-encoder-local-geometry/lg2-rank-fixtures.json)
support the preregistered rank-methodology deviation. Repository paths under the
legacy tree are retained for provenance; canonical results and evidence manifests now
live inside this experiment entry.
