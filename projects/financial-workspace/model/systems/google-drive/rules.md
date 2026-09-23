# Google Drive rules

This contract defines Drive-native financial evidence identity, observation, retrieval, and failure behavior. It does not redefine the financial facts evidenced by a document.

## Schema

See [schema](schema.md) for fields and identifiers.

## Relationships and cardinality

One bounded workspace observation contains zero or many files and folders. A file may have one or more parents; an inventory retaining one parent must not imply exclusivity. Folder membership is navigation state. One file may support zero or many transactions, purchases, service months, journeys, matters, claims, or tax years, and each domain entity may cite zero or many files. Cross-system links own those relationships. A cached or derived artifact has exactly one recorded source reference, while equal bytes may occur under several Drive IDs.

## Evidence, coverage, and time

Retrieved bytes record SHA-256, size, retrieval time, and result. Coverage records `start`, `end`, and `basis`; unknown coverage stays null. Filename ranges and statement-month filenames are inferred, not provider-confirmed. Cross-year documents retain one Drive identity and explicit coverage. Modified time is distinct from document, coverage, posting, payment, and retrieval dates.

Repository cache bytes are replaceable evidence copies. Derived text records its own hash and `derived_from` reference. Cache replacement is allowed only after downloaded bytes match the pinned SHA-256 and a post-download read shows unchanged ID, modified time, size, and provider hashes.

## State, correction, and rejection

Minimum availability states are `observed`, `retrieved_and_verified`, `inaccessible`, `missing_in_scope`, `ambiguous`, and `changed`. Later metadata or hash changes create new observations and an exception; they do not rewrite history. `missing_in_scope` does not assert deletion.

Acquisition rejects an ID absent or duplicated in the bounded listing, a duplicate current path, a path escaping the cache root, changed bytes, or metadata changed during download. Failed downloads cannot replace verified cache bytes. Folder names, filenames, URLs, byte sizes, dates, and proximity cannot alone prove identity or reconciliation.

Current permissions, revision history, comments, shortcuts, trash state, retention, multiple-parent completeness, and native Google-document export bytes are unsupported until dated observations and contracts exist.

## Verification

See [checks and historical results](../../../integrations/google-drive/model-validation.md).
