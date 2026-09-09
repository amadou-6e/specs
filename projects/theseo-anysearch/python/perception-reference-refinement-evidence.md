# Reference refinement evidence

Issues specs#39 / theseo-anysearch#364. Frozen protocol
`44b089b58db3b9af45820cb358033c6a4acbc99f`, executable `7f3727c`.

Six fixed single-seed screening recipes selected dynamic masks, 192 geometries,
learning rate 0.003 and weight decay 0.01. Fresh three-seed assessment:
refined boundary F1 0.7628/0.7805/0.7468; baseline 0.4897/0.4879/0.4697;
frozen probe 0.6275/0.6182/0.6376. Paired loss improvement over baseline
0.1187 (95% CI [0.1023,0.1318]), over probe 0.0531 ([0.0296,0.0740]).

Outcome `reference_exceeds_probe`. Training refinement is a supported direction
with architecture fixed. No promotion: oblique-sheet F1 remains below 0.70 in two
seeds, and the reference has 192 training geometries versus the probe's 48.
Next proposed study equalizes probe exposure and tests broader-data/dynamic-mask
encoder pretraining at fixed architecture. This is a proposal, not a protocol
amendment or executed encoder study. No topology/scaling claims follow.

Completed in 256.16 recorded seconds, zero encoder updates. No weights committed.
Full implementation assessment: `docs/perception-reference-refinement-assessment.md`
on exp/364; report payload
`0baf857fccb0bc18ecb8c4aa917a2028d20d4625941a69f0de1460be94801043`.
