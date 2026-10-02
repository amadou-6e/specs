---
title: Work Graph design
status: draft
kind: design
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Work Graph design

The read-only slice imports paginated GitHub issues and native blocker edges,
saves immutable digested snapshots, and computes filtered projections from the
complete snapshot. The implementation is in [Laomedo PR #17](https://github.com/amadou-6e/laomedo/pull/17).

A future view needs a reviewed design in this subsystem before UI work. Runner
launch and rerun require separate authorization and must preserve the frozen
work and graph snapshot references in the [contract](../contract/work-graph.md).
