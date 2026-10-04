---
title: E05 direct no-model execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-04
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution

The [verifier review](https://github.com/amadou-6e/laomedo/pull/58#pullrequestreview-5406644179) rejected all 30 real Docker protection downgrades and approved direct, no-model steps 3-4. The [Laomedo harness](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/probe_stage.py) built a sidecar and synthetic grant canary from local `python@sha256:bb8009c87ab69e751a1dd2c6c7f8abaae3d9fce8e072802d4a23c95594d16d84` with build networking disabled. It verified their built image IDs and Docker Desktop 27.3.1 before creating a stage. The stage used the pinned `laomedo-codex-boundary:0.159.2` image.

Before stage start, the harness created and inspected the sidecar. Its two networks were the dedicated E05 internal network and Docker `bridge`; it had no mounts or published ports, a read-only root, all capabilities dropped, `no-new-privileges`, non-root user `10001:10001`, the pinned image and fixed Python entrypoint. A temporary local runner on port 8767 had model turns disabled. The sidecar's fixed request returned a real 401 from that runner before stage start. The stage's full normalized HostConfig, image ID, entrypoint, command, working directory and environment-variable names matched the reviewed request.

The stage wrote and read back a disposable checkout file, read the mounted effective skill, then attempted the forbidden skill write and reads/writes of four unmounted canaries. It created a checkout symlink to an unmounted host path. The synthetic HTTP grant accepted one scoped write and rejected a request without the grant. The runner sidecar returned 401. Direct probes of host-loopback ports 8767 and 8768 and Docker Engine TCP port 2375 returned DNS failure from the internal stage network. A bounded file sweep excluded `/proc`, `/sys` and `/dev`, scanned 6,009 accessible regular files and 679,212,708 bytes, and found no protected canary filename or marker byte. The stage stopped; grant revocation succeeded, and a later write with the formerly valid grant returned 403. Host-side checkout hashing rejected the stage-created symlink as `unsafe_workspace_entry`; protected canary hashes remained unchanged. All named containers and the network were removed.

Two earlier attempts were inconclusive because the sweep skipped files above its initial 64 MiB threshold, then reached a 512 MiB total cap. Both cleaned up, used no model and found no protected marker in the portions searched. The final streaming sweep covered the large files within a 4 GiB and 20-second bound and reported `incomplete=false`. The [sanitized final observation](https://github.com/amadou-6e/laomedo/blob/f897f41/experiments/exp18/stage-observation.json) records prestart sidecar inspect, stage checks, canary events, before/after hashes, lease deadline, route results and cleanup. It contains no grant value or personal credential.
