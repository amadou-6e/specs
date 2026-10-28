---
title: Python package layout and migration
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-28
applies_to: [laomedo]
---

# Python package layout and migration

The owner selected a standard src layout, named the execution package agents,
and clarified that callers should migrate rather than retain the flat import
surface. Canonical Python code lives under src/laomedo. Components, frontend,
tests, docs, examples and packaging metadata stay at the repository root.

| Package | Ownership |
| --- | --- |
| agents | Run lifecycle, contracts, artifacts and provider adapters |
| skills | Registry, discovery, editing operations and materialisation |
| github | Issue/PR contracts, clients, gateways and transports |
| host | Trusted credentials, mediation, leases, publication and startup |
| activity | Capture, storage, projection, tracing and inspection routes |
| integrations/langflow | App composition, joins and stage adapters |
| work_graph | Existing work-graph domain |

Each implementation has one canonical owning module. Cohesive features are
subpackages: activity/agent_activity contains store, capture, cost, projection
and routes. The Python package root contains only its initializer and shared
package-path infrastructure. Runtime forwarding modules, import hooks and the
checkout-only bridge are removed; development uses an editable src install.

No credential or host authority moves into a model-callable boundary. Public
HTTP records, error codes, request identities, acknowledgement order,
cancellation and cleanup semantics remain unchanged. Configuration bytes,
script bytes, policy hashes and image pins remain stable; neither persistent
record-schema migration nor changes to external wire formats are included.

## Feature cohesion and typed data

Package boundaries follow responsibilities, not a fixed nesting depth. Repeated
filename prefixes trigger a cohesion review: activity/opencode owns projection,
events and telemetry; skills/operations owns client, server, service and models.
Do not retain obsolete modules as forwarding shims after migrating consumers.

An implementation file introduces classes or standalone functions, not both.
Functions that belong to an object's responsibility become methods. Independent
helpers live in the owning feature's utils.py or a focused function-only module.
Exception classes belong in errors.py; initializers remain small. Hiding a class
inside a standalone factory does not satisfy this separation.

Values repeatedly passed together as one domain concept use a canonical Pydantic
model in that feature's models.py. Constructors, validation and projections belong
on that model when cohesive. Preserve strict input validation, immutability,
ordering, deterministic snapshot hashes and explicit external projections; do not
silently coerce values or duplicate a domain model at each transport boundary.
Secrets must be excluded from representations and validation diagnostics. Extract
secret values only at an existing authorised private boundary.

Initial typed concepts include work-graph items, dependencies and snapshots;
verified stages; skill edits, proposals and editor provenance; container cleanup
identity; activity capture identity and invocation; and prepared runner requests.
Pydantic is a direct constrained dependency, checked in host, installed-package and
pinned staging runtimes. No credential or execution authority is added by a model.

Structural checks prevent mixed object/function modules, obsolete imports,
conflicting module aliases and module/package name collisions. Behavioural checks
cover canonical payloads, snapshot hashes, ordering, validation and redaction.
These checks establish internal invariants, not real integration acceptance.

## Consumers and one-time migration

Repository imports, current component definitions, launcher commands and
current graph exports use canonical domain names directly. Flat imports and
old python -m module names are intentionally retired after caller migration.
The app factory uses integrations.langflow.viewer:create_app.
Launchers use agents.runtime.cli, agents.providers.claude.cli,
host.leases.service_cli and host.managed_service under the laomedo namespace.

Saved graphs embed Python code; source migration is explicit. The repository
provides tools/migrations/migrate_module_paths.py and reviewed module, symbol
and CLI maps. Every published module generation maps directly to its final owner;
renamed or extracted symbols migrate to their defining modules. Unsafe dynamic
references and changed constructor or method signatures require manual migration.
The tool must not claim such inputs are already current.
The default is a preview on explicitly selected files. Applying retains a
non-overwritten sibling backup, preserves graph/run identities and unrelated
payloads, and updates only embedded code and known launcher fields. Repeating
migration is idempotent. This tool is not shipped as runtime compatibility.

File migration preserves unrelated bytes, Unicode, number spelling, duplicate
JSON keys, BOM and line endings by splicing only changed string values. It
selects template code and explicit root launcher fields, not arbitrary nested
payload keys. Unparseable retired imports report manual migration, not current
status. Backup conflicts are checked before writing; writes are atomic per
file. Unexpected I/O failure can leave a batch partly applied with originals
retained. Registered scheduled tasks retain their old command independently
of files: re-run the updated user-task installer with existing configuration
before enabling an old task. The file migration tool does not update tasks.

Existing locally controlled graph definitions and launchers are migrated before
their next use with the new package. Report external launchers that cannot be
migrated; do not silently keep aliases or claim their verification. Historical
execution exports, receipts and observation evidence remain unchanged. Migrate
a copy when historical input is needed for a new graph.

## Runtime assets

Assets belong to their runtime domain: runner config, seccomp and agent-side
MJS adapters live in agents/resources; bundled skill instructions live in
skills/resources; the pinned staging script lives in host/publication/resources.
The standalone stdlib Git credential helper lives in host/credentials and
remains executable as a script. Docker build definitions belong in containers,
and package documentation belongs in docs rather than the runtime root.

Resource paths derive from their owners, independent of checkout location.
Shared import/package roots identify the installed canonical package. Stage
containers mount that package tree read-only. Explicit source roots may be a
checkout root, src root or installed import root, without arbitrary parent
search. Private credentials and service state stay outside source and outside
model-callable mounts.

## Verification boundary

Check installed-wheel discovery, canonical imports, resource ownership and
pinned bytes from an unrelated working directory. Exercise canonical CLI
entrypoints and reject reintroduction of flat forwarding files. Check migration
against archived graph inputs, idempotence, identity/content preservation and
backup behavior. Catalogue guards inspect defining error producers directly.

Run core and explicit Langflow regression suites. Mocked controls and historical
receipts do not establish real Agent execution. Runtime migration acceptance
also requires real managed startup, recorded-run Status and an authorised Fresh
execution on the installed final package. Reconcile unknown outcomes before
retrying. Independent Claude review and owner working-graph approval remain
required before merge; a package refactor does not prove unexercised provider
scenarios or redesign execution lifecycle behavior.
