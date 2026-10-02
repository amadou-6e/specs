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

Bounded single-user local prototype is supported by these observations. Network
isolation, complete credential-route auditing, hosted/multi-user use and automatic
fresh UI Stop remain unverified. Production authentication stays with specs #129.
No issue closure or merge is implied.
