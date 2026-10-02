---
title: Installed-node attempt execution
status: complete
kind: experiment-execution
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Execution and deviations

Started a separate approved localhost:7862 Langflow server with the read-only
component directory and local auto-login. Existing localhost:7861 was unchanged.
Started the existing runner implementation on localhost:8766 with a new private
state directory and four-turn ledger, reusing its skill store and auth volume.
The historical pilot ledger was not reset.

Before model calls: installed catalog and import/export/reimport passed.
Mutable skill and incomplete resume inputs failed in Langflow with no dispatch.
After calls: a genuinely missing snapshot and exhausted cap failed without a turn.

1. Fresh run 496719d1-2be6-4353-9ef3-643bdd74562f: native tool results,
   marker write/read, Langflow HTTP 200, one dispatch across both branches.
2. Verified runner restart (PID changed), then node resume of the same run/thread:
   marker read, Langflow HTTP 200, exact prior snapshot accepted.
3. Fresh run 16f0e599-1705-4476-96a5-ed3abf50ac80: independent host workspace,
   but the agent looked for fixture.txt beside the skill and failed its task.
4. Cancellation attempt c90ba2b9-d9c6-4b4f-82f5-46ac805979ca: native sleep command
   started, agent ended the turn before the harness saw expected output events;
   no confirmed cancellation or command-completion event.

Verifier corrections spent no extra turns: explicit UTF-8; input snapshot binding
rather than unchanged output snapshot; host isolation separated from model wording.
The new post-resume hash differs only by an empty .aws directory, verified by
in-memory reconstruction of the prior hash. Its creator was not separately traced.
The corrected cancellation verifier now triggers on command-start, but has not
been retested with a model. Budget remains 4/4.

