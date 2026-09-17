# Frozen 33 to 65 context evidence

Issues specs#49 / theseo-anysearch#374. Governing protocol commit
2f9fa46f3c26f96b9f0e1c05f9fa101a09923ad3. Run voxel-context-65-v1-run1,
source f848db6 (authorized unmerged stack). No merges or promotion.

All four noninferiority checks pass; no gain interval excludes zero positively.
Occupied IoU improvement CI[-.00124,.00678], boundary F1[-.00551,.00883],
clearance error improvement[-.000527,.000482], recovery[-.000571,.000523].
Shared frozen encoder weights support65 central queries, but added context has
no demonstrated benefit over33. Separate adapted heads; no full-volume claim.

Batch4 accepted, total peak CUDA allocation107.70/610.98 MiB at33/65. Forward
latency13.25-15.60/86.70-86.75 ms per batch; local non-isolated measurements.
Elapsed84.797 seconds including preparation. No encoder updates. Corpus on CPU.
Prefer33 for this local task; next investigate tiled wider-output quality/cost
under a fresh contract, without assuming overlap or spatial norms are harmless.

Implementation report: docs/perception-context-65-assessment.md;
machine evidence: docs/perception-encoder-local-geometry/context65-report.json.
Payload SHA25636fef437a4d62fd505e27c39cba7b58c393bc2ca1d387e426d96f0f9ce12704c.
Disposition retain. Topology/P1-P8 remain separate; no certification or promotion.
