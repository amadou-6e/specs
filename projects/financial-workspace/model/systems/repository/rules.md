# Repository rules

This contract defines observable repository identity, provenance, lifecycle, and rejection behavior without redefining financial concepts owned by the financial object models.

## Schema

See [schema](schema.md) for fields and identifiers.

## Invariants

1. Reproducibility claims identify the commit and contributing working-tree changes.
2. External originals retain provider IDs; local cache copies are disposable.
3. Original-source bytes used by a run match pinned hashes.
4. Cache paths remain inside the allowed root. Only a complete matching download with stable pre/post metadata replaces cached content.
5. Posted movements remain separate from purchases, service months, liabilities, snapshots, claims, and projections.
6. Derived artifacts identify inputs or a manifest and applicable code or rule version.
7. Missing, unmatched, excluded, ambiguous, and resolved records retain scope, reason, sources searched, status, and disposition.
8. Replay copies only declared matching inputs into temporary isolation and compares declared outputs with frozen hashes.
9. Generation and validation do not imply publication; publication is separately recorded.
10. Credentials and authentication state stay outside the repository.

## Evidence, relationships, and time

A provider ID plus native metadata and locator is an original-source reference. Hash-verified bytes prove equality with pinned bytes, not current remote freshness or period completeness. Filename-derived periods remain labeled; absence from the 30-file catalog means outside indexed scope. Online verification additionally requires one matching provider ID and unchanged ID, modification time, size, and provider hashes across download. Offline checks cannot claim remote freshness. Snapshots are dated observations; the 2026-09-08 Notion snapshot is not a live sync.

A source can support many artifacts and an artifact can use many sources; manifests or provenance rows express that relationship. File links never substitute for financial allocations.

## Lifecycle

```text
source: discovered -> indexed -> locally verified -> remotely verified
                         `---------> failed/review
run: declared -> executing -> generated -> validated -> reviewed -> publishable -> published
                  `----------------> failed/review
```

Failure retains the previous pin and valid cache. Reviewed source changes create a new explicit expectation. Closed runs are immutable; corrections create a linked new run or versioned correction. Current run formats predate one enforced lifecycle schema, so absent state is unknown.

## Rejection and unsupported claims

Catalog construction rejects missing local sources or inventory entries, hash or size disagreement, and duplicate provider IDs. Fetch rejects absent or ambiguous IDs, duplicate paths, hash mismatch, metadata changes, and path escape. Replay rejects changed inputs, missing commands or outputs, failed commands, and output-hash differences.

Current code does not prove source-period completeness, transaction semantics, statement controls, a fresh-checkout closed-month replay, or publication. A passing hash check proves byte identity only.



## Verification

See [checks and historical results](../../../processes/cash-flow/model-validation/repository.md).
