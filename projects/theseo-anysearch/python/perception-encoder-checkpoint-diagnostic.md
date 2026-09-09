# Matched-compute checkpoint diagnostic

Issues: specs#37, theseo-anysearch#362. Separate follow-up to D0-D2, not a
replacement verdict. User authorizes stacking on unmerged exp/360 and specs docs/35;
no integration merges or promotion. Prior protocol:
[D0-D2](https://github.com/amadou-6e/specs/blob/66279ceab743af9c350107fe26fca730d2b245fe/projects/theseo-anysearch/python/perception-encoder-diagnostics.md).

## Intervention

Use the exact reference architecture, optimizer, seed streams, batch size and
2048 updates from D1. On a single trajectory per seed, retain final weights and
the checkpoint with lowest selection boundary log loss at updates
256/512/768/1024/1280/1536/1792/2048. Ties choose the earliest checkpoint.
No early stopping, extra training, hyperparameter search or assessment selection.
This isolates checkpoint choice within the new campaign; it is not a paired
comparison against the previous campaign's different data.

Run seeds 0/1/2. Refit the same linear/32/128 frozen-feature probe ladder on the
new data and choose width by selection log loss, as previously. Zero encoder
updates. Both reference checkpoints calibrate their own F1 threshold on selection
only, using 0.01..0.99, ties lowest. Log loss is the primary paired comparison;
F1, AUPRC and family scores remain diagnostic. Keep original 0.70 F1 bar contextual,
not a gate on further research.

## Fresh identities and execution

Study `voxel-encoder-checkpoint-diagnostic-v1`, dataset with suffix
`-development-1`, query identity `voxel-encoder-checkpoint-diagnostic-v1-queries-1`.
48 training /24 selection /48 assessment geometries; same four families crossed
with three density fractions. CPU mask/query streams 36201/36202/36203, 20% masking,
256 hidden queries per geometry. All other generation and class-support rules
match D0-D2. Reject geometry hashes duplicated within or across splits or against
the previous D0-D2 corpus. Assessment instances are development evidence, not a
new domain-generalization certification.

Before fitting commit executable source, then freeze exact source/spec SHAs,
LG2 checkpoint file/loaded-state hashes, all geometry and query identities,
the prior-registration file hash, and the complete resolved plan. Recheck before
execution. D0 fixture sanity reruns with its original 300-second cap. Maximum
800 seconds per seed for reference training and 800 per seed for its probe ladder;
overall cap two hours including preparation. Check limits at each training update.
Timeout retains available evidence as inconclusive, with no automatic retry.

## Assessment and next-action rule

Pair per-geometry assessment log losses across both checkpoints and the selected
probe, averaging across all three seeds. Use 2000 cluster-bootstrap draws within
family/density strata, seed 362; preserve paired geometry draws. Positive gain is
comparator loss minus selection-best reference loss. Report seed results and
95% intervals. No independence assumption across rows from one geometry.

- Best versus final lower interval <=0: selection benefit unresolved; investigate
  data coverage and observation controls, without declaring impossibility.
- Best improves over final and beats probe (lower interval >0): investigate encoder
  training/representation under a separate intervention.
- Best improves over final but remains worse than probe (upper interval <0): refine
  reference training before treating it as a useful ceiling.
- Best improves but its probe comparison overlaps zero: report uncertainty, no
  architecture conclusion.

The rule yields proposals, not automatic execution of new interventions. Report
validity separately; leakage, changed frozen state or mismatched manifests invalidate
the affected evidence. All outcomes remain non-promotional.
