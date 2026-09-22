# F-002 — Occupancy states require explicit semantics

## Characterization

- Classification: historical project requirement
- Status: recorded
- Confidence: high that the source defines this requirement

## Finding

The predecessor requires representations to distinguish occupied, known-free,
unknown, and out-of-observation or invalid space rather than treating absent sparse
coordinates as free.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 states the semantic distinction as a project constraint and repeats it in the
proposed input and checkpoint contracts.

## Applicability to Model Garden

The distinction is directly relevant to encoder compatibility and safe checkpoint
reuse across observation producers.

## Limitations and counterevidence

The source does not demonstrate that its proposed four-channel encoding is minimal or
optimal, and this migration did not inspect the current runtime contract.

## Consequences

Any experiment should test semantic preservation explicitly and reject silent
occupied, unknown, or invalid-to-free conversion.
