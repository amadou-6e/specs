# Cross System rules

This contract governs records crossing repository, Drive, Gmail, and Notion boundaries. Financial meaning and native identity remain owned by their respective contracts.

## Authority

| Concern | Authority |
| --- | --- |
| Financial meaning and lifecycle | [Financial domain](../../objects/financial-domain/rules/README.md) |
| Original documents and Drive metadata | [Google Drive](../../systems/google-drive/rules.md) or original provider |
| Original correspondence | [Gmail](../../systems/gmail/rules.md) |
| Normalized records, reconciliation, exceptions, runs | [Repository](../../systems/repository/rules.md) |
| Native pages, data sources, views and presentation | [Notion](../../systems/notion/rules.md) |

Native metadata wins for native identity; reviewed repository data wins for normalization and reconciliation; the domain contract wins when a representation collapses concepts. Conflicts retain both claims and sources.

## References and relationships

Every reference has system, object type, native ID, and observation time. Repository `source_id` values are namespaced aliases such as `drive:<id>` and `gmail:<id>`. Paths, titles, sender text, amounts, and dates cannot be sole keys. Content sources record hashes when bytes are available; unknown coverage remains unknown; caches remain replaceable.

Links have stable `link_id`, typed endpoints, relation type, status, method, evidence IDs, and decision provenance. Endpoints permit zero-to-many links. Monetary many-to-many links record exact decimal allocations, currency, remainder, tolerance, and status. Amount or proximity alone cannot confirm a match. Rejected and superseded links remain auditable.

## State, time, and publication

Link status is `proposed`, `confirmed`, `rejected`, `superseded`, or `unresolved`. Handoff status is `prepared`, `validated`, `approved`, `published`, `verified`, `failed`, or `superseded`. These do not alter domain lifecycle.

A manifest names schema version, immutable `run_id`, repository revision/tree state, scope, input hashes, coverage, rules/decisions, output hashes, exceptions, and destination. `partial` requires explicit scope and linked gaps.

Publication compares the exact package to a fresh scoped baseline. Approval binds to package hash, destination, action set, and schema. Upserts use stable external IDs and are idempotent. Receipts retain each action, returned native ID, result, and error; verification compares identities, counts, hashes where possible, and monetary controls. Corrections use a new run or explicit correction record.

Ambiguity remains unresolved in the owning exception register. Inaccessible evidence, stale baseline, changed hash, missing approval, or schema mismatch blocks the handoff. Provider-native permissions, versions, comments, thread presentation, formulas, relations, views, charts, and automations are explicitly lossy outside their systems.

See [identity](schema/identity.md) and [mappings](schema/mappings.md).

## Verification

See [checks and historical results](../../../processes/cash-flow/model-validation/cross-system.md).
