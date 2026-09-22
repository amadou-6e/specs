# Collision-readout execution

## Identities

- Run: `compact-collision-readout-v1-run1`
- Frozen protocol revision: `4961f46d4023d9780a9ffd0db18db2bf5e29e09c`
- Implementation: `958b541`
- Frozen manifest commit: `84436a7`
- Package manifest: `2ddf188ecedff4699dba434fec05a851c5649119c07dcf30c9d9afd1292d4ed1`
- Runtime root: `runtime/compact-collision-readout-v1-run1`
- Fresh-input root: `runtime/compact-collision-readout-v1-inputs`

## What ran

Twenty-one fits ran: seven heads for packaged seeds 401, 402, and 403. Each fit used
4,096 updates with 32 geometries by four sampled paths, the fixed AdamW schedule, and
no HPO or early stopping. The corpus contained 1,536 training, 768 calibration, 768 ID
test, and 576 OOD geometries, with 32 short six-connected paths per geometry. All 42
thresholds were locked from calibration before test predictions were accessed.

The seven controls were original, resize-convolution, transpose, frozen native
decoder plus head, raw-grid, spatial-feature, and null. Encoder, normalization, and
native-decoder states were frozen and checked before and after extraction and replay.

## Environment and resources

Execution used deterministic float32 CUDA with TF32 and autotuning disabled, four CPU
threads, cached inputs, and one GPU-preloaded training representation. The study
charged 3,102.907 seconds including its 1,200-second validation reserve. No training
process remained active after completion.

## Deviations and failures

No protocol deviation is reported in the assessment. Generated corpora, weights, and
prediction stores remained runtime-only as specified. The legacy assessment and
verification artifacts in the evidence manifest are the provenance for these facts.
