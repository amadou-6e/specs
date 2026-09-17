---
title: Replay tab
status: template
kind: ui-design
owners: [theseo-team]
last_reviewed: YYYY-MM-DD
applies_to: [theseo-anysearch]
related: []
---

# Replay tab

This folder is copied and renamed for one independently navigable tab or window. Add
the reviewed editable `design.drawio` beside this README; it is the sole authority for
visual geometry, component states, interaction identifiers, and transitions.

## Surface type and ownership

State whether this is a tab or window, which subsystem owns its behavior, and which
application shell or parent flow opens it.

## Purpose

Describe the user goal and the decisions this surface supports.

## Entry and exit

List every supported way to open, leave, close, or switch away from the surface.

## States

Index the named Draw.io pages or layers for empty, loading, ready, error, disabled,
and selection-dependent states. Do not define states only in prose.

## Interactions and transitions

Index stable interaction identifiers from Draw.io and their destination states or
surfaces. Link the subsystem contract for underlying product behavior.

## Owned elements

List panels, dialogs, sidebars, and components whose lifecycle belongs solely to this
surface. Put their detailed studies under `components/` when necessary.

## Shared dependencies

Link shared shell chrome or components and explain why they have no single surface
owner.

## References and captures

Keep source screenshots used for fidelity comparison in `references/`. Keep reviewed
renders and implementation comparisons in `captures/`. Neither replaces editable
Draw.io geometry.

## Validation

Record component-level and full-surface visual inspection, expected viewport sizes,
keyboard navigation, accessibility checks, and implementation comparison status.
