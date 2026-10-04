---
title: E05 direct no-model results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Direct no-model result

**Direct process-boundary pass; agent-originated criterion untested.** The inspected sidecar met its launch condition before the stage started and reached the temporary runner on port 8767 only through its fixed request. The pinned stage passed its HostConfig and Config checks. A direct command wrote the disposable checkout and scoped grant canary, read the mounted effective skill, and received `EROFS` on a skill write. The four unmounted protected paths returned `ENOENT` for direct reads and writes; the complete bounded marker sweep found no alternate file path to their marker bytes or unique names. The stage could not resolve the probed host-loopback routes, and the grant rejected an unscoped request and a post-revocation request. The host snapshot hash rejected the stage-created symlink. Protected hashes stayed unchanged and cleanup completed.

The [final observation](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/stage-observation.json) records zero model turns. A deterministic Node process inside the container performed the commands; no Codex or other agent issued them. The result covers the tested local image, Docker Desktop 27.3.1, runner port and routes, and synthetic canaries. It does not establish isolation from all possible network paths or a production-stage integration. Step 5 remains untested until the user separately authorizes a nonpersonal credential and capped model-turn budget. Do not mark E05 complete on this result.
