---
title: Python package layout and migration
status: draft
kind: interface-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-27
applies_to: [laomedo]
---

# Python package layout and migration

The owner selected a standard src layout and named the execution package agents.
Canonical Python code lives under src/laomedo. Components, frontend, tests, docs,
examples and packaging metadata remain at the implementation repository root.

| Package | Ownership |
| --- | --- |
| agents | Run lifecycle, contracts, artifacts and provider adapters |
| skills | Registry, discovery, editing operations and materialisation |
| github | Issue/PR contracts, clients, gateways and transports |
| host | Trusted credentials, mediation, leases, publication and startup |
| activity | Capture, storage, projection, tracing and inspection routes |
| integrations/langflow | App composition, joins and stage adapters |
| work_graph | Existing work-graph domain, retained |

No credential or host authority moves into a model-callable boundary because of
this layout change. Public HTTP records, error codes, request identities,
acknowledgement order, cancellation and cleanup semantics remain unchanged.
Configuration bytes and image pins remain stable; no persistent data migration
or wholesale model-library dependency change is part of this refactor.

## Retained interfaces

Saved graphs embed Python code and import flat module names. Keep the existing
names as compatibility modules resolving to the identical canonical module object,
including private symbols, exception/class identity and mutable globals. The
implementation mapping is tools/package-layout.json. New component definitions
use canonical imports. Historical execution exports remain unchanged; current
example exports may be regenerated. Known-source legacy contract migrations keep
their exact recognised source text.

Existing python -m commands, scheduler tasks and app factory names remain valid.
Executable compatibility modules must branch before importing the defining
module and invoke its real main; a successful no-op is an acceptance failure.
The checkout-only root laomedo/__init__.py bridge supports working-directory
imports and old editable mappings. It points only to src/laomedo, never searches
other checkouts, and is excluded from wheels. The canonical package initializer
has no executable setup; that invariant needs a regression check before changes.

Resource and import roots are derived from a canonical package helper, independent
of domain nesting and the checkout bridge's __file__. Resources remain at the
same package-relative paths. Source origin reports identify the canonical package.
Stage containers mount the importable package tree, including all canonical
subpackages and retained facades. Explicit source roots accept the existing checkout root, src import roots and
installed import roots without searching arbitrary parent directories.
The host credential helper remains an executable package-root script.

## Verification boundary

Check installed-wheel imports and resources from an unrelated working directory,
retained entrypoints from the checkout, unchanged pre-refactor embedded component
code, module/global identity and actual interception by existing patch targets.
Catalogue guards inspect defining producers rather than compatibility wrappers.
Run core and explicit Langflow regression suites; internal mocked controls do not
establish real graph or agent acceptance. Runner-affecting migration also needs
real managed startup, recorded-run Status and an authorised Fresh execution,
with unknown outcomes reconciled before any retry.

The original dirty checkout is preserved. Work occurs on an isolated branch from
current develop; unrelated pending changes are not silently included. Independent
Claude review and the owner's working-graph review remain required before merge.
A package move does not imply lifecycle algorithms have been redesigned or prove
provider scenarios that were not actually exercised.
