---
title: Langflow graph freeze results
status: draft
kind: experiment-results
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Results

The first run entered the pause before the saved-flow patch, then returned TASK|BEFORE. A new run returned TASK|EDITED-AFTER. Stored graph SHA-256 changed from cfd353b84e5c83ee1d1950d7957220eaea277673e66fd1a3183e56e1c273face to e753a310eebe0c5cd3c4f565c26d21fb89b645d647000b49dbb5041532696709. The marker component source changed from 0b4888d552f5bc07ec2b91cd8a85a352d90e717dae20c6e69e450ff04de7843e to 9accc1b961112303ed53206274d3c2fe8653e0129ef0e8accac88947cf6d5c53.

Observed: the mid-run saved-flow edit did not affect the waiting downstream marker in this pinned, cold-build path. Not established: a native run-bound component-code hash. The run response gives a run ID but not that hash. A Laomedo launch record must bind graph/component hashes before dispatch, and the adapter must refuse launch if it cannot resolve them. EXP-04 owns that follow-up. This is a partial freeze result, not acceptance of native attestation.
