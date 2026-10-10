---
title: Runner Git regression execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Retrospective regression execution

Source base: develop `44f628e775bad90d9cd25c6a0a0e50a0072c6de7`. Work was isolated
in branch `feat/79`; the other session's `feat/104`/#105 was not edited. The visible
spec checkout uses `docs/79`, with changes confined to skill-registry ownership.

Initial tests exposed that LocalRunner forbids repository-root source metadata:
it copies a subdirectory into an outside-Git private workspace. Therefore the
implementation creates a new credential-free baseline and then installs exact
skill exclusions. Initial use of skill inventory on Git metadata was corrected;
that inventory requires SKILL.md and cannot validate arbitrary Git directories.
Git metadata is checked by entry type instead, without reading object bodies.

On Windows, Git loose objects are read-only. This first broke cleanup and an
OpenCode resume regression. Owned-tree cleanup now handles that attribute within
the state boundary, and private initial objects are writable. The full host suite
then passed 302 tests, six skipped. A further linked-Git-root negative control was
added before the final committed-source rerun. Final counts are in results.md.

Fresh fixture repositories have no pre-existing exclude file. Each has a tracked
CRLF source and an immutable CRLF skill revision. The production runner prepares
two independent workspaces; real Git status and staging verify the exact exclusion
and visible unrelated changes. Fake native transports test pre-dispatch refusal,
post-turn tampering and snapshot refusal without invoking a provider. Cleanup
failure is injected; no clean teardown is falsely claimed. Personal/global Git
configuration and credentials are not used. Tests were authored by the same agent
as the implementation, with independent review still required.
