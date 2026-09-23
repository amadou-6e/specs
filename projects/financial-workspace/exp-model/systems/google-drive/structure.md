# Google Drive structure

This view preserves the concrete Google Drive hierarchy established before the model catalogue was introduced. It distinguishes the implemented remote structure from the intended target structure. Folder paths support navigation; Drive file and folder IDs remain authoritative identity.

The implemented hierarchy is a dated observation from **2026-09-13**, not a claim about the current remote state. The target hierarchy is normative intent; illustrative filenames do not assert that every shown file exists.

## Implemented remote structure

Verified against the connected Drive on 2026-09-13. The existing Financial folder was moved from Documents to the Drive root and renamed Financial Workspace; its folder ID and links were preserved. The following is the implemented remote hierarchy, not a local copy.

~~~text
My Drive/
+-- Documents/
|   +-- E-Commerce/Billing/Midjourney/  # Invoice and receipt PDFs
|   +-- Work/Siemens/Financial records/ # Siemens agreement
|   +-- Reisen/                         # Existing travel evidence
|   `-- other document areas
`-- Financial Workspace/
    +-- 🏦 Banking/
    |   +-- SSKM/2021/ ... 2026/
    |   +-- DKB/2023/ ... 2026/
    |   +-- PayPal/2023/ ... 2026/
    |   `-- Revolut/2023/ ... 2026/
    +-- 📉 Liabilities/
    |   +-- SSKM/S-Privatkredit/
    |   +-- KfW/2026/
    |   `-- BVA/
    +-- 🔁 Recurring spending/
    |   +-- Housing/2021/, 2024/, 2026/
    |   +-- Insurance/2023/, 2026/
    |   `-- Subscriptions/2026/
    +-- 🧾 Everyday spending/Receipts/2026/
    +-- 💼 Employment/bridgingIT/2024/ ... 2026/
    +-- 📈 Investments/
    +-- 🧮 Tax/
    |   +-- Elster/                      # Existing older tax files
    |   `-- 2026/
    |       +-- Income/
    |       +-- Deductions/
    |       +-- Filing/
    |       +-- Assessment/
    |       `-- Correspondence/
    +-- [Google Doc] Workspace links  # Links to purchase and travel folders
    `-- [Google Doc] README             # Explains the workspace and filing rules
~~~

The procurement automation folders remain separate at the Drive root: [Procurement imports](https://drive.google.com/drive/folders/1ZRcE8OLnbYVz3tbbnlyEAxtW91fK4xUk), [Incoming](https://drive.google.com/drive/folders/1OIm_NoHc-WPlIWTCCIk8ZYwDMyTPIwWn), [Needs review](https://drive.google.com/drive/folders/1yjfN5Zpd-cYfDme_QT7SUzFW-6Fnq2ry), [Processed](https://drive.google.com/drive/folders/1UfmtFudm3m8UTRJFABqcxT-8N2Q9NPbG), and [Failed](https://drive.google.com/drive/folders/1IROCGrG7ZuTkxbNOhQBNWuYlWN6GgLXX).

| Implemented remote location | Relation to proposal |
|---|---|
| [Financial Workspace](https://drive.google.com/drive/folders/11t4fi7yXKUSyZBpKkiuEehwxqXll6TN3) is a sibling of Documents, with [🏦 Banking](https://drive.google.com/drive/folders/1vQIl5CWKXT9ragc7Ml8YG_it1ictVczd), [📉 Liabilities](https://drive.google.com/drive/folders/1Tz0EyOtc1msQ3Fxp81OswPfNl9iB_Yuk), [💼 Employment](https://drive.google.com/drive/folders/18JclK-t-r1sPBQBBdKgrC8xAOgcSjK4g), [🧮 Tax](https://drive.google.com/drive/folders/1EfvBeHXYdjKtE-9S3B9DsPxdAyTflhd2), and the other proposed categories. | Matches the proposed top-level separation and main categories. |
| [PayPal](https://drive.google.com/drive/folders/1ClzG6OAFRx3txcx_cmGR0IU46lIwPgt4) and [Revolut](https://drive.google.com/drive/folders/1lnoY3R8RSyq2UzaCrVZlBY_q4LQDHyi3) statements are filed by year. The one Revolut file covering 2024 and 2025 is stored once under 2025. | Matches year grouping without duplicating cross-year evidence. |
| [SSKM loan](https://drive.google.com/drive/folders/1fokPnONYdp3us1ZMeQDFmWh7apmkXx-6) and [KfW](https://drive.google.com/drive/folders/1tx4YhVNV0gzUHm8DUKElEKNZDmFuEc7n) are under Liabilities; the dated KfW balance PDF is under 2026. | Matches the liability distinction. Undated loan files remain at provider level. |
| [Elster](https://drive.google.com/drive/folders/1JsLXmg2x8DVkUbij2AoyA0FFP7KvUAkL) is under Tax. | Older Elster files have not yet been classified into tax-year and document-type folders. |
| [Billing/Midjourney](https://drive.google.com/drive/folders/1E0jG_UbCaWX7HHgopAvZMJwAFs6C4Y6W) is under [E-Commerce](https://drive.google.com/drive/folders/1BNOTTGhBz6CA4S0Wd-Oo8f-LP0MVHse7). [Siemens financial records](https://drive.google.com/drive/folders/1b8ToXu8RtEOa2zSIx9UaAWEqg5TU4Wjo) are under the existing [Work/Siemens](https://drive.google.com/drive/folders/1k2DtLtCGUZIuBwwTBLdd9hjUpaCSp86R) folder. | Follows the explicit exceptions to the initial proposal. |
| [Recurring spending](https://drive.google.com/drive/folders/1bErFY9OC6HCf3jgy6NWsYBXDUr98CE-s), [Everyday spending](https://drive.google.com/drive/folders/1Rr0TqdpRuTk8mHB2UrzYf5Fpwe66cwzv), and [Investments](https://drive.google.com/drive/folders/1LAJZLhxkliR95pmE-5rdG5ocwhq95BHu) exist. [Workspace links](https://docs.google.com/document/d/14-h2WwcFpFYKDVveGAspKcE4eK-cGz1pRp8R4f1TqUo/edit) sits at the Financial Workspace root. | The native Google Doc links to the verified purchase and travel folders. [README](https://docs.google.com/document/d/1AtknilGP8OP8VvRN9U08vfABqhC2669euLQ-pjf9tnw/edit) explains the workspace; no dedicated Claims folder was identified. |

Population update, 2026-09-13: Three historical housing records were filed under Recurring spending/Housing/2021 and 2024. Three TK membership and payment-authorisation records were filed under Recurring spending/Insurance/2023. These years follow the available document dates; the actual expense periods have not been verified. Everyday spending and Investments still have no source evidence filed.

## Target structure

Google Drive should be organized by financial subject first and by year inside each provider or document class. This keeps the same account or obligation together across years.

Original financial evidence and workspace navigation documents belong here. Canonical normalized data, code, reconciliation decisions, and run manifests belong in the private repository or an indexed encrypted artifact store. Frozen Notion import packages may also be copied to the proposed Cash flow Drive folder for review, while the repository retains the reproducible package identity and hashes.

~~~text
Financial Workspace/
+-- 🏦 Banking/                                      # Original statements and bank correspondence.
|   +-- SSKM/
|   |   +-- 2024/  -> [PDF] SSKM_2024-12_Kontoauszug.pdf
|   |   +-- 2025/  -> [PDF] SSKM_2025-12_Kontoauszug.pdf
|   |   \-- 2026/  -> [PDF] SSKM_2026-08_Kontoauszug.pdf
|   +-- PayPal/
|   |   +-- 2024/  -> [PDF] PayPal_Umsaetze_2024.pdf
|   |   +-- 2025/  -> [PDF] PayPal_Umsaetze_2025.pdf
|   |   \-- 2026/  -> [PDF] PayPal_Umsaetze_2026.pdf
|   +-- Revolut/
|   |   +-- 2024/  -> [PDF] Revolut_2024.pdf
|   |   +-- 2025/  -> [PDF] Revolut_2024-2025.pdf
|   |   \-- 2026/  -> [PDF] Revolut_EUR_2026.pdf
|   \-- DKB/
|       \-- 2026/  -> [PDF] DKB_2026_Auszug-01.pdf
+-- 📉 Liabilities/                                  # Original evidence for loans and money owed.
|   \-- KfW/
|       \-- 2026/
|           +-- [PDF] KfW_Bildungskredit_Kontostand_2026-08.pdf
|           \-- [PDF] KfW_Zinsbescheinigung_2026.pdf
+-- 🔁 Recurring spending/                           # Financial documents for repeated obligations.
|   +-- Housing/
|   |   \-- 2026/
|   |       +-- [PDF] Mietvertrag.pdf
|   |       +-- [PDF] Nebenkostenabrechnung_2026.pdf
|   |       \-- [PDF] Strom_Jahresabrechnung_2026.pdf
|   +-- Insurance/
|   |   \-- 2026/
|   |       +-- [PDF] Versicherungspolice.pdf
|   |       \-- [PDF] Beitragsrechnung_2026.pdf
|   \-- Subscriptions/
|       \-- 2026/  -> [PDF] Jahresrechnung_2026.pdf
+-- 🧾 Everyday spending/                            # Original receipt images retained when useful.
|   \-- Receipts/
|       \-- 2026/
|           +-- 2026-08/
|           |   +-- [JPG] 2026-08-14_Supermarket_31-20.jpg
|           |   \-- [PDF] 2026-08-18_Restaurant_24-50.pdf
|           \-- 2026-09/
|               \-- [HEIC] 2026-09-03_Hardware-store_18-90.heic
+-- 💼 Employment/                                   # Financial employment evidence only.
|   \-- BridgingIT/
|       \-- 2026/
|           +-- [PDF] Lohnabrechnung_2026-08.pdf
|           +-- [PDF] Lohnsteuerbescheinigung_2026.pdf
|           \-- [PDF] Reisekostenerstattung_2026-05.pdf
+-- 📈 Investments/                                  # Statements, confirmations, and certificates.
|   \-- Broker name/
|       \-- 2026/
|           +-- [PDF] Depotauszug_2026-12-31.pdf
|           +-- [PDF] Jahressteuerbescheinigung_2026.pdf
|           \-- [PDF] Kaufabrechnung_EXAMPLE.pdf
+-- 🧮 Tax/                                          # Tax-year matters and original authority documents.
|   \-- <year>/                                     # Stable year folder; status lives in Matters and STATUS.
|       +-- STATUS, CHECKLIST, EVIDENCE MANIFEST, NEXT STEPS  # Living indexes linked to their canonical copies.
|       +-- subjects/                               # Funding, residence, exchange, employment, and other topics.
|       +-- review_artifacts/                       # Frozen findings and reviewed-input hashes.
|       +-- Filing/                                 # Original submitted returns and acknowledgements.
|       +-- Assessment/                             # Original assessment notices.
|       \-- Correspondence/                         # Original tax-authority correspondence.
+-- [Google Doc] Workspace links               # Links to related document areas.
\-- [Google Doc] README                       # Explains the workspace and filing rules.
~~~

Purchase and travel records remain in their subject folders, which hold invoices, tickets, itineraries, correspondence, and workflow state. The Finance Drive uses Workspace links to point to those verified folders and retains only independently financial documents, such as a reimbursement statement. A dedicated Claims folder has not been verified; claim evidence may remain with its purchase or journey.

The [Drive folder example](../../../integrations/google-drive/example/README.md) describes representative original statement PDFs, but the copied binaries remain local and are excluded from this specs repository. Names shown above for unavailable document types are illustrative and are not fabricated files.
