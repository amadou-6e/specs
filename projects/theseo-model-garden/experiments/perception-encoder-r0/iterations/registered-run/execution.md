# Execution

## Identity

| Item | Recorded value |
|---|---|
| Run | `voxel-encoder-pilot-v2r2-r0-1` |
| Dataset | `voxel-encoder-pilot-v2r2-dataset-1` |
| Governing pilot spec | `0060366f43892bade5acf734cf2e189d8a666ad2` |
| Pre-data registration | `a0d03c434be72d6eab7d962e53af62a7dd57b11d` |
| Protocol SHA-256 | `8230bd97ea14f14f8a8910af61cde7ad211a6c189c9129981d225b45c79a8fe3` |
| Executable source | `f902b428c61b3a20c386fb3a91d28726fdd470d3` |
| Runtime head | `6c34230632920534b54bb4a625b784b7636d26dd` |
| Configuration SHA-256 | `6a56e73552066d03d4c1f6d1e08aecbc4171d4ad4ddb22d92eb17462b5215c29` |
| Started | `2026-09-08T15:37:33.899431+00:00` |
| Finished | `2026-09-08T15:38:07.804005+00:00` |

## Materialized identities

| Artifact | SHA-256 |
|---|---|
| Pool plan | `af923f0e3157f212b442746f0791f92739a5336834291b82b6e1dddccaa887c1` |
| Query plan | `e6ca0e1834cf474b37d846f986ca2ca9cbadb96a581b07d0341d084d77367df7` |
| Data manifest | `18e9335430799e1588dd89e586ed1d879147d3833d2a7c10b384732c85074f73` |
| Donor bank A | `1421eb9e3d8f651589e63691b0b0c6035af07508e585f7f03b4e48f5fea8a90b` |
| Donor bank B | `b1ffdafd14f910ca7ec35807a525140e7ae87a7f08adeb0bc1415967255f7cd5` |
| Control artifacts | `f421e888bdcea131e14caa56eef4a6819648ca8a48ba9daaff54a3408b34f595` |
| Predictions | `a4887e9d49da918b3c2fd7c7ee11e71c92e017d2c3488817c4e61692f74f2f03` |

The run selected 216 training, 72 in-domain, and 72 transfer contexts. Each query
received 64 completions, producing 23,040 labels.

## Runtime and resources

Execution used four CPU generation workers and CUDA fitting on an NVIDIA GeForce RTX
3060 Ti. Wall time was `33.904757600001176` seconds. Two control fits performed 4,096
updates each. Their accelerator-hour upper bounds totaled
`0.0022329438055546944`. Candidate training updates were zero because R0 was an
audit, not encoder training. No resource cap was exhausted.

## Deviations and validation

No registered setting changed after data opening. External review was still pending
when execution began, contrary to the surrounding workflow expectation. This is a
workflow deviation, not retroactive protocol approval.

The preserved result says the saved-prediction assessment reproduced exactly and 354
Garden tests passed, including evidence-chain and stop-rule tests. This migration did
not rerun those tests.
