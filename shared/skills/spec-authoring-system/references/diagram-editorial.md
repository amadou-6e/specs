# Editorial pass for workflow diagrams

Apply this pass before the first user-facing diagram, rather than waiting for
separate requests to categorize, mark, structure, and resize its nodes. Revisit
it after substantive edits. It refines presentation; it does not authorize new
product behavior or replace the owning diagram conventions.

## 1. Find card categories using few-shot examples

Start with several concrete operations from the workflow. Propose a small set
of categories that explains them, then check ambiguous operations with the
user. Keep category meanings consistent across the graph.

In the Laomedo journey, responsibility became the card category, not a repeated
`Actor/owner` field. These examples illustrate that choice:

| Example | Responsibility category | Structural type |
| --- | --- | --- |
| Select an agent and prompt | User | Action |
| Address PR review comments | Agent | Action |
| Present the run summary | Laomedo | Action |
| GitHub pull request | External service | Artifact |

Categories answer who is responsible; structural types answer what a node is.
An action may be a rectangle, a decision a diamond, an artifact a document,
and a continuation a capsule. Do not confuse either dimension with phase,
success/failure state, or grouping. Group adjacent operations into meaningful
phase subgraphs when useful. Split a mixed operation and its resulting artifact
when they have different responsibilities or roles.

Use categories appropriate to the actual project. These four are examples,
not a mandatory taxonomy. Do not guess an owner to make the graph complete;
record the uncertainty or ask a focused question.

## 2. Mark the categories consistently

Give cards a recognizable category header and, where supported, a distinct icon
and restrained color. Include a legend. Do not rely on color alone. For example,
Laomedo used user, agent, application, and external-service markers while
retaining diamonds for decisions and document shapes for artifacts.

Check that icons survive generation/export and that their meaning is clear.
Avoid adding a redundant owner field when the category already conveys it.

## 3. Find useful fields for each card type

Choose fields from the information a reader needs to understand the operation,
not from an assumed runtime schema. Try them on a few populated cards before
applying them everywhere. A useful starting point is:

- A short title naming the operation or artifact.
- `IN:` the input or context required.
- `OUT:` the result or handoff produced.
- `DETAIL:` a relevant choice, constraint, or unresolved point, only when useful.

For example:

> User · Select agent  
> IN: Selected issue; available agents  
> OUT: Chosen agent  
> DETAIL: Recommended prompt templates and skills are available

> Agent · Address review comments  
> IN: PR reference; hint that review comments exist  
> OUT: Updated work on the existing PR  
> DETAIL: User chooses a new or existing session

> External service · GitHub PR  
> IN: Published changes  
> OUT: Reviewable pull request and comments

These are illustrative, not additional requirements. Use only confirmed facts;
mark unknowns explicitly. Artifact fields may describe contents and consumers;
decision nodes usually need only a short question and labeled outgoing choices.
Do not force full card fields into every diamond.

Left-align card text with consistent padding and put a colon after every field
marker. Keep titles visually distinct. Short decision questions may stay centered.
Check wrapping at the intended reading scale instead of shrinking text to fit.

## 4. Normalize decision diamonds after layout

For decision trees, choose one diamond size large enough for the longest wrapped
decision question, then apply it to all comparable decisions, including legend
examples. The size is diagram-specific; do not hard-code Laomedo's dimensions
as a universal rule.

Perform automatic layout first, then normalize diamonds while preserving their
centers. If a diamond changes from width/height `w,h` to `W,H`, adjust its origin
by `(w-W)/2,(h-H)/2`. A later layout pass may undo this, so recheck afterward.
Recompute enclosing group bounds and inspect connected edge routes and labels;
stale waypoints can cause crossings, obscured nodes, or misleading arrow paths.

## 5. Inspect the result and hand off

Render and inspect every changed page both at full-page scale and at readable
card scale. Check category recognition, icon rendering, field punctuation,
alignment, equal diamonds, clipping, edge direction, and subgraph boundaries.
Fix and rerender problems; XML or structural validation alone is insufficient.

Keep the editable source in its canonical specification location. Use temporary
exports only for inspection, following repository guidance; do not put spec
sources or administrative scratch work in an experiment-results directory.
Preserve uncommitted user edits and keep derived sources consistent with the
owning diagram's authority rules.

This procedure captures the Laomedo refinement sequence: initially untyped
nodes became marked categories; responsibility moved from a proposed field to
the card header; cards gained explicit inputs, outputs, and details; decisions
were made uniform; card text was left-aligned with colon-delimited markers.
The goal is to apply those editorial checks from the start, not reproduce the
original back-and-forth. See the
[worked journey](../../../../projects/laomedo/architecture/user-traversal.md).
