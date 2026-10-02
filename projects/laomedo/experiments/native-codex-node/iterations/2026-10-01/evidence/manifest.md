---
title: Installed-node evidence manifest
status: complete
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Evidence manifest

Producer: acceptance.py in the Laomedo native-node example, plus independent
host inspection and in-memory snapshot reconstruction, 2026-10-01.

Public sanitized artifact: examples/native-codex-node/evidence.json in Laomedo
PR #23; pin the final evidence commit in the PR body. It contains source hashes,
run/thread identities, outcomes and the ledger, not transcripts or credentials.
Reproduction harness and exported flow are in the same example directory.

Raw JSONL, runner records, Langflow responses and host logs remain in the private
native-node-21 state outside Git. Access is limited to the local operator; exact
host paths and credentials are not published. Retain them for review; no automatic
deletion or retention guarantee is claimed here. No raw artifact hash inventory
has been exported; reviewers need authorized local access for independent checks.

The summary verifies real Langflow responses contain corresponding run, thread
and snapshot refs. Native item/started without item/completed is not proof of
command completion, denial, or cancellation.

