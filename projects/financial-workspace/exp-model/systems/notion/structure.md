# Notion structure

These views answer how native objects, projection fields, and publication state relate. They introduce no guarantees beyond the contract. The [existing Cash Flow presentation](../../../model/systems/notion/presentation/procurement.md) preserves the concrete Procurement board, tables, charts, filters, helper scaffolding, placements, and native view IDs.

## Object and storage view

```text
workspace page
|-- database container
|   `-- data source (schema at observation time)
|       |-- row page 0..* (page ID + projected external ID)
|       `-- view 0..* (filters, sorts, layout, charts)
`-- linked views 0..*

dated local observation
|-- manifest: retrieval time, scope, counts, hashes, gaps
|-- schema/view captures
|-- row property export
`-- optional page-content export
```

The 2026-09-08 legacy Procurement snapshot covered 260 rows across 12 databases and fully paginated 12 unfiltered views. The 2026-09-09 receipt describes a different unified destination: 248 created, 12 matched, 260 source IDs verified, and one retained example without a source link. Neither proves current contents.

## Projection mapping view

| Meaning | Notion representation | Constraint |
| --- | --- | --- |
| Projection identity | Source ID or canonical ID | Unique in target; page ID retained |
| Display | Name | Never identity |
| Time | Date, Payment date, Service Month | Roles remain distinct |
| Money | Price; Original amount plus Currency | Missing is not zero; no implicit FX |
| Classification | Category, Status, service/liability fields | Domain semantics govern |
| Provenance | Evidence, Gmail link, source fields | Original provider remains authoritative |
| Presentation | helpers, flags, formulas, chart scaffold rows | Excluded from canonical facts |

The historical migration mapped Completed to Confirmed and retained Pending; this is migration behavior, not a universal lifecycle equivalence. Transport keys such as date:Date:start are importer serialization, not native property names.

## Publication-state view

```text
package -> validated -> fresh baseline comparison
        -> create / update / unchanged / conflict / excluded
        -> package-bound approval -> identity/schema recheck
        -> published receipt -> post-write verification
```

Conflict, stale/incomplete baseline, target mismatch, schema drift, package change, or missing approval blocks mutation. The representative 2025-12 test reached validation only: all four records were skip_existing, the baseline covered five candidate identities rather than the complete month, approval was absent, and publication remained not_run.
