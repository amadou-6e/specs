# Evidence manifest

Public sanitized artifact: implementation examples/opencode-agent/live-success-evidence.json.
Earlier failed attempts remain in examples/opencode-agent/live-evidence.json.
Reproduction harnesses are direct_cli.py, flow_acceptance.py and cancel_acceptance.py.
The later live cancellation retest is in
examples/opencode-agent/live-cancellation-retest.json. It records attempt 11,
the observed `cancelled` status and independent worker/file checks.

Private artifacts: native controller/worker events, exact API responses, persisted
run/session state and credentials. Never copy those into this repository. Sanitized
evidence contains run/thread identities, snapshot hashes, exact revisions, observed
outcomes and accounting, with no profile paths, organization or credential values.
