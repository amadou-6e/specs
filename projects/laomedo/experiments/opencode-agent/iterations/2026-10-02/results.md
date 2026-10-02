# Results

- Direct CLI returned OPENCODE_CLI_27_REACHABLE, exit zero, no tool events.
- Fresh run fe0f3ede-6057-46a3-9b22-bb298fa16f9d completed through Langflow HTTP200.
  Native session ses_f04a1b37cffewO58dW066lZirh loaded both offered skills through
  completed native skill tools. Three native tool results were recorded. Fixture
  color/count were amber/3, and host readback verified OPENCODE-WORKSPACE-27.
- Worker command attempted both controller credential paths and failed. Independent
  comparison found no controller credential in that run's worker results. This is
  the tested route, not an exhaustive audit of network/proc/tool exploit routes.
- Restart/resume retained the run/session and post-run hash; marker readback and one
  native tool result completed through Langflow HTTP200.
- Cancel run 2459fd29-7bf0-4e29-aed1-03a707ecfe66 received native abort acknowledgement.
  Observed owned worker disappeared and the delayed write did not occur. Its fresh
  workspace did not inherit the earlier marker. Live terminal status was failed,
  exposing a cancellation race. A later synthetic regression verifies the fix that
  sets cancellation before abort unblocks the response and preserves cancelled
  status. Historical live record is not rewritten; final status fix is not live-tested.
- Host suite after fixes: 50 passed. Cumulative ledger 10/10; no remaining turns.

After a further four-turn authorization, live attempt 11 retested cancellation
with the fixed runner. The response was `cancelled`, native abort was
acknowledged, its owned worker exited, and the delayed file was absent. The
fresh run had no marker inherited from the earlier run. This verifies the
status fix in the tested runner API path. Cumulative ledger is now 11/14,
with three authorized turns unused. The historical failed result above remains
unchanged. The saved Langflow flow's Runner URL was subsequently changed to
port 8768 under explicit user approval and verified by readback. Its six nodes
and five edges remained. Successful model-backed flow calls before that edit
used a per-run port 8768 override before the edit.

Saved-flow attempts 12 and 13 used the edited flow with **no node tweaks**.
Both returned HTTP 200, completed, loaded both pinned skills through native
skill calls and supported queryable runner status. Attempt 12's worker command
exited one after the agent appended a period to the fixture filename. Attempt
13's exact worker command exited zero. The worker saw only the two pinned skill
names and read the amber/3 fixture; host readback verified its workspace
marker. Its path-presence command found no controller auth file or personal
skill/session/config directories in the worker. The controller's skill view
contained exactly the pinned skills. Comparison with the selected private
provider key found it absent from the saved/exported flow, tracked files in
both repositories and the inspected run results. The initially too-literal
fixture checker was corrected against the unchanged raw worker event; the
model turn was not repeated. At that point the ledger was 13/14, one turn unused.

Bounded single-user local prototype is supported by these observations. Network
isolation, complete credential-route auditing, hosted/multi-user use and automatic
fresh UI Stop remain unverified. These tested routes support the local #27
prototype; they do not prove the absence of every possible disclosure path.
Production authentication stays with specs #129.
No issue closure or merge is implied.

## Review fixes and final bounded retest

The review of implementation `4b92295` and specs `f6833d8` found that resume
could accept a skill changed by its own previous worker, cancel could be lost
before dispatch, controller setup could leak a broker, and a copied Console token
could expire before a later turn. The implementation now rejects extra or changed
pinned skill directories before resume/dispatch and after a completed turn;
checks a pre-dispatch cancel flag; closes partial controller setup; and validates
the selected key digest and remaining Console expiry before reserving a turn.
It also limits the broker to one concurrent command, releases the runner lock on
corrupt records, handles null skill input, and deduplicates tool parts by call ID.
These fixes have synthetic regressions. Earlier private run records contained no
duplicate call IDs, so duplicate inflation was a plausible code path, not an
observed historical count error. The broker still binds to `0.0.0.0` for Docker
Desktop bridge routing; its random bearer capability is the current access gate.

The earlier persistent second plaintext `auth.json` was verified against the
selected private source and removed. The controller now receives the source file
as a read-only mount. A canary Docker smoke and a no-model check of the real
provider both passed; Docker left only an empty session auth placeholder.
No credential values or raw traces were published.

Saved-flow attempt 14 used the new mount with no node tweaks. It returned HTTP
200, completed, loaded both pinned skills through native tools, executed the
exact worker command with exit zero, and independently verified the marker and
amber/3 fixture. The tested worker private paths were absent, and the selected
provider key was absent from saved/exported flow, tracked repositories and the
inspected run results. The cumulative ledger is **14/14**; no model turns remain.
The host suite passed 63 tests. This retest verifies the normal local path after
the auth mount change, not a live skill-mutation attack or perfectly atomic
pre-dispatch cancellation. Network isolation, all credential access routes,
fresh UI Stop, and hosted/multi-user use remain outside the verified scope.

After the reviewer identified worker access to the unauthenticated host runner
API, implementation PR #31 inherited runner API authentication and configured
disposable command workers with Docker networking disabled. The revised branch
passed 70 credential-free host tests. This did not submit another model turn or
rerun the saved Langflow flow; the 14/14 ledger is unchanged. The earlier worker
network result remains historical evidence, while this later boundary has so far
been checked in code and synthetic tests only.
