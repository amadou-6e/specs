---
title: Writable stage protection protocol
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Writable stage protection

[EXP-18](https://github.com/amadou-6e/laomedo/issues/48) requires a reviewed E05 safety protocol before a pinned writable-stage test. The [2026-10-03 review](https://github.com/amadou-6e/specs/pull/195#pullrequestreview-5399309348) approved only create-only steps 1-2, which [passed](iterations/protocol-review/results.md). The [amended protocol](protocol.md) awaits re-review before stage startup in steps 3-6. The experiment depends on the [EXP-07 orphan bound](../orphan-lease/README.md). No degraded Docker stage or model call is authorized by this draft.
