# Notion rules

This contract defines testable guarantees for Notion-native objects and Financial Workspace projections without redefining the domain entities being projected.

## Native identity and schema

Every retained reference records object type, native ID, and observation time. Workspace/page, database, data-source, view, and row/page IDs are distinct. Identity cannot be derived from title, displayed location, parent page, inline placement, view membership, or a collection URL.

A schema observation records destination data-source ID, property name, provider property ID when available, type, options or relation target, formula/rollup definition when available, and retrieval time. A type, option-semantics, relation-target, formula, or writable-status change is schema drift.

Locally recorded IDs observed on 2026-09-14 are Procurement page 3d614a27-4b73-81bf-a713-f045c52307de and data source 58795b7f-dcaa-417a-ae21-4a438dc768c3; Recurring database a2ec6ee9-9d77-4e4f-b460-6ec06747b0e3 and data source 8ce81817-8ecb-40b2-a707-89b0dcc47e41; Liabilities database ac4cd751-2dba-4881-857b-7a19ee9f619c and data source 8dcd99e7-ae11-48c4-9093-724b20d48aef. These require reverification before writes.

## Rows, identity, and deduplication

Each row retains its Notion page ID. A managed projection also carries a stable external identity such as Source ID, transaction_id, or (service_id, service_month). Page ID and external identity are separate aliases. A legacy row without external ID remains keyed by page ID and cannot be merged solely by name, merchant, amount, date, or reference.

Deduplication compares exact external identity against a fresh scoped baseline. No match permits create; exactly one match permits unchanged or an approved update; multiple matches are a conflict. Matching evidence may propose a legacy link but cannot confirm one by itself.

## Fields, time, money, and evidence

Required meaning comes from the financial-domain and publication contracts. Name is presentation. Commercial date, payment/posting date, service month, due date, last-verified date, and retrieval time remain distinct. Amount and currency stay paired; missing is not zero and foreign currency receives no implicit FX conversion.

Evidence text and links are convenience projections; original evidence remains authoritative in its provider. Formulas, rollups, chart helpers, calendar scaffolds, and dashboard aggregates are presentation state and cannot prove a transaction. Expected recurring rows and liability balances do not become transactions through display.

## Baselines and publication

A baseline names destination IDs, retrieval time, scope/filter, pagination completion, row identities, relevant properties, and gaps. Full coverage requires complete pagination of every intended source/view and requested page content. Historical exports are never current baselines.

Comparison produces create, update, unchanged/skip_existing, conflict, or excluded. Multiple matches, missing required identity, stale/incomplete baseline, changed package hash, target mismatch, schema drift, or unsupported conversion blocks the affected write and normally publication.

Approval binds package hash, destination, schema expectation, and action set. A writer rechecks identity before mutation, applies only approved actions, and records time, external ID, old/returned page ID, result, and error. Retry must not create duplicates. Partial failure preserves completed actions in the receipt and recovery starts from a new baseline.

Rows may be archived/restored and pages moved or renamed without changing identity. Deletion, replacement of page IDs, or repurposing an entity row is unsupported. Domain status display does not establish settlement. Views, formulas, relations, charts, and automations are explicitly lossy outside Notion.

## Concrete schemas

The [existing Cash Flow schema](schema.md) records the observed container IDs, unified Procurement properties, helper properties, vocabularies, and money/evidence behavior. It is required reading for Cash Flow publication or migration.

## Verification

See [checks and historical results](../../../integrations/notion/model-validation.md).
