# Explainability request configuration

This page describes behaviorally significant request choices rather than experiment
training configuration.

A request selects run/checkpoint, algorithm, state source, step selection, action
target, feature grouping, background, and output destination. Defaults must be recorded
in the emitted report so identical artifacts can be reproduced.

Background `auto` selects trace for a multi-step source and zeros for a single step.
Explicit trace or mean requires two or more observations. Scenario provenance controls
the validation label and must not be overridden by a display option. Output paths do
not change explanation identity, while checkpoint, state, grouping, score target, and
background do.
