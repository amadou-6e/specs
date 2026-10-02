# Evidence manifest

Public sanitized artifact: implementation examples/opencode-agent/live-success-evidence.json.
Earlier failed attempts remain in examples/opencode-agent/live-evidence.json.
Reproduction harnesses are direct_cli.py, flow_acceptance.py and cancel_acceptance.py.
The later live cancellation retest is in
examples/opencode-agent/live-cancellation-retest.json. It records attempt 11,
the observed `cancelled` status and independent worker/file checks.
Saved-flow proof and its retained first-attempt limitation are in
examples/opencode-agent/saved-flow-proof-evidence.json. The reproducible
no-tweaks harness is saved_flow_proof.py; its read-only verification phase
corrects a literal fixture-label predicate without rewriting the live event.
The review-fix record is in `review-fixes-evidence.json`. Its canary Docker smoke,
no-model provider preflight and saved-flow attempt 14 are reproducible with
`smoke_auth_mount.py`, `preflight_auth_mount.py`, and `saved_flow_proof.py` under
the existing private state and ledger rules. The final ledger is 14/14.

Private artifacts: native controller/worker events, exact API responses, persisted
run/session state and credentials. Never copy those into this repository. Sanitized
evidence contains run/thread identities, snapshot hashes, exact revisions, observed
outcomes and accounting, with no profile paths, organization or credential values.
