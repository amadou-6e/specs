# Research method

## Questions

This reconstruction asks what the retained perception-encoder records say about
qualification, robustness, collision transfer, and program continuation.

## Non-questions

It does not rerun experiments, inspect uncommitted runtime artifacts, compare new
architectures, or decide whether an encoder should be promoted.

## Search strategy

On 2026-09-22, the existing single-file state review was used to identify its four
named local evidence records under `legacy/python/`. No external web search, database
search, or literature search was performed. The original historical discovery method
for those records is unknown and is not reconstructed here.

Included material had to be directly linked by the prior state review and contain a
protocol, result, assessment, or disposition relevant to the program state. Adjacent
implementation issues, pull-request conversations, runtime directories, and reports
not retained in this specs checkout were excluded from direct inspection.

## Inspection method

The four local Markdown records were inspected as repository documents. Their stated
identities, numerical results, limitations, and dispositions were extracted. This pass
did not execute commands described by the records, recompute hashes, open runtime-only
arrays, or independently reproduce their measurements. Accordingly, experimental
measurements remain source-reported results, while file locations and document content
are directly verified repository facts.

## Evaluation method

Each claim is classified as a directly verified repository fact, a source-reported
experimental result, or a cross-record synthesis. Confidence is high when a completed
assessment gives an explicit outcome and limitation, and medium for synthesis across
records whose underlying artifacts were not independently replayed in this pass.
Conflicts would be preserved rather than resolved by chronology; no material conflict
was found among the four dispositions.

## Limitations

- Runtime-only weights, corpora, predictions, and arrays were not available for this
  documentation pass.
- Referenced implementation commits, GitHub reviews, and machine-readable reports were
  not independently inspected.
- The retained records describe synthetic distributions and bounded studies, not a
  general deployment population.
- This reconstruction cannot validate experimental correctness beyond the evidence
  and internal caveats recorded by its sources.
