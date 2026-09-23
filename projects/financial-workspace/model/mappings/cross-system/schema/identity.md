# Identity and deduplication

This page defines cross-system keys without redefining native identity.

| Object | Cross-system key | Retained native identity |
| --- | --- | --- |
| Domain entity | Typed domain ID | All provider IDs used to derive it |
| Drive evidence | `source_id=drive:<drive_file_id>` | Drive file ID |
| Gmail evidence | `source_id=gmail:<gmail_message_id>` | Message, thread when known, and attachment IDs |
| Notion projection | Canonical external upsert ID | Page, database, and data-source IDs |
| Repository run | Process-scoped `run_id` | Revision, manifest path and hash |
| Link | Schema-scoped `link_id` | Both typed endpoints |

Provider IDs are opaque and never compared without namespaces. Deduplication uses exact native/canonical ID, then confirmed alias, then a versioned provider composite, then a proposed match requiring review. Hash equality proves byte equality, not logical identity; hash change creates an exception.

Incompatible reuse of an ID is blocking. Missing native ID, namespace, or unique upsert ID blocks affected publication. Absence from a baseline or scoped discovery proves only non-observation in that scope.
