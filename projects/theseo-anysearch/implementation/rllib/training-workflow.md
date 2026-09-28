---
title: RLlib training development workflow investigation
status: draft
kind: implementation
owners: [theseo-team]
last_reviewed: 2026-09-28
applies_to: [theseo-anysearch]
related: []
---

# RLlib training development workflow: investigation plan

This is a plan for developing current implementation guidance, not a claim that
the archived design or an unrun test describes today's behavior. Baseline to
inspect: `theseo-anysearch` `develop` at
`fd94554c9620096f94aaed95ffda6a1bbd4711ec`; refresh and record a newer
revision if the audit starts after that commit.

## Purpose and boundary

Explain how contributors develop and verify one training run without duplicating its product contract. The [rllib implementation index](README.md) owns contributor
guidance; subsystem contracts own observable behavior.

## Evidence to inspect

`rllib/trainer/README.md`, `trainer.py`, `lifecycle.py`, `checkpointing.py`, `evaluation/`, `curriculum/`, `reporting/`, `tune/`, and CLI tests; compare archived [module proposal](../../legacy/rllib-module-spec.md).

Read the owning subsystem specifications and their validation pages before
accepting an archived statement. Inspect relevant source and tests at one exact
product revision, then execute focused tests where practical. Record failures
and untested areas rather than assuming coverage from filenames.

## Questions to resolve

Which component owns iteration control, checkpoints, curriculum state, RLlib evaluation scheduling, trajectory capture, and Tune integration? Which modules are active and which are scaffolds? How are continuation, fine-tuning, and evaluation distinguished in current code? What state must tests restore? Audit Ray resource effects and worker execution separately in the [Ray plan](../ray/execution.md).

For each finding, label it **current**, **obsolete**, or **unverified**, and
record the source file, test, and revision supporting that label.

## Repository-specific concepts to classify

- Stage/curriculum state, concurrent evaluation, checkpoint-local auxiliary state,
  trajectory capture, and clone/apply execution recipes.
- Separate RLlib mechanics from AnySearch's orchestration, identities, and
  artifact decisions; point each behavior claim to the owning subsystem.

## Deliverable and acceptance

A source-verified ownership and diagnostic guide, safe local test commands, and a checklist for changes crossing trainer/evaluation/checkpoint boundaries. Contractual semantics remain in [training and tuning](../../subsystems/training-and-tuning/README.md). Replace this plan with accepted contributor guidance only after
source and test evidence has been recorded. Keep unresolved claims explicit and
do not copy historical text into a current rule without review.
