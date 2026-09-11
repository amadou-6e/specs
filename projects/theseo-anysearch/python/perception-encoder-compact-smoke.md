# Compact C0-C3 engineering smoke contract

Issue theseo-anysearch#379; specs#54. Parent plan commit
4df18c69ee81c2c2ebd383b7eab615ae7583a6b3. Authorized unmerged implementation stack
on #376. This bounded engineering run does not start the48 GPU-hour HPO campaign.

Study compact-c0c3-smoke-v2. Fresh development-only train/probe/development splits,
12 distinct49-cubed parents each; two existing stationary generators (random_field,
oblique_sheets) and densities.08/.16/.28 in the context-scale order. Scene ID
compact-c0c3-smoke-v2-<split>-<index:03d>; SHA-seeded generator and independent20%
mask. Parent boundary and distance targets, truncation/divisor8. Crop33 input;
256 central17 queries/task, seed37900+split index, same eligibility as context
pilots, replacement only for undersized nonempty pools. Fixed masks are deliberate
for this smoke; not a final augmentation policy. No final test set is opened.

Profile aggregation designs grid/strided/attention at64/128/192, batch1 and4,
three warmups and10 synchronized float32 forwards including input transfer.
Grid: ordered5-cubed pooling, MLP1000->128->D with SiLU. Strided: two3-cubed
stride2 padded convolutions8->16->32 with SiLU, ordered3-cubed pooling, linear toD.
Attention:5-cubed pooled tokens8->32, learned positional embeddings, four learned
queries, four attention heads, flattened128->D. Spatial backbone unchanged.

Train all three128-dimensional variants in both frozen and joint backbone modes,
seed0 source encoder verified against continuation report.96 updates, batch4,
AdamW.001/wd.01, shared sample RNG379. Four separate32-hidden SiLU query heads;
input is only compact vector and central coordinates normalized[-1,1]. Sum two
binary BCE losses and10 times each of two distance SmoothL1 losses. No spatial
auxiliary loss. Old global projection never trained or used for compact output.

Discard training heads, freeze encoder/aggregation and fit fresh fixed32-hidden
probes for128 updates using existing AdamW.001/wd.01,batch1024, train-only feature
normalization. Classification threshold.5; no tuning. Report trained, zeroed and
cyclically shuffled development vectors with fixed heads; these ablations are
engineering diagnostics, not calibrated selectivity or usefulness gates.

Verify shapes, hidden-truth isolation, gradient reachability, frozen-state integrity,
finite outputs and serialization. Pin source/spec/data/checkpoint hashes before
execution.20-minute overall cap including registration preparation; check between
bounded operations and every training update. One GPU process, CPU threads4,
deterministic float32, TF32/autotuning disabled. No architecture ranking, certified
quality, seed-robustness claim, or promotion from96-step training.

Output cost ledger and compact report; weights outside Git. C0-C3 remain partial
until production data/control coverage, detailed numerical comparisons, caching,
batch/worker/precision benchmarks and actual campaign contracts are completed.
This smoke has no claim to exhaustively use or optimize all hardware resources.

## Engineering deviation: deterministic pooling

The v1 run stopped during grid joint-training because adaptive_avg_pool3d backward
has no deterministic CUDA implementation. Its partial output is invalid for quality
or cost comparisons. Preserve its manifest and partial artifacts; do not resume or
select configurations from it. V2 uses fresh data/registration/run identities and
explicit separable averages over the same adaptive bins, with tested forward and
gradient equivalence. Deterministic execution remains enabled. Source/spec pins
must be renewed before the replacement run.
