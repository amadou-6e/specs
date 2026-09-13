# Compact controls evidence

Specs#56 / implementation#381. Protocol97e205793e6e443199f118b528c0c3fc9181e76c;
source3987482. Run compact-controls-v1-run1,60 fits,79.032 seconds including
preparation. No encoder updates, final test, HPO winner, certification or merge.

Plain1024 probes with selection-only thresholds: compact IoU.190-.230 and
boundary F1.305-.330, compared with spatial.690/.777 and raw neighborhood.633/.638.
Compact AUPRC.233-.264 occupancy/.223-.246 boundary remains near the random-grid
control. Threshold selection repairs many zero scores without closing this gap.
Balanced BCE changes operating points but does not materially improve ranking and
usually worsens probability log loss. Longer probes do not rescue these96-update
smoke checkpoints. Compact training AUPRC is also low, not just held-out scores.

Direction: investigate tiny-corpus compact overfitting and a known geometric-code
decoder control, then position-enriched coordinate/decoder ablations under a new
protocol. Equal small heads face different decoding difficulty for spatial versus
global representations. Do not infer a fundamental128-dimensional capacity limit
or start broad HPO from this diagnostic. Full campaign foundations remain partial.

All comparisons use one seed/two families, central17 queries, fixed masks; controls
are not parameter-matched, random grid is not aggregation-matched, and raw input
is only a3-cubed neighborhood. No distance or wider-field claim. Full report:
docs/perception-compact-controls-assessment.md in implementation repository.
Machine payload05385b70d722dcfa75222e1f62f82b3682bdddd0a46622eba478d357da4bad86.
60 prediction/probe artifacts hashed outside Git.442 full garden tests passed
before additional evidence replay coverage. Disposition retain diagnostic.
