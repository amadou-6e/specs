---
title: Encoder continuation and context studies
status: complete
kind: experiment
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related:
  - ../../legacy/python/perception-encoder-continuation.md
  - ../../legacy/python/perception-context-scale.md
---

# Encoder continuation and context studies

## Problem statement

The local-geometry program produced a sequence of separately registered studies after
the original encoder screens. The sequence had to determine whether weak readout
results reflected the representation, the supervised reference, or exposure; whether
continued fixed-architecture pretraining retained useful distance information and
transferred to held-out procedural families; and how far the resulting encoder could
be evaluated with larger or tiled spatial context.

## Research questions and hypotheses

1. Can checkpoint selection and reference-training changes establish a credible
   supervised comparator before judging the encoder?
2. Does continued training of the same encoder architecture improve boundary readout
   at matched probe exposure without losing distance information?
3. Do the continued encoders transfer to held-out procedural families without encoder
   updates or new-family probe fitting?
4. Do 33- and 65-cubed inputs, or tiled 33-cubed inputs, preserve central-query quality
   within declared resource limits?

The hypotheses and gates were frozen separately for each ordered iteration. There was
no single preregistered hypothesis covering this entire sequence.

## Scope and non-claims

This entry concerns local-geometry representation diagnostics on procedural voxel
families. It does not certify topology, planning, full-volume prediction, radius-512
operation, real-world transfer, a production deployment, or model promotion. Resource
measurements are local pilot measurements. The grouping records research dependency;
it does not create a post-hoc aggregate score or shared pass threshold.

## Status and summarized outcome

Status: `complete`.

The sequence established a stronger reference, improved the fixed architecture through
continued training, retained both distance readouts, and passed the registered held-out
family checks. Shared frozen weights remained viable at 33 and 65 input sizes for the
central queries tested. Tiled 33-cubed inference preserved registered quality but was
substantially slower and was retained only as a memory-limited option. These outcomes
are bounded to the registered tasks and do not constitute promotion.

## Documents

- [Retrospective protocol map](protocol.md)
- [Consolidated sources](sources.md)
- [Ordered iterations](iterations/README.md)
