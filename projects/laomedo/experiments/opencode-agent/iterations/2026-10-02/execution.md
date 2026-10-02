# Execution

The user authorized four further submitted turns after ledger 6/6. Cumulative cap
became 10 without deleting failed attempts. Attempt 7 used the direct terminal CLI
with tools denied and returned the exact marker. It creates a personal CLI session,
so it is explicitly a login diagnostic rather than isolated-run evidence.

Attempt 8 executed the imported Langflow flow with the separate controller/worker
transport. Attempt 9 resumed it after the runner was stopped and restarted, also
through the same imported flow. Attempt 10 used the runner API directly to execute
one delayed command and cancel it once its owned worker was observed. There were
no additional model submissions. Earlier source revisions are retained in the PR.

The user then authorized four more turns, extending the cumulative cap from 10
to 14 without resetting earlier attempts. The runner was restarted with the
already committed cancellation-race fix and the new cap. Attempt 11 repeated
the delayed-command cancellation through the runner API. Native abort was
acknowledged, the request returned `cancelled`, the owned worker was absent,
and neither the delayed file nor a marker from another run appeared. Ledger
after the test: 11/14; three authorized turns remain unused.

The existing saved Langflow flow initially pointed to port 8767 while this
OpenCode runner listens on 8768. An attempted address update was rejected by
automatic approval review under the configuration-change rule. After the user
explicitly approved this exact edit, the saved Runner URL was updated to
`http://host.docker.internal:8768`. Readback returned HTTP 200, the new URL,
six nodes and five edges. Earlier successful flow calls used an explicit
per-run port 8768 override. No model turn was spent on the configuration edit
or readback.

The user selected proof of the remaining #27 acceptance gaps using the three
unused turns. Attempt 12 called the saved six-node Langflow flow with no node
tweaks. It returned HTTP 200, completed, loaded both pinned skills natively,
listed only those skills from the worker, and reached the private-path presence
checks. The worker exited one because the agent appended a period to the
fixture filename. The failed tool result remains in the private record and
the submitted turn remains counted.

Attempt 13 repeated the saved flow without tweaks after the probe prompt was
corrected. The exact worker command exited zero. The runner status was
queryable and `completed`; both native skill calls completed, only the two
pinned skills were visible in the controller view and worker listing, the
private-path presence checks passed, and independent host readback found the
workspace marker. The worker returned fixture amber/3. A first checker used a
too-literal `color: amber` predicate and reported that field false; a read-only
verification of the unchanged worker event recognized the actual sentence
`The sample color is amber. The sample count is 3.` All other original checks
were true. Ledger after attempt 13: 13/14, with one authorized turn unused.

The remaining authorized turn was used after review fixes. First, a canary-only
Docker smoke verified the read-only controller auth mount and empty session auth
placeholder. A separate no-model check verified the real private provider and
selected model through the new mount. Neither submitted a model turn. Attempt 14
then ran the unchanged saved six-node Langflow flow with no node tweaks. It
completed with both pinned native skill loads, the exact worker command, fixture
read and independent marker verification. The worker private-path checks passed.
The cumulative ledger is 14/14; no further model turn is authorized.
