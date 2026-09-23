---
title: Tax rules
status: draft
kind: entity-model
owners: [amadou-6e]
last_reviewed: 2026-09-23
applies_to: [financial-workspace]
supersedes: null
related: [model/mappings/cross-system]
---

# Tax rules

- Tax relevance does not move an expense out of its natural domain.
- Jurisdiction and tax year form the tax-year identity.
- Expected liabilities and receivables remain distinct from actual payments and refunds.
- Filing, assessment, correspondence, payment, and refund dates remain distinct.

Invalid identities, impossible dates, currency conflicts, unsupported inference, or contradictory evidence require rejection or review.

## Admissible source artifacts

Filing protocols, assessments, authority correspondence, wage-tax certificates, and payment evidence may support Tax objects. Compound PDFs may support several tax events. Authentication certificates, private keys, and PKCS12 files are security material and must never be fetched as examples or routine evidence. Every checked-in example records the source-system identity and limitations; raw source bytes remain external or in ignored temporary storage.
