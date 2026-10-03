---
title: E05 create-only results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-03
applies_to: [laomedo]
supersedes: null
related: []
---

# Create-only result

The [2026-10-03 review](https://github.com/amadou-6e/specs/pull/195#pullrequestreview-5399309348) approved only steps 1-2. The no-model [Laomedo create-only probe](https://github.com/amadou-6e/laomedo/tree/feat/48/experiments/exp18) on Docker Desktop 27.3.1 observed: exact requested protection accepted by the verifier; a writable `/skills` bind rejected as `mount_mismatch:/skills`; an unavailable seccomp profile failed at `docker create` before a container existed. Dispatch attempts, stage starts and model turns were all zero. The named test containers and network were removed.

This is a **create-only refusal pass**, not a Docker stage protection pass. The [next reviewer pass](https://github.com/amadou-6e/laomedo/pull/58#pullrequestreview-5399354158) found that seven of the original eight real downgrades were rejected, while `systempaths=unconfined` still passed because Docker records it in `MaskedPaths` and `ReadonlyPaths`. The verifier now compares a complete normalized `HostConfig` against a captured correct-create baseline, explicitly requests private cgroup namespace and checks mount propagation. A fixed-request runner-API sidecar is drafted but unstarted. Those changes still need the reviewer's real create-only matrix rerun. No E05 container was started, so checkout writes, grant behavior, protected-file access, host-side symlink processing and network reachability are untested. Agent-originated denial remains untested and requires separate authorization for a nonpersonal credential and capped turns. Unsupported protection continues to block writable first-slice dispatch.
