# Specs

Private source of truth for product, architecture, contract, and UI specifications
across projects.

## Repository layout

- `projects/<slug>/`: project-owned specifications and design artifacts.
- `shared/templates/`: reusable starting points for new specification work.
- `shared/conventions/`: the lifecycle and review rules shared by projects.
- `tools/`: dependency-free scaffolding and validation commands.

BlogHub is the first imported project. Its existing `.spec` layout is preserved under
`projects/blog-hub/` so Draw.io sources, backups, and screenshot references remain
usable. New projects can begin with the smaller standard scaffold.

## Start a project

```bash
python tools/new_project.py example "Example" \
  --source-repository https://github.com/amadou-6e/example
```

Then complete the generated brief and create feature specs as the work becomes
concrete. A specification should explain the problem and observable outcome before
it prescribes implementation.

## Workflow

1. Capture the problem, users, constraints, and evidence in a project or feature brief.
2. Define acceptance criteria that can be verified independently.
3. Add architecture decisions, contracts, and UI component studies where needed.
4. Review the spec for ambiguity, security, operability, accessibility, and migration risk.
5. Link implementation issues and pull requests back to the governing spec.
6. Update the spec when feedback changes the intended behavior; preserve meaningful design history.

See [the specification lifecycle](shared/conventions/spec-lifecycle.md) for status and
review conventions.

## Validate

```bash
python tools/validate_specs.py
```

Validation checks project manifests, temporary files, repository size limits, and
relative Markdown links. GitHub Actions runs the same checks for pull requests.

