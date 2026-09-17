# Held-out family evidence

Issues specs#45 / theseo-anysearch#370. Protocol frozen at
`bc3a092d07309eb8f22390bd2878f371713badad`, executable `1a73724`.

Completed `transfer_supported`: all eight family/task checks passed on every seed.
New boundary F1 shells 0.783-0.805, labyrinths 0.769-0.781; occupancy IoU
0.869-0.878 and 0.793-0.810 respectively. Both distance tasks passed on both
families. All paired improvement intervals favor the new encoders.

Probes were fitted/threshold-selected only on the original four families; no
new-family adaptation and zero encoder updates. Fixed 32-hidden probes, matched
old/new exposure. Retain new local encoders as candidates for scale/context tests,
not as universal or real-world encoders. No topology or promotion claim follows.

Full implementation assessment: docs/perception-family-transfer-assessment.md.
Report payload `f48a2741debf123070493623f078fd8832cc6900bcd9855fe54f07669f26124c`.
Recorded duration 37.94s; all 24 probe artifacts remain untracked and hashed.
