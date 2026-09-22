# Specification lifecycle

## Statuses

- `discovery`: the problem and constraints are still being investigated.
- `draft`: a concrete proposal exists and needs feedback.
- `review`: scope, behavior, and acceptance criteria are ready for approval.
- `accepted`: the specification is approved for implementation.
- `implemented`: the accepted behavior is available and verified.
- `superseded`: a newer specification replaces this one; link to it.
- `archived`: the specification no longer governs active behavior.

Project manifests use `active`, `paused`, or `archived` for the project as a whole.

## Minimum useful feature spec

A feature spec should identify:

- The problem and affected users.
- Current and expected behavior.
- Scope and explicit non-goals.
- Acceptance criteria with observable outcomes.
- Relevant data, API, UI, security, and operational implications.
- Open decisions and implementation dependencies.
- Links to evidence, diagrams, issues, and pull requests.

## Review gates

Before a spec is accepted, verify that terminology is consistent, failure behavior is
defined, sensitive data is handled deliberately, migrations and compatibility are
considered, and acceptance criteria are testable. UI specs also need responsive,
loading, empty, error, keyboard, and accessibility states where applicable.

Implementation can uncover missing constraints. Update the spec through review rather
than allowing code and intended behavior to drift silently.

