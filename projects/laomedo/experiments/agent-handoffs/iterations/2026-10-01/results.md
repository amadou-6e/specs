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
