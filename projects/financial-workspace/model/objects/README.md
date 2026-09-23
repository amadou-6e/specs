# Model objects

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
objects/
├── 1 README.md
└── 0..* <domain>/ entries
```
<!-- END GENERATED: contained-elements -->

## Shared guarantees

- Every entity has a canonical identity; provider-native identity is provider scoped.
- Money uses decimal semantics and retains ISO 4217 currency at source precision.
- Unknown, missing, inferred, planned, expected, observed, and reconciled states remain distinct.
- Event dates, effective periods, reporting periods, observation times, and snapshot cutoffs remain distinct.
- Many-to-many monetary relationships use explicit reconciliation links and allocations.
- Evidence retains provenance, source identity, coverage, and hashes when bytes are available.
- Corrections preserve aliases, reviewed decisions, and superseded history.

## Domain catalog

- [Accounts](accounts/README.md): Owns financial accounts and their stable identity independently of provider display names or repository paths.
- [Transactions](transactions/README.md): Owns observed movements of money, transfers, settlement state, and provider transaction dates.
- [Procurement](procurement/README.md): Owns orders, purchase items, merchants, commercial dates, returns, and merchant refunds.
- [Recurring expenses](recurring-expenses/README.md): Owns continuing services, contracts, billing schedules, service periods, and cancellation state.
- [Everyday spending](everyday-spending/README.md): Owns receipt-backed and statement-derived routine consumption classifications that do not require procurement item tracking.
- [Travel](travel/README.md): Owns journeys, route segments, bookings, travel dates, tickets, accommodation, and personal or work classification.
- [Matters](matters/README.md): Owns stateful returns, claims, reimbursements, disputes, deposits, and recoverable balances that may produce future movements.
- [Tax](tax/README.md): Owns tax-year matters, classifications, filings, assessments, payments, refunds, and jurisdiction-specific status.
- [Financial position](financial-position/README.md): Owns point-in-time assets, liabilities, balances, valuations, and monthly snapshots.
- [Evidence](evidence/README.md): Owns system-independent evidence references, assertions, provenance, coverage, and transformation lineage.
- [Reconciliation](reconciliation/README.md): Owns candidate and reviewed links, monetary allocations, matching decisions, ambiguity, and exceptions.

## Ownership boundary

Domain folders own economic meaning. [System models](../systems/README.md) own native representations. [Cross-system mappings](../mappings/cross-system/README.md) own crosswalks and authority precedence. Processes own operational sequencing.

## Instance boundary

This catalogue specifies the financial object types used by Financial Workspace. It does not store source documents or invented instances. A concrete object example is valid here only when it is a redacted projection of an object verified in the actual model and linked to its owning Gmail message, Google Drive file, Notion page, bank source, or other source-system position. Source bytes may be pulled into ignored temporary or cache directories for inspection, but they do not become specification files.

## Source-linked example contract

A populated domain example contains one human-readable `README.md`, one `source-reference.yaml`, and one `projection.yaml`. The source reference records the owning system, provider-native identity, observed location or stable link, MIME type or artifact format, observation date, evidence role, supported claims, and limitations. The projection contains only fields supported by that source and explicitly lists redactions. One source may support many objects, and one object may require many sources.
