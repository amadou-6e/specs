# F-004 — Reviewed evidence supports retention, not promotion

## Characterization

- Classification: cross-source synthesis
- Status: supported
- Confidence: medium

## Finding

Across the completed audit, robustness assessment, and collision-readout assessment,
the consistent supported disposition is to retain bounded evidence without promoting
an encoder or automatically continuing the architecture program.

## Supporting sources

- [S-001 — Frozen collision-readout assessment](../sources/S-001-collision-readout-assessment.md)
- [S-003 — Frozen compact validation assessment](../sources/S-003-robustness-assessment.md)
- [S-004 — v2r2 R0 result](../sources/S-004-r0-result.md)

## Evidence

The collision assessment reports improvement without competitiveness; the robustness
assessment reports important distribution-shift failures and no promotion; R0 reports
defer before candidate training or architecture comparison.

## Applicability to Model Garden

This synthesis describes the program state represented by these retained records. It
prevents an individual high metric or successful narrow condition from being mistaken
for a package-level qualification outcome.

## Limitations and counterevidence

The sources preserve useful positive evidence, including strong baseline conditions
and improved collision heads. Later experiments not characterized here could supersede
this synthesis. Underlying artifacts were not independently replayed in this pass.

## Consequences

A successor requires an explicit new experiment or decision; this research entry does
not authorize one.
