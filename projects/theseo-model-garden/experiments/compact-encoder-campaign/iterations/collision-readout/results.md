# Collision-readout results

## Primary result

All 21 fits and 90 locked test-prediction groups completed. Resize-convolution,
transpose, and frozen-native heads passed the preregistered three-seed ID improvement
screen. Their geometry-weighted uncertain-path negative-log-loss bootstrap intervals
against the original head were positive in seeds 401, 402, and 403; each also exceeded
the required 0.03 uncertain AUPRC gain and met the empirical ID limits of 10% missed
collision and 25% false alarm.

## Failed gate

No revised head passed the stronger competitiveness screen against both raw-grid and
spatial-feature controls in every seed. The result therefore does not authorize
promotion or deployment qualification.

## Supporting observations

The frozen-native head had ID uncertain-path AP of 0.642-0.676 across seeds, compared
with 0.476-0.512 for the original head, 0.721-0.753 for raw-grid, and 0.763-0.774 for
spatial features. Uncertain-only calibration reduced missed uncertain collisions, but
that is a changed operating point rather than improved ranking. Native OOD miss rose
to 7.4-8.3%, and OOD results were not permitted for winner selection.

## Disposition and non-claims

Retain geometry-aware readout directions without promotion. The experiment does not
establish sensor-noise robustness, contiguous-mask robustness, finite-body or swept-
volume safety, global reachability, or navigation performance. Further qualification
requires a fresh protocol and data and must not tune on these locked tests.
