# Compact fresh-scene optimization: first tranche

Issues specs#62 / implementation#389. Authorized unmerged stack on #386. Prior
positive-control protocolfd8eba978a6100b997cc762dbea6078d3b0f5686. User explicitly
authorized up to48 GPU-hours on2026-09-12, not integration merges. This tranche is
development optimization, not certification or the completed campaign.

## Scope and budget

Fix33 input and central17 output. Spatial initializer is validated continuation
seed0. Dense output training is justified by #386 learnability, but fresh-scene
transfer is unproven. No scene ID, generator code or local-feature skip enters
compact readouts. Old global projection remains unused.

Maintain a machine-readable runtime budget ledger:48 hours authorized, reserve one
hour conservatively for preceding compact foundations (measured successful runs
total502.704s; reserve also covers aborted smoke/tests and unmeasured overhead).
Allocate at most8 hours to this tranche, including preparation, all training,
extraction/probing and final development evaluation. Charge wall time of the single
GPU run, conservatively including CPU phases. No simultaneous GPU runs. Interrupted
unsettled reservations remain charged until reconciled, never assumed free. Report
the reserved-versus-measured distinction. Remaining campaign work needs fresh run
contracts, not renewed user approval within the authorized48-hour total.

Each training-plus-readout stage has a900-second limit inside the8-hour tranche.
On resume, an interrupted stage is conservatively charged900s in addition to
previously recorded elapsed time; completed stage checkpoints are reused, not
retrained. Hold an OS-released exclusive ledger lock during execution. Save
optimizer and CUDA-generator state for rung extensions. Individual scenes with
no eligible distance cells contribute zero count, not perfect scores; report
eligible counts. Require at least20 labels of each binary class and a nonempty
distance pool per family/split before optimization.

## Fresh data

Study compact-search-v1. Independent train192/probe384/selection96/development96
parents, balanced over four families and densities .08/.16/.28 (12 strata).
IDs compact-search-v1-<split>-<index:04d>. SHA256 first8 little-endian bytes seed
NumPy.49-cubed parents at coordinates -24..24 divided by8; crop33. Parent quantile
threshold fixes occupancy density once. Targets: parent boundary, occupancy and
nonnegative signed EDT truncated/divided by8; crop central17. No new crop targets.

Families: random_field (Gaussian noise sigma1.5 reflect); oblique_sheets (prior
random-unit-normal sine, frequency[4,8], phase[-pi,pi]); sphere_shells (minimum
absolute distance to two sphere surfaces, centers uniform[-1,1]^3, radii[.4,1.5]);
box_shells (minimum absolute maximum signed slab distance to two boxes, centers
uniform[-1,1]^3, half-extents[.3,1.2]^3). Quantile threshold each parent at the
stratum density. These are synthetic families, not unseen real-world validation.
Reject duplicates; freeze parent/input/target hashes and label support.

Probe/selection/development masks fixed20%, SHA ID plus -mask. Training masks
fresh per update at configuration rate. Query metrics use all eligible central17
cells: hidden occupancy/boundary, visible-free clearance, hidden-free recovery.
Primary comparisons stay central-only; no whole33 or topology claim. Development
data are not opened by the run until configurations/ranking are finalized; reserve
an independent future test set for qualification. The manifest hashes development
data for identity only, never computes candidate metrics before final selection.

## Training and independent readout

Existing three aggregators, dimensions64/128/192, frozen or joint backbone. Training
decoder is linear D -> 3*4913 logits/values. AdamW, batch4, fixed initializer/sample
seeds; exclude old global projection. Occupancy and boundary weighted BCE on hidden
cells, weights derived from training-target prevalence; distance SmoothL1 on all
free central cells. Sum occupancy + configurable boundary/distance weights. Train
head discarded for selection: it is not the representation score.

Independent frozen readout: train-only standardized vector, bias, ridge regression
to all three central target volumes using the independent384 probe scenes. Alpha1
penalizes weights, not bias; solve in float64, no encoder gradients. Predictions
clamp[0,1]. This is a linear dense readout, NOT the original32-hidden query probe;
report parameter count D*14739+14739 and target exposure. It tests linearly decodable
spatial information and cannot certify a small query head or unchanged-head transfer.
Select classification thresholds by pooled selection F1 over.01..99, lower ties.
Distance thresholds absent. Report all four eligible-cell metrics and families.

## Search schedule

Structural screen:18 balanced cells =3 aggregators x3 dimensions x2 backbone modes,
512 updates each, lr.003/wd.01, mask.2, boundary weight1/distance weight10. Select
top two structural cells by frozen ranking. Then18 new hyperparameter trials,
alternating those two cells,512 updates each. Hyperparameter templates drawn before
screening with NumPy RNG389: lr log-uniform[1e-4,3e-3], wd log-uniform[1e-5,1e-2],
mask in[.1,.2,.35], boundary weight[.5,1,2], distance weight[3,10,30]. Values and
template-to-slot rules in manifest before training; only structure binding depends
on selection. No augmentation/search-space changes after observing development.

Extend top six of36 to2048 updates, preserving optimizer/RNG state. Also extend
structural trial IDs5 and16 to2048 regardless of early rank (protected slow-learner
controls fixed before scores). Extend top two among2048-stage candidates to8192.
Rank and lock the final winner using selection alone, then evaluate those two on
development without further selection. These are single-seed direction results;
multi-seed confirmation and independent final tests remain future packages.

Development targets, NOT claimed utility/certification floors: IoU.60, F1.70,
clearance/recovery NMAE.10. Rank lexicographically by number of targets met, minimum
of metric/target (target/error for errors), then mean capped-at2 ratio, smaller D,
and lower trial ID. Every metric stays visible; no aggregate overrides a failed
component. Targets are fixed directional milestones before this run, not inferred
after inspecting winners. If none meets them, report experimental-only and direct
remaining budget to the observed failure mechanism; never lower the targets.

## Validity and reporting

Before optimization: test loss/readout gradients, query/mask isolation, data-group
separation, train-only normalization, resumable checkpoints and ranking. Confirm
ridge recovers a synthetic linear-code fixture. If validity fails, fix before using
scores. Retain prior spatial/raw/random control evidence as context, not as directly
comparable ceilings on these new families. A new matched control/confirmation suite
is required for pretraining-benefit or deployment claims.

Deterministic float32, CPU threads4, TF32/cuDNN autotuning off; explicit deterministic
pooling. Cap checked every update and between bounded extraction/readout phases.
Save each rung's model/optimizer/decoder/RNG and fitted readout/predictions outside
Git, with hashes. Write durable progress after each completed trial so interruption
does not discard completed work. Never restart completed trials without recording
the extra cost. Commit resolved configurations, manifests and compact report.
No final certified checkpoint or automatic promotion from this first tranche.
