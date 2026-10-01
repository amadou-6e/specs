# Specs

Private source of truth for product, architecture, contract, and UI specifications
across projects.

## Repository layout

- `projects/<slug>/`: project-owned specifications and design artifacts.
- `shared/templates/`: reusable starting points for new specification work.
- `shared/conventions/`: the lifecycle and review rules shared by projects.
- `shared/skills/`: reusable agent workflows for researching and writing specs.
- `tools/`: dependency-free scaffolding and validation commands.

BlogHub is the first imported project. Its specifications live under
`projects/blog-hub/`; UI sources are owned by their corresponding view, while shared
flows and historical baselines live under `projects/blog-hub/ui/`.

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

See [the specification lifecycle](shared/conventions/spec_lifecycle.md) for status and
review conventions, and [the typed and named folder hierarchy](shared/conventions/typed_folder_system/README.md)
for how categories and entries are structured.

For collaborative project definition, use the
[define-project-spec skill](shared/skills/define-project-spec/SKILL.md). It guides
user scenarios, ownership, category selection and populated template adaptation.

## Validate

```bash
python tools/validate_specs.py
```

Validation checks project manifests, temporary files, repository size limits, and
relative Markdown links. GitHub Actions runs the same checks for pull requests.
