# Results

Real chain succeeded at exactly 2/2 additional submitted turns. Prior ledger remains
7/8. Source run `7883d774-2dfd-44a7-881e-abc157add1fa` fed target
`1f8f9571-b55b-416b-8944-a661d581dfc6`; distinct native threads were observed.
Target answer was exactly `LAOMEDO_CHAIN_28_COMPLETE`. Its persistent handoff points
to the source and declares independent workspace policy; both post-run hashes and
the pinned skill revision are in the sanitized evidence file.

At delivered implementation ac204ab: 54 host tests pass; pinned runtime tests pass
11 existing Codex component checks, two handoff graph checks and two native-controller
checks (six independent loop stop/error subcases plus cancellation evidence). Artifact
tests cover selected bytes, hash mismatch, traversal/profile/credential paths,
hard links, destination conflicts, shared-workspace rejection and restart provenance.

Follow-up implementation `9a46a50` rejects changed skill sets during explicit resume
and adds a same-provider resume test binding thread/snapshot/model/effort/skills.
55 host tests pass at this revision; it submits no new live turns. The pinned
runtime checks above were run at ac204ab, before this resume-only follow-up.

Real loop, cross-provider chain and cross-provider file transfer remain unobserved.
Fresh immediate remote cancellation remains limited by missing early run ID (#22);
outstanding native command finalization remains #24. The new controller deployment
configuration is a draft and has not replaced the user's current service.

## Takeover verification on 2026-10-02

At implementation `9a46a50`, the primary agent independently reran all 55 host
tests and all 15 pinned Langflow checks (11 Codex, two handoff, two bounded
controller); all passed. A reproducible real-loop acceptance harness was prepared,
but no additional model call was submitted. Inspection of private provider ledgers
confirmed that #27 also used two turns, making the aggregate authorization 4/4.
The previously reported two remaining turns were incorrect. Further live-loop
acceptance requires a new two-turn allocation. Applying the separate localhost:7863
deployment draft also awaits explicit configuration approval.

## Real loop acceptance on 2026-10-02

The user subsequently authorized two further turns. Harness `live_loop.py` executed
the actual native bounded-controller graph in pinned Langflow 1.12.3, with no mocked
runner calls. Execution `a6ac76c7-d09b-4ad5-8442-4cd8f126e9d1` stopped on success
after exactly two completed iterations and answer `LAOMEDO_LOOP_28_COMPLETE`.
Runs `2ddea53d-602e-4f18-a3b8-7a7a785e0a9a` and
`698d8dbc-8296-40aa-a733-1004b56fdb8e` had distinct native threads. The second task
was the first answer. Private execution records retain both transitions; sanitized
run IDs and snapshot hashes are in the implementation's `live-loop-evidence.json`.
The handoff runner ledger advanced cumulatively from 2/2 to 4/4; no ledger reset or
authentication copy occurred. Together with the two OpenCode attempts, the new
cross-ticket aggregate is 6/6 submitted turns. Original pilot ledger is unchanged.

Real-loop acceptance is now observed. Separate browser-installed deployment still
awaits configuration approval; cross-provider acceptance remains dependent on #27.
No issue closure, merge, early remote cancellation or exactly-once guarantee is claimed.
