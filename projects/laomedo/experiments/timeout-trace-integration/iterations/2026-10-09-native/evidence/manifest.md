---
title: Native reconciliation prospective pins
status: draft
kind: evidence-manifest
owners: [laomedo-maintainers]
last_reviewed: 2026-10-10
applies_to: [laomedo]
supersedes: null
related: []
---

# Native execution pins and access

| Artifact | Pin / access |
| --- | --- |
| Initial protocol and source | Laomedo `add96614a73f19d6dd64c321635d5100a96d5aa9` |
| Reviewed cleanup amendment and both live runs | [bec25c0](https://github.com/amadou-6e/laomedo/commit/bec25c0cfcd3b148acfb3caac9cd7e0c1866182d) |
| Tested develop base | `bd285cf792c5faa20d5effe7e55aa720a2c833b6` |
| Protocol byte hash at run time | `e21fea8c5df0d3f2537eeba579ec38bddc9fdafd303f060cf2658839574b1672` |
| Codex / model / effort | 0.159.2 / gpt-6-luna / low |
| Docker image ID | `sha256:7b79ce12be47d6c8262dd4043895112d204416bda5cd891d124775df55587239` |
| Post-run test relocation | `d43e5ca`; exact rename, no probe or production change |
| Ledger | cap 12, final used 12, one run per case, no retries |

| Published machine artifact | Location | SHA-256 |
| --- | --- | --- |
| before projection | [before.json](before.json) | `315a2d5db5c818e9d32789c8fe1d912258f9c2f50be558060f4bfee6b5e5fb35` |
| during projection | [during.json](during.json) | `1f075032264d69bce566e91f788f4a1043d06d3de29496c905e4e4b902535446` |

The producer is the frozen native probe plus a host-side whitelist projection.
Each JSON includes pins, sanitized summary, teardown, at-timeout and reopened
trace projections, and original-index command/turn boundaries. Model text and
tool outputs are omitted. The protocol and task hashes describe run-time bytes;
Git may normalize line endings, so the source commit is the reproduction pin.

| Private raw native file | Event count | SHA-256 |
| --- | --- | --- |
| Before | 45 | `250174a011b5fae04aa26088980ecacae926a5f0a969f4733073378e0d16c29a` |
| During | 108 | `74186f9bde5714118b7befadf3831d0fd36894c22ed4112a9fbaf8fb671d5ab5` |

Private raw files, profiles, runner API tokens and SQLite stores remain outside
Git in access-controlled local experiment state. No retention period or public
availability is promised. The existing private Codex login volume was reused
without a refresh; this does not prove production credential isolation. There
were no GitHub credentials or grants. No semantic success, global effect
completeness or #93 outage/real-push revocation claim is made.
