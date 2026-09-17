# Context-scale pilot evidence

Issues specs#47 / theseo-anysearch#372. Frozen protocol
`b950249860b3e33640e9faadc3fe0a7ecabc92fc`; executable `6dea43e`.

Completed17/33 fixed-resolution paired pilot, three seeds, frozen and retrained
arms. Shared frozen encoder at33 improved all four central-query tasks with
positive paired intervals. Boundary F1 rose from0.696-0.722 to0.739-0.756;
IoU from0.660-0.679 to0.687-0.717. Distances also improved.

Short512-update retraining did not beat the established frozen33 encoder on
surface tasks. Retain shared weights as the working direction. A separately
registered65-cubed frozen/resource check is next, not automatic execution or a
claim about radius512. Probes were scale-adapted; full-volume accuracy untested.

Batch4 incremental inference allocation rose from9.93 to72.91 MiB. Short timing
measurements are noisy and not production scaling guarantees. Recorded whole
run duration247.15s; no out-of-memory error.

Report payload `e66dfdecf165ee75bbf6255741968d3acb3457a696f9b851a385c444af062bfe`.
Implementation assessment: docs/perception-context-scale-assessment.md.
All weights/corpora remain untracked; no promotion or integration merges.
