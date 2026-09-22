# F-003 — The reusable encoder boundary should remain goal-independent

## Characterization

- Classification: historical design inference
- Status: provisional
- Confidence: medium

## Finding

The predecessor proposes that geometry and observation metadata enter the reusable
encoder while goal and planner state enter a downstream trainable head.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 motivates this split through reuse goals and an analogy to successor features,
while explicitly stating that the proposed latent is not a successor feature.

## Applicability to Model Garden

The boundary could improve checkpoint reuse across planners and task conventions.

## Limitations and counterevidence

The source records a systems argument, not experimental evidence that excluding goal
information improves transfer or downstream quality.

## Consequences

Treat goal independence as an experimental interface hypothesis until a decision and
compatibility contract adopt it.
