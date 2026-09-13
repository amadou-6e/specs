# Experimental fine729 package

Specs #76 / implementation #403. Authorized unmerged successor to replication
#401, source b3a28146fa2c2c8f890e9b0b9b531196032cb8a8, spec
b77b6a20ffc7e88930b4e4110133a649afdb95c7, verified report
f7d65863a81c3c905d24649d78a4d2d55ce747ccc0c89d361feb796d4bfc7c10.
All three seeds passed the directional packaging assessment. No new training,
model selection, threshold calibration or scientific quality claim occurs here.

## Interface

Expose a frozen encoder taking binary occupancy (B,33,33,33) and a boolean
unknown mask of the same shape (or B,1,33,33,33). All cells are valid, stride1;
other geometry/validity regimes are unsupported. Mask semantic occupancy/free
channels using VoxelLevel.from_occupancy before the fixed backbone. Never expose
the unused backbone projection or raw feature volume to the caller's head.

Output is a detached float32 tensor (B,729), normalized by the frozen probe-only
float64 population statistics. Layout is channel-major1x9x9x9, centers8..24
at stride2 in the input. It is a spatial code, not a generic global embedding.
Backbone and aggregation remain eval/frozen even if the parent calls train().
Use no_grad, not inference_mode, so a separately trainable head can consume it.

Provide the separately loaded native head; it accepts only code and integer
central17 flattened query indices and produces three raw-logit/value channels:
hidden occupancy, boundary, and normalized clearance/recovery distance. Query
indices use the existing tensor flatten order. Apply sigmoid to binary channels
and clamp distance to[0,1] for evaluation; return raw values for head training.
Default seed401 is the lowest numeric ID, not a development-selected winner.
Export all401/402/403. No fine-tuning the encoder or transferring arbitrary-head
quality is claimed.

## Artifact and verification contract

Versioned manifest pins this full spec SHA, source commit, replication report
hash, input/output layout, normalization, all three seed/checkpoint/state hashes,
calibrated thresholds, and experimental/non-promotion status. Atomic local weight
files plus SHA256 hashes; loader checks manifest digest, safe basenames, format,
fixed contract, file hashes and restored module state hashes before returning.
Statistics must be finite,729-long, shared across positions and scale>=1e-5.
Weights/corpora remain runtime-only; commit compact manifest/verification report.

Export is conditional on the verified replication report hash and recomputed
packaging-readiness assessment. Recheck source report/artifact/backbone hashes.
Replay direct occupancy/mask inputs for the first32 and last32 development rows
for every seed, at rtol1e-5/atol1e-6 against saved independent-head predictions.
This is implementation equivalence, not a new holdout claim. Test forward sizes,
invalid inputs, manifest/weight tampering, state round trip and mask isolation.
On disposable copies, take a head-only optimizer step and require finite nonzero
head gradients, changed head state, unchanged encoder state and no encoder grads.
Do not save the modified head. Report CUDA peak memory and warm median/p95
encoder latency at batch1 (ten warmups,50 timed repetitions, synchronized).

Use deterministic float32 CUDA without TF32/autotuning. No new corpus beyond
regenerating the known development rows for equivalence. Freeze package identity
`compact-package-v1-run1` and governing/source SHAs before validation. Reserve
1800 seconds inside the existing48 GPU-hour ledger, including300s test overhead.
No overlapping GPU run; charge actual successful elapsed time plus reserve, or
the full tranche on failure. No failed-run overwrite or uncharged resume.

Success delivers a directly loadable experimental local-geometry artifact and
usage example with the explicit limits. It does not promote to develop, merge
PRs, establish planning/topology transfer, or certify out-of-distribution quality.
