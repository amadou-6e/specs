# F-003 — Revised collision heads did not establish competitiveness

## Characterization

- Classification: source-reported experimental result
- Status: supported
- Confidence: high

## Finding

All three revised collision heads passed the registered within-compact-code improvement
screen across three seeds, but none passed competitiveness against raw-grid and spatial
controls.

## Supporting sources

- [S-001 — Frozen collision-readout assessment](../sources/S-001-collision-readout-assessment.md)

## Evidence

The assessment records 21 fitted heads, 90 locked prediction groups, frozen encoder and
normalization weights, and the explicit retain-without-promotion disposition.

## Applicability to Model Garden

The result shows that readout design can recover additional collision signal from the
unchanged compact code under this study, while leaving the core competitiveness
question unresolved negatively under its controls.

## Limitations and counterevidence

The work does not test navigation, global reachability, continuous collision, sensor
noise, or larger fields. Improvement over an older compact head is genuine evidence,
but it is not evidence of superiority to stronger spatial inputs.

## Consequences

Retain the readout evidence. Do not infer that encoder retraining or artifact promotion
was authorized.
