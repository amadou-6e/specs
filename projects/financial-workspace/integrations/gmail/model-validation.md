# Gmail model validation

This record maps guarantees to checks actually run. No external system was queried or mutated.

| Check | Result | What it proves |
| --- | --- | --- |
| `git branch --show-current`, `git rev-parse HEAD`, `git status --short` | `main`, `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`, extensively changed | Evidence context; not a clean release |
| PowerShell JSON parse of 2026-09-15 Gmail inventory | 5 records; complete discovery false | Candidate readability and non-completeness |
| PowerShell JSON parse of evidence manifest | 5 candidates; 6 attachments | Representative cardinality |
| Null-hash filter | 6 of 6 attachment hashes null | Identity retained; bytes unverified |
| Review of procurement and recurring discovery docs | Requirements align | Candidate versus complete-period contract |
| Existing run task result/package audit | Partial by design | Candidates point to evidence; no complete-month claim |
| From `specs/`: `python tools/validate_specs.py` | Passed: 5 projects, 1,420 files, 0 errors, 1 unrelated large-file warning | Structure, frontmatter, links |

## Future checks and gaps

A Gmail schema must reject absent mailbox scope, malformed namespaces, duplicate message keys, orphan attachments, conflicting IDs, guessed values, and completeness without terminal pagination. Fixtures must cover threads, repeated bytes, multi-item messages, missing bodies, attachment failures, rule changes, and ambiguous item order.

Complete-period replay must preserve query/account, traverse every page, record terminal state and IDs, and reconcile discovery one-for-one with inventory. Content verification must compare MIME/attachment bytes to hashes. Candidate replay proves only declared IDs.

No complete-period artifact exists for the example month. Legacy evidence lacks mailbox scope, thread IDs, MIME/body hashes, part paths, and all six attachment hashes. Acquisition, schema validation, pagination replay, and deletion/change detection are unimplemented. Item-ordinal stability lacks a regression fixture. Retention, permissions, legal hold, label history, and deletion semantics were not observed.
