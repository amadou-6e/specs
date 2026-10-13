---
title: Recorded Codex agent inspection
status: draft
kind: contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
applies_to: [laomedo]
supersedes: null
related: []
---

# Recorded Codex agent inspection

Scope: read-only local Codex inspection from the Langflow node toolbar. This slice does not execute, retry, cancel or publish. It consumes host-owned records without model turns. The [editable workshop](../design/agent-inspection.drawio) owns geometry, states and interaction IDs.

## Identity and access

`Inspect agent` replaces the Code toolbar action on Codex agent nodes. Other component controls are unchanged. Use the canonical run UUID from this node's current output when available. After reload, offer explicit selection from authenticated runner history; never infer the latest run or claim a manually selected record belongs to this node. Changing selection clears prior evidence immediately. Closed or superseded requests cannot replace the active selection.

The Langflow backend allows only explicitly configured loopback runner connections and reuses its existing backend transport secret. Browser requests contain the runner reference, run UUID and pagination cursor, never a credential. The runner requires bearer authentication. Responses are uncached. Inspection must refuse foreign record identity, traversal, symlinks/reparse points, redirects and oversized replies. No host state directory or login profile is mounted into Langflow for this feature.

## Overview

Show run/thread identifiers, execution status, task outcome, evidence completeness and completion basis independently. Requested and reported model/effort are distinct. Missing usage counters remain unknown; no API charge is inferred from subscription usage. Display the shared campaign turn ledger as campaign usage, not this run's own consumption. Unknown or missing ledger values remain unknown.

## Output validation

Show stored Contract acceptance/rejection, closed validation codes and field paths, precheck installation/call count, output retries/corrections and any closed correction-block reason. Strict final-answer JSON syntax diagnostics contain only reason, line and column, never raw answer excerpts. Execution completion and a successful precheck do not establish final output acceptance. Inspector validation describes the recorded runner precheck; downstream Contract routing remains authoritative.

## Timeline and content boundary

Return only source-line sequence, event kind, item kind/identifier, turn identifier, dynamic tool name, reported command exit code and duration. Do not return messages, reasoning, commands, arguments, environment values, tool output or raw JSON. This is metadata inspection, not full transcript viewing or universal secret detection. Record identifier/name fields remain bounded metadata; users must not store credentials in identifiers.

Read at most 32 MiB of trace per request, 256 KiB per line, and return at most 200 projected events per page. Preserve source sequence across pages. Missing, malformed, limited and paged traces are explicit states, not complete evidence. Record JSON is bounded to 1 MiB; proxy replies to 2 MiB. History returns at most 100 records and never auto-selects one. Refresh is a read only operation. Tabs support keyboard arrows/Home/End, selection labels and accessible loading/error states.

## Validation requirements

- Secret canaries in raw content, arguments and tool output do not reach responses.
- Missing counters, malformed fields and missing traces do not become success or zero.
- Completed execution with invalid final JSON shows rejection diagnostics.
- Authentication, exact connection allowlist, record identity and link boundaries are tested.
- Pagination preserves sequence, and bounded/malformed traces expose limits.
- Browser checks cover current-output identity, manual history, tabs, selection changes and refresh without Run requests.
- Existing Skill files and Issue viewer controls remain usable.

## Limits

Completed-run metadata only. Live streaming, raw content access/redaction, cost estimates, cross-provider inspection and durable Langflow invocation joins remain outside this slice. Current campaign permissions, budgets and credentials remain unchanged.
