---
title: Develop-based integration execution
status: draft
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-09
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution record

The user selected finishing Laomedo #117 and merging after Claude review. Its
former #105 parent remained an independently maintained, unapproved draft.
The implementation slice was extracted onto develop `80bcacf`, preserving the
old child `fd3118d` under remote `archive/117-integrated-fd3118d`. No mediation,
lease or protected-approval implementation was copied into this slice.

The prospective protocol was committed at Laomedo `8923e1f`. Claude requested
host receipt/status guards and ordered ledger checks; these were committed
at `aa850f2` and cleared in the same reviewer session before execution. A test
insertion-count correction and trailing whitespace cleanup followed without
production or probe logic changes. Both live cases pin tested source
`7b5d009b6a3fe8ffc84c167e901f64587bfe1a91`.

The no-model Playground preflight passed. A separate read-only check of the
existing private login copy returned HTTP 200 with usage allowed; it requested
no token refresh and submitted no model. Disposable Langflow 1.12.3 used a
private SQLite mount and only the bridge token. The loopback host bridge alone
held the runner API token. Native Codex 0.159.2 used the already approved
non-split login profile and unchanged Docker permissions. No GitHub credential
or write grant was present. Model and effort were gpt-6-luna and low.

One fresh pre-thread case held the async acknowledgement until confirmed Stop,
then reopened the host binding in a new child and Langflow's database after
restart. Entry nine was conservative; no native model call occurred. The one
fresh active case used entry ten, observed the long command, clicked visible
Stop, checked the delayed sentinel and repeated restart correlation. Neither
case was retried. Native starts stayed one per case with zero after restart.

The active result remained `real_join_inconclusive` because the read marker
shared output with the known public fixture sentence. A retrospective equality
check of the completed event supplies the amendment in results; it did not
modify the original summary or ledger and spent no additional model turn.
