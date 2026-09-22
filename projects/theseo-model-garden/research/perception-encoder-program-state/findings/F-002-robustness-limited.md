# F-002 — Broad compact-code robustness was not demonstrated

## Characterization

- Classification: source-reported experimental result
- Status: supported
- Confidence: high

## Finding

The frozen compact encoder missed retained targets across many density, missingness,
noise, unseen-generator, and contiguous-slab conditions; the completed assessment
therefore does not support broad distributional robustness.

## Supporting sources

- [S-002 — Frozen compact robustness and collision-transfer protocol](../sources/S-002-robustness-protocol.md)
- [S-003 — Frozen compact validation assessment](../sources/S-003-robustness-assessment.md)

## Evidence

The protocol defines the frozen encoders, paired conditions, generators, targets, and
limitations. The assessment reports failures in all 21 groups at some extreme density
and noise conditions and severe degradation under the seven-slice unknown slab.

## Applicability to Model Garden

The finding identifies unsupported operating regimes for the retained frozen package.
It informs qualification design for successors using similar fields and masks.

## Limitations and counterevidence

Baseline results remained strong for the original generators and some unseen cases.
The bounded synthetic screen does not establish failure in every downstream domain.

## Consequences

Future qualification should retain explicit distribution-shift and support reporting;
this finding alone does not select a replacement architecture.
