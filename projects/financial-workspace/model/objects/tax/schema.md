---
title: Tax entity catalog
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Tax schema

| Entity | Stable identity | Required meaning |
| --- | --- | --- |
| Tax year | `jurisdiction + tax_year` | lifecycle, filing status, assessment status |
| Tax classification | `classification_id` | subject, tax year, category, deductible share, evidence |
| Tax filing | `filing_id` | tax year, submitted version, submission date, acknowledgement |
| Tax assessment | `assessment_id` | tax year, authority reference, decision date, payable/refundable amount |

Unknown values remain null or explicitly unsupported. Display names, paths, amounts, and dates are never substitute identities.
