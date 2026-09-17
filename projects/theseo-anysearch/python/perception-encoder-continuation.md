# Fixed-architecture encoder continuation

Issues specs#41 / theseo-anysearch#366. User authorizes continued execution and
stacking on unmerged exp/364; no integration merges. Separate experiment from
reference refinement at specs commit 44b089b58db3b9af45820cb358033c6a4acbc99f.
Do not alter previous verdicts or reopen the topology program.

## Comparisons

Three seeds, same fresh probe selection/assessment sets for all arms:

- Existing LG2 encoder, probe fit on 48 geometries.
- Same existing encoder, probe fit on 192 geometries at the same update budget.
- Newly pretrained encoder of the exact same architecture, probe fit on 192.
- Strong supervised reference using the previously selected dynamic/192/lr0.003
  recipe, checkpoint selection as in reference refinement.

New encoders start from fresh seed initializations, not LG2 checkpoints. Pretrain
on 192 separate geometries for 2048 updates, batch eight, AdamW lr0.003/wd0.01.
Use fresh label-independent Bernoulli(0.20) masks each update. Objective is the
existing LG2 joint loss: hidden occupancy BCE plus 10 times SmoothL1 on normalized
ESDF (truncation eight, divide by eight). Attach a two-channel 1x1x1 training head
to eight local feature channels. Global projection remains untrained/out of scope.
Freeze final encoder weights after pretraining; no boundary-assessment selection
of encoder checkpoints. Probe heads alone train afterward.

Keep the linear/32/128 probe ladder and 1024 updates per capacity, AdamW
lr0.001/wd0.01, batch1024. Train-only normalization. Choose capacity by selection
log loss, then calibrate F1 threshold using selection only as in prior protocols.
The new-192 versus old-192 comparison has matched probe exposure. It evaluates a
pretraining bundle, not an isolated effect of learning rate or dataset composition.

## Identities and bounds

Study `voxel-encoder-continuation-v1`; dataset
`voxel-encoder-continuation-v1-development-1`. Pretrain192 /probe-train192 /
selection48 /assessment48 geometries, same four procedural families and density
strata. All splits disjoint by content hash; reject overlap with the prior reference
refinement campaign. CPU mask/query streams 36600/36601/36602/36603; encoder
training random stream 36610+seed. Fixed observation/query support rules unchanged.

Freeze source/spec commits, corpus/query/target hashes, prior-registration hash,
old encoder file/state hashes and resolved configuration before fitting. Verify
loaded and post-probe encoder states. Save new checkpoints untracked with report
hashes. D0 reruns. Maximum900 seconds per reference, encoder or probe-ladder fit;
overall7200 seconds including preparation, no automatic retries or expansions.
Validity failures stop affected evidence; timeout retains inconclusive results.

## Assessment

Paired per-geometry boundary log loss, averaged across all three seeds; 2000
cluster-bootstrap draws within family/density strata, seed362. Report old192 versus
old48 gain, new192 versus old192 gain, and new192 versus reference gain, positive
favoring the first named model. If the new versus old192 lower95% bound exceeds
zero, proceed toward distance-retention and new-family validation. Otherwise retain
the old encoder and investigate objective/readout limitations. Exposure results
inform interpretation but never permit changing completed thresholds.

Report F1 and per-family scores as diagnostics. This surface-only experiment does
not validate distance retention, general encoder quality, unseen-family transfer,
topology, planning or radius scaling. No promotion follows from any outcome.
