---
name: model-garden-experiment-specification
description: Create, reconstruct, or revise a Model Garden experiment specification with a frozen protocol, ordered iterations, reproducible execution evidence, decision gates, bounded results, and replication records.
---

# Maintain a Model Garden experiment specification

Use the [experiment template](template/README.md) for file ownership and cardinality,
and the project [SPECS.md](../SPECS.md) for category boundaries. An experiment answers
bounded research questions under explicit decision rules. Its documents preserve what
was planned, what actually ran, what evidence was produced, and what may be concluded
without collapsing those different authorities into one narrative.

This skill governs experiment documentation. It does not authorize launching,
stopping, rerunning, or modifying an experiment or its external artifacts unless the
user separately requests those actions.

## Establish scope and evidence

- Read the experiment entry, governing protocol, every registered iteration, source
  list, raw reports or manifests, relevant implementation and configuration revisions,
  and linked subsystem, decision, and research specifications.
- Determine whether the work is one experiment with several iterations, a
  sub-experiment governed by the same protocol, or a separate experiment answering a
  different question. Do not split retries into independent studies or combine runs
  governed by materially different questions and decision rules.
- Distinguish planned work, executed work, reported evidence, interpretation, and
  accepted product decisions. An experiment result is evidence; it does not promote a
  model, configuration, or implementation into the product without a separate decision.
- Preserve negative results, failed gates, abandoned attempts, deviations, and
  uncertainty. Do not rewrite history to make the final iteration appear to have been
  the original plan.

## Define the experiment root

- In `README.md`, state the decision-relevant problem, bounded research questions,
  falsifiable hypotheses where applicable, scope, non-claims, current status, and a
  concise outcome only after results exist. Use only the experiment lifecycle values
  `planned`, `running`, `complete`, `replicated`, or `superseded`.
- Keep one `protocol.md` for the experiment. Before decision-bearing observations,
  define variables, controls, baselines, data/world/task splits, seeds, sample sizes,
  metrics, thresholds, stop conditions, decision gates, sub-experiments, permitted
  adaptations, iteration behavior, forbidden post-hoc changes, analysis, resource
  budget, and threats to validity. Pin its governing revision.
- Keep one consolidated `sources.md` covering code and spec revisions, datasets,
  artifacts, prior experiments, and literature used anywhere in the entry. Identify
  source roles and limitations rather than providing an unqualified link dump.
- Do not call a protocol frozen if decision-bearing results were already inspected
  before its rules were fixed. Record that limitation and treat later changes as a
  new authorized iteration or revised experiment, as appropriate.

## Preserve ordered iterations

- Create `iterations/` when the first attempt starts. Give each attempt an ordered,
  stable identifier and record its role, status, predecessor, authorizing protocol
  gate, and permitted differences in its `README.md`.
- Use `execution.md` for what actually happened: exact protocol, code, dependency,
  data, task, world, checkpoint, and artifact identities; commands; seeds; hardware;
  timestamps; failures; reruns; resource use; and every deviation. Never silently
  edit the parent protocol to match an execution.
- Use `evidence/README.md` as the manifest for raw reports, logs, checkpoints,
  visualizations, and external artifacts. Keep large/generated artifacts outside the
  specs repository and record stable identity, location, provenance, and retention
  information sufficient to find and verify them.
- Add `results.md` when an iteration concludes. Report primary and per-seed results,
  uncertainty, baseline comparisons, each passed or failed gate, negative findings,
  unexpected observations, interpretation, non-claims, and the disposition dictated
  by the frozen protocol. Link evidence rather than copying large outputs.
- Add `replication.md` only when the iteration performs a reproducibility or
  replication check. Distinguish identical-input reruns from fresh-seed, fresh-data,
  fresh-world, or independent-implementation replication and state tolerances and
  determinism limits.

## Apply gates without hindsight

- Evaluate every stop and decision gate exactly against its specified metric,
  population, aggregation, threshold, and evaluation point. A high headline metric
  does not override a failed baseline comparison, confidence requirement, subgroup
  gate, or other predeclared criterion.
- If a gate cannot be evaluated because evidence is missing or invalid, report it as
  unevaluable. Do not count it as passed or failed by inference.
- Treat exploratory analyses performed after results are observed as exploratory.
  They may motivate a permitted next iteration or a new experiment, but must not be
  presented as preregistered evidence.
- Record the disposition the protocol requires. If the team chooses a different
  action, identify it as a decision outside the experiment rather than modifying the
  result to justify it.

## Reconstruct historical experiments carefully

- When migrating existing runs, preserve their original configuration, logs, reports,
  branches, commits, and artifact identities. State which facts are directly evidenced
  and which are reconstructed from incomplete records.
- When migrating a flat legacy document, preserve the original unmodified as
  `imported-<name>.md` beside the required experiment files and use thin, explicitly
  labeled `README.md` or `protocol.md` wrappers until its content is fully absorbed.
  Use a local `imported-<name>.md` wrapper when a Model Garden entry needs this
  convention. Section merging
  is acceptable only in an explicitly incomplete migration; restore the template's
  distinct question, scope/non-claim, and status/outcome sections before activation.
- Do not invent a frozen protocol retroactively. A retrospective protocol may
  describe the apparent design, but it must disclose that decision rules were not
  fixed before results were known.
- Keep multiple historical attempts as separate iterations when their execution or
  evidence can be distinguished. Do not manufacture aggregate statistics across
  incompatible runs merely because they concern the same model or task.
- Encoder-pretraining and qualification experiments belong here even when their code
  ran from an AnySearch checkout. Preserve the implementation repository and revision
  as execution provenance rather than relocating the experiment to the consumer.

## Review and validate

- Check that the overview, protocol, sources, iteration records, evidence, results,
  and replication claims agree; all claimed runs have identities; all conclusions
  trace to evidence; and every gate has an explicit disposition.
- Check that result language stays within the experiment's scope and that proposed
  product changes link to decisions or subsystem work rather than becoming implicit
  experiment conclusions.
- Perform a replication-reader pass: another contributor should be able to identify
  what to run, with which inputs and revisions, on what hardware assumptions, and how
  to judge success without reconstructing context from chat or TensorBoard alone.
- Run the specs repository validator. Report documents changed, evidence inspected,
  commands actually run, unavailable artifacts, and remaining threats or uncertainty.
