---
title: Writable stage protection protocol
status: draft
kind: experiment
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Writable stage protection

[EXP-18](https://github.com/amadou-6e/laomedo/issues/48) requires a reviewed E05 safety protocol before a pinned writable-stage test. The [2026-10-03 review](https://github.com/amadou-6e/specs/pull/195#pullrequestreview-5399309348) approved the [create-only steps 1-2](iterations/protocol-review/results.md). The [2026-10-04 review](https://github.com/amadou-6e/specs/pull/195#pullrequestreview-5406644232) approved direct no-model steps 3-4 with a sidecar-container preflight condition; the [direct result](iterations/direct-no-model/results.md) passed that bounded process check. The experiment depends on the [EXP-07 orphan bound](../orphan-lease/README.md). Step 5 has a [four-turn ceiling and a proposed exception for the user's subscription login](iterations/agent-originated/README.md), but its credential boundary and model route are not reviewed. E05 is not complete.
