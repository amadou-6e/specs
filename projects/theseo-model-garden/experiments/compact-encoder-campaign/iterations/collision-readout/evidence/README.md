# Collision-readout evidence

The canonical migrated protocol, execution, and results are local to this iteration.
The legacy documents below preserve the original wording and immutable provenance.

| Evidence | Identity or location | Role |
| --- | --- | --- |
| Local inherited protocol | [protocol.md](../protocol.md) | Canonical protocol representation for this entry. |
| Legacy frozen protocol | [legacy source](../../../../../legacy/python/perception-encoder-collision-readout.md) at `4961f46d4023d9780a9ffd0db18db2bf5e29e09c` | Original protocol provenance. |
| Legacy assessment | [assessment](../../../../../legacy/python/perception-encoder-collision-readout-assessment.md) | Original result narrative and validation evidence. |
| Report payload | `1a2ff1ff8e87667720a00d3b6d6f55db69dcadba7fd0e709112baca1a0cdb921` | Content identity recorded by the assessment. |
| Runtime artifacts | `runtime/compact-collision-readout-v1-run1` | Runtime-only weights, reports, predictions, and checkpoints. |
| Fresh inputs | `runtime/compact-collision-readout-v1-inputs` | Runtime-only generated corpus. |
| Verification | `docs/perception-encoder-local-geometry/compact-collision-readout-verification.json` at implementation revision `b3e7657` | Replay record: 314 artifacts, 21 heads, 111 prediction groups, 116,736 queries. |

Runtime retention is not guaranteed by this specs repository. The identities above
permit verification when the external artifacts remain available.
