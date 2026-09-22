# F-007 — Frozen transfer requires controlled comparison

## Characterization

- Classification: historical methodological requirement
- Status: recorded
- Confidence: high that the source states the requirement

## Finding

The predecessor treats frozen transfer as a hypothesis and requires comparisons with
raw-grid, random-feature, adapted, fully fine-tuned, and from-scratch controls at
matched data and compute.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 explicitly reports mixed precedent for frozen embodied encoders and carries the
control requirement into its evaluation plan and risks.

## Applicability to Model Garden

These controls are necessary to separate benefits of architecture, pretraining, and
optimization from the systems convenience of a frozen checkpoint.

## Limitations and counterevidence

The historical review does not preserve a completed matched comparison or numerical
decision threshold.

## Consequences

Future experiment protocols should preregister matched controls and thresholds before
claiming a transfer benefit.
