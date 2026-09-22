---
title: Held-out family evidence
status: archived
kind: legacy
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
supersedes: null
related:
  - ../../experiments/encoder-continuation-and-context/iterations/006-family-transfer/README.md
  - perception-family-transfer.md
---

# Held-out family evidence

> This entry is historical and is not an authoritative specification. The structured
> experiment iteration linked below owns the current interpretation of this evidence.

## Archived material

This record preserves the outcome summary and artifact identity for the frozen
`voxel-family-transfer-v1` study. It records the observed metric ranges, the gate
verdict, the implementation revision, the governing specification revision, the
report-payload hash, and the original artifact-tracking statement.

## Why it was archived

The evidence was imported from the former flat Python specification corpus. The
study is now represented as iteration `006-family-transfer` in the structured
`encoder-continuation-and-context` experiment. Current interpretation and future
work belong with that experiment rather than this preserved evidence record.

## Authority ended

Authority ended when the family-transfer study was incorporated into the structured
experiment entry. The inspected historical evidence does not establish the exact
date of that migration, so this archive does not invent one.

## Current replacement

- [006 — Held-out procedural-family transfer](../../experiments/encoder-continuation-and-context/iterations/006-family-transfer/README.md)
- [Current execution record](../../experiments/encoder-continuation-and-context/iterations/006-family-transfer/execution.md)
- [Current results record](../../experiments/encoder-continuation-and-context/iterations/006-family-transfer/results.md)
- [Archived frozen protocol](perception-family-transfer.md)

## Continuing evidential value

This record remains useful for checking historical claims against the exact governing
and executable revisions and the report-payload identity. It also preserves the
original scope limitation: the result supported transfer to the two registered
procedural families, not topology, promotion, universal transfer, or real-world
generalization.

## Preserved historical evidence

Issues specs#45 / theseo-anysearch#370. Protocol frozen at
`bc3a092d07309eb8f22390bd2878f371713badad`, executable `1a73724`.

Completed `transfer_supported`: all eight family/task checks passed on every seed.
New boundary F1 shells 0.783-0.805, labyrinths 0.769-0.781; occupancy IoU
0.869-0.878 and 0.793-0.810 respectively. Both distance tasks passed on both
families. All paired improvement intervals favor the new encoders.

Probes were fitted/threshold-selected only on the original four families; no
new-family adaptation and zero encoder updates. Fixed 32-hidden probes, matched
old/new exposure. Retain new local encoders as candidates for scale/context tests,
not as universal or real-world encoders. No topology or promotion claim follows.

Full implementation assessment: docs/perception-family-transfer-assessment.md.
Report payload `f48a2741debf123070493623f078fd8832cc6900bcd9855fe54f07669f26124c`.
Recorded duration 37.94s; all 24 probe artifacts remain untracked and hashed.
