---
title: Compact controls evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - perception-encoder-compact-controls.md
  - ../../experiments/compact-encoder-campaign/README.md
  - ../../experiments/compact-encoder-campaign/protocol.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md
  - ../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md
---

> This entry is historical and is not an authoritative specification. The original
> evidence record is preserved below without normalizing its identity-bearing
> revisions, hashes, run name, measurements, limitations, or disposition.

## Archived material

This record captured the outcome of the frozen `compact-controls-v1-run1`
classification-control diagnostic. It reports the probe-fit budget and duration,
comparative control metrics, bounded interpretation, known limitations, external
report location, machine-payload identity, and artifact-handling statement.

## Why it was archived

The evidence became one input to the structured compact perception-encoder campaign.
That campaign now owns navigation, chronology, and current interpretation across the
engineering screens. This record remains immutable provenance for the original
outcome and its exact identifiers rather than current experimental guidance.

## Authority ended

By the 2026-09-22 structured migration, current interpretation moved to the
`compact-encoder-campaign` experiment. This archived outcome does not authorize
additional fits, HPO, encoder updates, certification, promotion, or a merge.

## Current replacement

- [Compact encoder campaign](../../experiments/compact-encoder-campaign/README.md)
- [Campaign protocol map](../../experiments/compact-encoder-campaign/protocol.md)
- [Engineering-screen iteration](../../experiments/compact-encoder-campaign/iterations/engineering-screens/README.md)
- [Engineering-screen execution](../../experiments/compact-encoder-campaign/iterations/engineering-screens/execution.md)
- [Engineering-screen results](../../experiments/compact-encoder-campaign/iterations/engineering-screens/results.md)
- [Engineering-screen evidence index](../../experiments/compact-encoder-campaign/iterations/engineering-screens/evidence/README.md)

## Continuing evidential value

Keep this record to interpret artifacts and reports that cite specs issue 56, Theseo
AnySearch issue 381, protocol `97e205793e6e443199f118b528c0c3fc9181e76c`, source
`3987482`, run `compact-controls-v1-run1`, or machine payload
`05385b70d722dcfa75222e1f62f82b3682bdddd0a46622eba478d357da4bad86`. The frozen
design that governed the run remains in
[the compact-controls protocol](perception-encoder-compact-controls.md).

---

## Preserved historical evidence record

# Compact controls evidence

Specs#56 / implementation#381. Protocol97e205793e6e443199f118b528c0c3fc9181e76c;
source3987482. Run compact-controls-v1-run1,60 fits,79.032 seconds including
preparation. No encoder updates, final test, HPO winner, certification or merge.

Plain1024 probes with selection-only thresholds: compact IoU.190-.230 and
boundary F1.305-.330, compared with spatial.690/.777 and raw neighborhood.633/.638.
Compact AUPRC.233-.264 occupancy/.223-.246 boundary remains near the random-grid
control. Threshold selection repairs many zero scores without closing this gap.
Balanced BCE changes operating points but does not materially improve ranking and
usually worsens probability log loss. Longer probes do not rescue these96-update
smoke checkpoints. Compact training AUPRC is also low, not just held-out scores.

Direction: investigate tiny-corpus compact overfitting and a known geometric-code
decoder control, then position-enriched coordinate/decoder ablations under a new
protocol. Equal small heads face different decoding difficulty for spatial versus
global representations. Do not infer a fundamental128-dimensional capacity limit
or start broad HPO from this diagnostic. Full campaign foundations remain partial.

All comparisons use one seed/two families, central17 queries, fixed masks; controls
are not parameter-matched, random grid is not aggregation-matched, and raw input
is only a3-cubed neighborhood. No distance or wider-field claim. Full report:
docs/perception-compact-controls-assessment.md in implementation repository.
Machine payload05385b70d722dcfa75222e1f62f82b3682bdddd0a46622eba478d357da4bad86.
60 prediction/probe artifacts hashed outside Git.442 full garden tests passed
before additional evidence replay coverage. Disposition retain diagnostic.
