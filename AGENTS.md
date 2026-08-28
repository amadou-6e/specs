# Agent guidance

This repository contains specifications, not product implementation. Prefer changes
that make intent, behavior, constraints, and verification clearer.

## Working rules

- Read the project manifest and nearby specifications before editing.
- Preserve project-specific organization unless a migration is explicitly requested.
- Do not overwrite user-authored Draw.io changes. Inspect the current Git diff before
  editing and use branches and commits for design history; do not create backup copies.
- Keep reference screenshots beside their Draw.io workshop when they are used for
  fidelity comparison.
- Keep view-specific components under `projects/<slug>/views/<view>/ui/components/`.
  Use `projects/<slug>/ui/shared/` only for components with no single view owner.
- Keep live screenshots in `references/` and superseded multi-view studies in
  `ui/archive/`. Do not track Draw.io exports; generate them temporarily for visual
  inspection and discard them after review.
- Use editable geometry for UI proposals; screenshots are references, not substitutes.
- Visually inspect Draw.io changes at component level and at full-page scale.
- Record unresolved decisions explicitly instead of inventing product behavior.
- Never add credentials, browser profiles, cookies, tokens, or captured login URLs.
- Do not vendor generated caches, virtual environments, model weights, dependency
  trees, or cloned upstream repositories.
- Run `python tools/validate_specs.py` before committing.

## Change workflow

Problem or feedback -> specification issue -> typed issue branch -> spec and evidence
-> validation -> pull request -> review -> merge.

Use `<type>/<issue-number>` branches, for example `feat/12`, `fix/18`, `docs/21`, or
`chore/24`. Pull requests should link the issue and identify the specifications whose
status or behavior changed.
