# Compact learnability evidence

Specs#58 / implementation#385. Protocol1bf1359b55b7c9aef2de1fe23a831e2e850009e0,
source91d50ad. Run compact-learnability-v1-run1,303.141 seconds, six2048-step fits.
All failed overfit IoU.95/F1.97 targets. Plain32 IoU about.20 for oracle/table/encoder;
Fourier128 IoU.242 oracle/.374 table/.334 encoder. Analytic oracle exactly recovers
all targets: code information sufficiency does not guarantee learned readout success.

Next action already prepared: specs#60 / implementation#386 direct dense-output
positive control, fresh data, no coordinate-query decoder. These results cannot
establish insufficient128-dimensional capacity or generalization. Four scenes,
one seed, visible+hidden training labels; Fourier/capacity bundled change.
447 garden tests passed; final states/predictions hashed outside Git. Disposition
retain diagnostic. No merge, HPO winner or certification. Full report:
docs/perception-compact-learnability-assessment.md in implementation repository.
Machine payload00e7511e6dd9ba360140428fc249689b9f7c5db0dab62b28bd226f58123ea256.
