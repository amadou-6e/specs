# Frozen encoder new-family validation

Issues specs#45 / theseo-anysearch#370. User-authorized stack on exp/368, no merges.
Source checkpoints are the same old/new encoders used in distance retention,
governed by specs commit762262d657b4320dbce39d3b53bc028105a2896b. No encoder updates.

## Split boundary

Study `voxel-family-transfer-v1`; dataset `voxel-family-transfer-v1-development-1`.
Probe training192 and selection48 use only random_field, oblique_sheets,
height_field, curved_tubes. Assessment48 uses only shells and trig_labyrinth.
Balance each family across occupied fractions0.08/0.16/0.28. No new-family probe
fitting, capacity selection, threshold tuning or encoder selection is permitted.
Check duplicate occupancy hashes across splits and against the retention corpus.

For new families, seed NumPy from the first8 little-endian SHA256 bytes of geometry
ID. Use a17-cubed [-1,1] grid. Shell field is abs(norm(xyz-center)-radius),
center components uniform[-0.3,0.3], radius uniform[0.45,0.85]. Labyrinth field is
sin(x)*cos(y)+sin(y)*cos(z)+sin(z)*cos(x), with each grid axis multiplied by an
independent uniform[2.5,5.5] frequency and shifted by uniform[-pi,pi] phase.
Occupancy is field <= its frozen fraction quantile. These are held-out procedural
generator families, not evidence of real-world or universally novel geometry.

Use existing exact target and LG1 CPU query routines: train stream34101, other
splits34102; 20% masking, 256 task-eligible queries per geometry. Full query banks
are fresh due to new geometries. Require >=20 positive/negative classification
rows per family and split, no redraw. Distance targets and query eligibility
match the prior retention protocol.

## Frozen probes and metrics

Old and new encoders, every seed0/1/2; four tasks: occupied IoU, boundary F1,
clearance NMAE and recovery NMAE. Fit a fixed32-hidden SiLU head per task using
train-only normalization, AdamW lr0.001/wd0.01, batch1024, 1024 updates. BCE for
classification, SmoothL1 for distances. This is a fixed-head transfer test, not
the earlier capacity-selected probe ladder. Old/new exposure and budgets match.
Use final probe weights. For binary tasks choose a threshold by selection F1
over0.01..0.99, ties lowest, then report IoU/F1 on assessment. This selection is
confined to established families. Distance predictions clamp to[0,1].

Assess each new family/task separately. Require every new seed to meet IoU0.60,
F1 0.70, clearance0.15, recovery0.20, plus paired improvement lower95% bound
>=-0.03 for classification or >=-0.02 for distances. Positive improvement favors
new encoders. Bootstrap whole geometries within density strata, same draws for
both arms and all seeds;2000 replicates, seed370, average seed metrics. Recompute
classification ratios from summed sufficient statistics per draw. All eight
components must pass to report transfer_supported; otherwise transfer_unconfirmed.
These engineering criteria do not authorize promotion or block future diagnostics.

## Integrity and scope

Freeze exact spec/source commits, geometry/query hashes, source-report and prior
registration hashes, encoder file/state hashes before fitting. Verify unchanged
encoder states afterward. One-hour cap checked before each bounded probe sequence
and after each1024-update fit; incomplete evidence cannot pass. Commit reports
and artifact hashes, never weights/corpora. Preserve old verdicts. No topology,
planning, radius-scaling or general certification claim follows.
