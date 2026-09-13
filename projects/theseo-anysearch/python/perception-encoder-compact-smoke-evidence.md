# Compact C0-C3 smoke evidence

Specs#54 / implementation#379. Governing spec04673aba3906a50c9a51e4631ef910f8a3e767e7;
source d34e534. Campaign foundations remain PARTIAL; this is not HPO or a usable
compact encoder certification. No merges or promotion; #378 scaling is paused.

V1 failed deterministic CUDA adaptive pooling backward. Preserved incomplete;
explicit-bin deterministic replacement and fresh identities used in v2.
V2 completed18 profiles, six short128-dimensional training paths and fresh probes
in43.766 seconds including preparation. Trained grid/strided/attention aggregation
with both frozen and joint backbones, no spatial bypass into query heads.

Batch4 allocated peak108.3-109.0 MiB.96-step frozen fits2.406-2.547 seconds;
joint fits7.657-7.906 seconds. Short local profiles do not establish production
throughput, best aggregation or resource saturation. No precision/cache/concurrency
optimization yet. Only64/128/192 shape/profiling checks; no dimension-quality search.

Five configurations have zero thresholded occupied IoU and boundary F1 at0.5;
grid-joint gives.152/.138. Some null/shuffled controls match or beat distance
predictions. No selection from these scores. Next: class support/probe calibration,
learning curves and full controls, not larger fields or retroactive thresholds.

Required before C4: richer data/corruptions, raw/random/spatial controls, full
input contracts, steady-state batch/worker/cache/precision profiling and calibrated
numeric acceptance.48 GPU-hour budget not launched. No final evaluation accessed.
Implementation assessment: docs/perception-compact-c0c3-assessment.md.
Report payload988ea76cf01b44252cfe3a6d3fc1ca87e2436486de36978a03d4330850eb5d61.
