# D0-D2 execution evidence

Specification issue specs#35; execution issue theseo-anysearch#360.
Protocol frozen at `66279ceab743af9c350107fe26fca730d2b245fe`; this evidence does
not change that protocol. Source `ebb0e44` in theseo-anysearch, branch exp/360.

The registered boundary-only campaign completed in 74.86 recorded seconds on
RTX 3060 Ti. D0 passed all seeds. D1 reference F1 was 0.3998/0.4373/0.4219;
D2 selected frozen-feature heads scored 0.6005/0.6032/0.6160. Neither met 0.70.
All three seeds selected the 128-unit head using selection log loss only.
There were zero encoder updates. Data identities and checkpoint hashes were
frozen before fitting. Existing LG3 evaluation instances were not reused.

The diagnostic router returns `reference_unresolved`, proposing D3, not global
research termination. Reference training losses approach zero while selection
losses rise, demonstrating overfitting. D2 beats the null in log loss: paired
stratified geometry-cluster 95% gain CI [0.1289, 0.1568]; D1 is worse than null.
This is not evidence that topology or surface targets are unidentifiable.

Next proposed refinement: address the reference's observed overfitting with a
preregistered matched-compute selection-checkpoint comparison on fresh development
instances before attributing the failure to observation or resolution. This is
not an adopted intervention or a completed D3 result. No model is promoted.

Full assessment and machine-readable report are maintained in the implementation
PR for #360 at `docs/perception-encoder-diagnostics-assessment.md` and
`docs/perception-encoder-local-geometry/diagnostics-report.json` respectively.
Report payload SHA256:
`f3e74cce9bad0aebde02f24f15e082a2f7e6ad9c7261cba71be3c7bfe38b51d9`.
Weights and prediction artifacts remain untracked; their hashes are in the report.
