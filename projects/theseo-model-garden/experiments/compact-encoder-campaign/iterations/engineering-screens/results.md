# Engineering-screen results

The smoke completed after replacing nondeterministic adaptive-pooling backward, but
five of six configurations had zero thresholded occupied IoU and boundary F1 at 0.5.
The controls study showed selection-only thresholds repaired many zero scores without
closing the large ranking gap to spatial and raw-neighborhood controls.

All six query-decoder learnability arms then failed the declared 0.95 IoU/0.97 F1
overfit targets, even though the analytic generator-code reference recovered targets
exactly. The dense-output positive control separated that decoder problem: the learned
table and actual voxel encoder reached IoU/F1 of 1.0 by 128 updates, while the oracle
six-value arm remained below the frozen gate.

Disposition: retain the evidence that the compact training path can memorize the tiny
corpus and proceed to fresh-scene optimization with independent readouts. These screens
do not certify generalization, a preferred architecture, deployment quality, or a
fundamental compact-dimension limit.
