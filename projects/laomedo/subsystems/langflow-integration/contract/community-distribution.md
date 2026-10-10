---
title: Community component release and automatic setup
status: draft
kind: target-contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Community component release and automatic setup

Source: [owner interview A02/A05/A09/A15](../../../decisions/0006-release-packages.md).
These are target requirements; no installer, license clearance or maintainer
acceptance is established by this record.

## Release scope

Release the components independently while pursuing upstream inclusion
alongside it. Upstream acceptance does not gate independent distribution.
Support Codex and Windows first; OpenCode, macOS and Linux follow.
The community components do not require the standalone Laomedo application UI.

The scope includes Codex Agent, the existing pinned Skill Reference and the
proposed [Output Contract](../../agent-execution/contract/output-contract.md).
The exact shipping manifest and optional handoff/controller components still
need implementation inventory and compatibility/license review. An existing
OpenCode adapter does not make OpenCode a first-release acceptance gate.

## User setup boundary

The user has Docker available and signs in to Codex. Everything else happens
automatically: providing/configuring the required runner, discovering/loading
the components and wiring their connection. Users must not manually configure
service endpoints, component paths, runtime profiles or daemon launch commands.
Account connection uses the normal selected provider login, not a fresh sign-in
for every run. No additional operator-login ceremony is introduced.

The component is the node visible in Langflow; the runner owns native execution,
sessions, Docker boundaries, cancellation and trace references. The internal
split must not require the user to assemble multiple services.

No developer credentials, private native sessions, personal paths or captured
login URLs ship in the package. GitHub write capability remains scoped and
separate from model authentication; automatic setup is not implicit permission
to use an ambient host GitHub login. Provisioning that capability on a clean
install must be reconciled with the existing account-connection contract.

## Acceptance and open engineering

On a clean supported Windows environment with Docker available, install the
components and runner, connect Codex and import/run the examples without manual
service wiring. Updates/uninstall have documented behavior; saved flow code is
not silently rewritten. Compatibility and license/provenance inventories must
identify their versions and unsupported scope. These are candidate acceptance
gates, not passing test results.

Artifact format, installer privileges, managed service lifetime, Langflow
discovery mechanisms, supported Langflow matrix and maintenance owner are open.
Use [the research and maintainer plan](../design/community-components.md) to
resolve source-backed questions. Contacting maintainers needs separate explicit
authorization; no message has been sent by this specification work.
