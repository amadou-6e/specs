# F-008 — Promotion requires standalone and downstream evidence

## Characterization

- Classification: historical recommendation
- Status: proposed
- Confidence: medium

## Finding

The predecessor recommends qualifying geometry retention with frozen standalone
probes before evaluating downstream planner performance, and rejects reconstruction
score alone as promotion evidence.

## Supporting sources

- [S-001](../sources/S-001-historical-perception-encoder-review.md)

## Evidence

S-001 separates standalone encoder certification from downstream planner measures and
lists geometric probes, runtime measures, ablations, and acceptance conditions.

## Applicability to Model Garden

The separation can prevent policy optimization or task-specific heads from masking a
weak representation and can make registry evidence easier to interpret.

## Limitations and counterevidence

The historical record does not show that the listed probes predict navigation value,
nor does it supply completed acceptance thresholds or qualification results.

## Consequences

An experiment should link standalone gates to subsequent downstream outcomes and a
decision should define which evidence is required for registry promotion.
