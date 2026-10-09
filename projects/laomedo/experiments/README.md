# Experiments

Folder collection: README.md (1), template/ (1), named trials (0..*). Each trial has
README.md, protocol.md, sources.md and iterations/README.md (1 each), ordered attempts
(0..* before execution, at least 1 for a completed result). Each attempt has overview,
execution.md, results.md and evidence/manifest.md (1 each); replication.md (0..1) only
when actual replication occurs.

- [Local skill-agent pilot](local-skill-agent-pilot/README.md): actual 2026-10-01 four-turn sequence.
- [OpenCode agent](opencode-agent/README.md): 2026-10-02 direct CLI, isolated skills,
  fresh/resume and explicit native-cancellation observations, retaining prior failures.
- [Native Codex node](native-codex-node/README.md): installed-flow fresh/resume evidence
  and retained negative results; an authorized retry verified explicit cancellation.
- [Early-run cancellation](early-run-cancellation/README.md): later pinned Langflow graph
  cancellation of a real Codex turn, with the visible Playground and trace-join limits retained.
- [Copyable example](template/README.md): unexecuted snapshot-rejection trial.
- [Agent handoffs](agent-handoffs/README.md): successful two-turn real chain and
  credential-free bounded-loop/artifact/provenance checks; live loop unobserved.
- [Langflow graph freeze](langflow-graph-freeze/README.md): EXP-03 synthetic
  saved-flow edit during an active run; behavior stayed old, native revision
  attestation remains absent.
- [Durable pre-dispatch](durable-pre-dispatch/README.md): EXP-04 synthetic
  crash-window evidence for run identity, frozen refs and no-replay sweep.
- [Pinned skill materialization](pinned-skill-materialization/README.md):
  EXP-08 LF/CRLF exact-byte, protected/unprotected Git-clone and tamper-refusal probe.
- [Agent evidence crash](agent-evidence-crash/README.md): EXP-05 synthetic
  invocation/native-ID/raw-event persistence across process-kill windows.
- [Agent-event replay](agent-event-replay/README.md): EXP-09 synthetic
  at-least-once receipt preservation and explicit action-identity uncertainty.
- [Long-call timeout](long-call-timeout/README.md): EXP-10 pinned Langflow
  outer-client, component HTTP and v2 server timeouts with late synthetic effects.
- [Post-timeout job status](post-timeout-job-status/README.md): follow-up
  read-only v2 job polls returned terminal `JOB_FAILED` before a late synthetic
  effect; it did not test a Laomedo trace.
- [Timeout trace integration](timeout-trace-integration/README.md): EXP-66
  synthetic live Langflow call preserved timeout, `JOB_FAILED` deliveries and
  late effect as a durable partial Laomedo trace; real-agent cancellation remains untested.
- [UI versus backend death](ui-versus-backend-death/README.md): EXP-06
  pinned Langflow client-close and hard-kill observations with a startup sweep.
- [Orphan lease](orphan-lease/README.md): EXP-07 protocol for the selected
  independent supervisor plus startup sweep; numeric bound and run pending.
- [Issue to agent to PR integration](issue-agent-pr-integration/README.md):
  EXP-19 credential-free phase-zero protocol; no model or GitHub write.
- [Work Graph source integrity](work-graph-source-integrity/README.md):
  EXP-01 installed-package fixture verification, including the hidden-open-blocker
  filtered-readiness amendment; no live GitHub access was tested.
- [Work Graph dispatch binding](work-graph-dispatch-binding/README.md):
  EXP-16 credential-free installed-wheel mock-runner snapshot, freshness,
  blocker, grant and run/trace binding result; real adapter remains unverified.

Copy template/ directly, rename and replace every example fact/lifecycle. Freeze a real
prospective protocol before dispatch. This migration authorized/spent no new model turns.
