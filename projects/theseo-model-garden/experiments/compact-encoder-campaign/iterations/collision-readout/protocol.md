# Inherited collision-readout protocol

## Authority and question

This is the canonical migrated representation of the separately frozen collision-
readout sub-protocol. Its original wording remains in the linked legacy source at
revision `4961f46d4023d9780a9ffd0db18db2bf5e29e09c`.

Question: can a better small-field readout recover collision-relevant information from
the existing normalized 729-value code, and can explicit uncertain-path calibration
expose or reduce the pooled-threshold failure?

## Fixed boundary

- Input field 33, central target 17, zero-radius discrete six-connected paths.
- No field scaling, encoder adaptation, RLlib evaluation, or global planning.
- Packaged seeds 401, 402, and 403; encoder normalization and native geometry-decoder
  weights remain fixed.
- Fresh train/calibration/ID/OOD data with parent overlap rejected against predecessor
  datasets and across new splits.
- Synthetic OOD shares density controls and is not real-sensor validation.

## Data and paths

Use seven generators and density levels 0.08, 0.16, and 0.28. Use 1,536 train, 768
calibration, 768 ID-test, and 576 OOD geometries. Each geometry provides 32 seeded
six-connected paths with lengths 2, 3, 5, and 9 equally represented. Collision means
any truly occupied valid node. Require at least 100 uncertain positives and 100
uncertain negatives in calibration; reject inadequate support rather than changing
the generator or threshold rule.

## Controls and training

Fit original, resize-convolution, transpose, frozen-native-decoder, raw-grid,
spatial-feature, and null heads for every seed. Resize-convolution and transpose are
parameter-count matched; the other controls are diagnostic rather than capacity-
matched. No occupancy or unknown query feature may bypass into compact heads.

Train all 21 heads for 4,096 updates using the inherited AdamW recipe, identical shared
sampling sequences within a seed, checkpointing every 512 updates, and no early
stopping or test-driven selection. This is a fixed-recipe comparison, not HPO.

## Calibration and evaluation

For each head, lock an overall and an uncertain-only inclusive threshold retaining at
least 95% empirical calibration collision recall. Lock all 42 thresholds before test
prediction access. Report ranking, calibration, operating-point, support, and
stratified path metrics. Keep the observability-assisted diagnostic explicitly
separate because it uses raw visibility and is not a pure compact-code interface.

The primary contrast is paired per-geometry uncertain-path natural-log loss with
1,000 family/density-stratified geometry bootstrap resamples. Test shuffled and zeroed
compact codes without refitting or recalibration. OOD evidence may diagnose transfer
but may not select a winner.

## Frozen decision gates

An ID improvement candidate requires, in every seed:

1. positive lower 95% bootstrap bound versus the original head;
2. uncertain AUPRC gain of at least 0.03;
3. uncertain missed-collision rate no greater than 0.10; and
4. uncertain false-alarm rate no greater than 0.25.

The stronger competitiveness screen additionally requires overall and uncertain AUPRC
within 0.03 of both raw-grid and spatial controls in every seed. Report every failed
condition. Never average failing seeds into a pass, relax criteria, select from OOD,
or add a fourth recipe after inspecting locked tests.

## Budget, validity, and disposition

Reserve 14,400 seconds from the 48 GPU-hour campaign, including a 1,200-second
validation reserve, with a cumulative 1,800-second cap per fit. Source, identity, mask,
or replay failures exclude affected evidence and require an explicit revision.

Replay datasets, frozen states, queries, labels, heads, thresholds, predictions,
metrics, comparisons, and decisions. Completion must assess readout benefit, residual
information loss, and the miss/false-alarm trade-off. Neither passing the improvement
screen nor packaging artifacts authorizes merge, promotion, deployment, or a safety
claim.

## Provenance

- [Original frozen protocol](../../../../legacy/python/perception-encoder-collision-readout.md)
- [Original assessment](../../../../legacy/python/perception-encoder-collision-readout-assessment.md)
