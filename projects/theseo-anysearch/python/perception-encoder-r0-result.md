# v2r2 R0 result

Run `voxel-encoder-pilot-v2r2-r0-1` completed on 2026-09-08.
Registered outcome: **defer**, recorded stop **no_topology_identifiable**.
Protocol/result acceptance remains pending review; nothing has been merged.

[Pre-data registration](perception-encoder-r0-execution.md) was published at
`a0d03c434be72d6eab7d962e53af62a7dd57b11d`. The immutable protocol identity is
`8230bd97ea14f14f8a8910af61cde7ad211a6c189c9129981d225b45c79a8fe3`.
Executable source was `f902b428c61b3a20c386fb3a91d28726fdd470d3`; the protocol was
published in implementation commit `6c34230632920534b54bb4a625b784b7636d26dd`
before data opening. No registered setting was changed after opening.

## Findings

All 216 training and 144 audit geometry quotas were filled. Each selected query
had 64 completions: 23,040 selected labels, including 9,216 audit labels.

| Optimistic span | In-domain negative labels | Held-out negative labels | Required per domain |
|---|---:|---:|---:|
| 1-2 | 84 / 1,536 | 0 / 1,536 | 64 |
| 3-5 | 79 / 1,536 | 0 / 1,536 | 64 |
| 6+ | 117 / 1,536 | 154 / 1,536 | 64 |

The first two transfer bins failed class support. The supported `6+` bin failed
all four conservative checks: entropy upper bound 0.915733 versus <0.90 bits;
visible-skill lower bound -0.077859 versus >0.02 bits/query; forbidden-predictability
upper bound 0.144125 versus <0.02; transfer-drop upper bound 0.156454 versus <0.05.

This does not prove random hidden geometry: the transfer `6+` entropy point
estimate was 0.447082 bits. It establishes insufficient evidence under this
empirical patch prior, spatial-sampling transfer, control recipe and budget.
Forbidden metadata was not supplied to the visible model; failure of that bound
does not establish encoder-input leakage. No architecture was ranked or rejected.

R0 took 33.905 wall seconds. CUDA control fitting used an upper bound of 0.002233
accelerator-hours on the RTX 3060 Ti, with 8,192 control updates and zero candidate
updates. No resource cap was exhausted. Both domains used identically hashed
fitted controls. The saved-prediction assessment reproduces exactly without
retraining; 354 Garden tests passed, including evidence-chain and stop-rule tests.

## Disposition and deviation

P0C, P0D and P1 were not started; no comparative contract was frozen. Preserve this
stop, rather than changing bins, thresholds or primary metrics under the same
identities. #341 is separately proposable, not an automatically started successor.

The earlier state-review snapshot requested review of numeric choices before
data opening. External review of this execution registration was still pending
at execution; that ordering expectation was missed before launch. This is a
recorded workflow deviation, not retroactive protocol approval. Pre-data
publication preserves the chosen rules, but acceptance or supersession remains
for reviewers. See specs PR #28 and implementation PR #352.

## Evidence

[Full machine-readable report](perception-encoder-r0-report.json), payload SHA-256:
`f14bacb88d29c1da009fb3ed02a6fa63648675706fef488661eb1c44dff9e71c`.

[Full assessment](https://github.com/amadou-6e/theseo-anysearch/blob/2c0f9a7a30e0ec1a937394a224a603ef07fef7fd/docs/perception-encoder-r0-assessment.md)
and [all execution artifacts](https://github.com/amadou-6e/theseo-anysearch/tree/2c0f9a7a30e0ec1a937394a224a603ef07fef7fd/experiments/perception_encoder/results/v2r2_r0)
are pinned to the result commit, including the frozen protocol, materialized-query
hashes, predictions, fitting hashes and review-status record. Raw volumes and
weights are not committed.
