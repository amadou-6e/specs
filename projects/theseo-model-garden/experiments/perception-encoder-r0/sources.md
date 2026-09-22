# Consolidated sources

## Governing and implementation sources

| Source | Identity | Role | Limitation |
|---|---|---|---|
| Governing pilot specification | `0060366f43892bade5acf734cf2e189d8a666ad2` | Surrounding v2r2 program. | Broader than R0; does not replace this protocol. |
| Pre-data registration | `a0d03c434be72d6eab7d962e53af62a7dd57b11d` | Proves publication before audit data opened. | External review remained pending. |
| Executable source | `f902b428c61b3a20c386fb3a91d28726fdd470d3` | Implementation used by the run. | Not correctness evidence by itself. |
| Runtime head | `6c34230632920534b54bb4a625b784b7636d26dd` | Published executable protocol revision. | Does not imply review acceptance. |
| Result revision | `2c0f9a7a30e0ec1a937394a224a603ef07fef7fd` | Pins assessment and artifacts. | Raw volumes and weights are absent. |

## Experiment evidence

- [Frozen protocol](protocol.md)
- [Execution](iterations/registered-run/execution.md)
- [Results](iterations/registered-run/results.md)
- [Evidence manifest](iterations/registered-run/evidence/README.md)

## Context

- [Model certification contract](../../subsystems/model-registry/contract/certification.md):
  qualification context, not evidence that R0 passed.
- [Perception-encoder research](../../research/perception-encoders.md): research
  context, not run evidence.

## Migration provenance

- [Original flat registration](../../legacy/python/perception-encoder-r0-execution.md)
- [Original flat result](../../legacy/python/perception-encoder-r0-result.md)
- [Machine-readable report](../../legacy/python/perception-encoder-r0-report.json),
  retained as an immutable evidence artifact with payload SHA-256
  `f14bacb88d29c1da009fb3ed02a6fa63648675706fef488661eb1c44dff9e71c`

The first two preserve migration provenance but no longer carry canonical narrative
roles. The JSON remains raw evidence; authority for its interpretation belongs to the
experiment-local results record.
