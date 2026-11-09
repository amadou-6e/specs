# Specs

Private source of truth for product, architecture, contract, and UI specifications
across projects.

## Repository layout

- `projects/<slug>/`: project-owned specifications and design artifacts.
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

The command creates a minimal bootstrap, not a typed authoring system. Define the
project's ownership and structure with the
[authoring overview](shared/skills/spec-authoring-system/references/workflow.md),
then use its project-owned category templates. The
[typed-folder example](shared/conventions/typed_folder_system/example/projects/example-project/SPECS.md)
demonstrates all three structural types. A specification should explain the
problem and observable outcome before it prescribes implementation.

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

## Validate

```bash
python tools/validate_specs.py
```

Validation checks project manifests, temporary files, repository size limits, and
relative Markdown links. GitHub Actions runs the same checks for pull requests.

## Trace report

```bash
python tools/trace_graph.py [--json graph.json] [--stale-days 180]
```

A read-only traceability report built from frontmatter, relative links, and
interaction IDs in visible Draw.io labels (ranges such as `ED-06–10` and lists such
as `CA-06/07` are expanded). It lists diagram IDs that Markdown does not project,
Markdown IDs absent from the current diagrams, interactions not cited by ID in
`ui-tests.md`, lifecycle status drift, stale reviews, and unlinked documents.
Findings are review prompts; the command always exits 0 and is not a CI check.
Run its tests with `python -m unittest discover -s tools -p "test_*.py"`.
