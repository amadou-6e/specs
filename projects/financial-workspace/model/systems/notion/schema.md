# Existing Cash Flow schema contract

This contract preserves the concrete Notion Cash Flow structure observed in saved artifacts on 2026-09-09 and the destination IDs recorded on 2026-09-14. It is a dated schema observation. A fresh baseline must confirm it before any write.

## Container topology

| Object | Native identity | Observed role |
| --- | --- | --- |
| Financial Workspace page | `page:17814a27-4b73-80a7-9bb2-f1125c8ee9bc` | Parent workspace |
| Cash flow page | `page:3d714a27-4b73-8129-ad21-e4186c4b057f` | Cash-flow section |
| Procurement page | `page:3d614a27-4b73-81bf-a713-f045c52307de` | Unified procurement workspace |
| Procurement data source | `collection:58795b7f-dcaa-417a-ae21-4a438dc768c3` | Purchase rows and chart helpers |
| Recurring expenses database | `database:a2ec6ee9-9d77-4e4f-b460-6ec06747b0e3` | Recurring-expense projection |
| Recurring expenses data source | `collection:8ce81817-8ecb-40b2-a707-89b0dcc47e41` | Recurring-expense rows |
| Liabilities database | `database:ac4cd751-2dba-4881-857b-7a19ee9f619c` | Liability projection |
| Liabilities data source | `collection:8dcd99e7-ae11-48c4-9093-724b20d48aef` | Liability rows |

The saved configuration does not contain complete property and view captures for Recurring expenses or Liabilities. Their IDs and roles are preserved here, but their schemas remain an explicit discovery gap.

## Unified Procurement properties

### Operational properties

| Property | Observed type or representation | Meaning and constraint |
| --- | --- | --- |
| `Name` | title | Human-readable purchase or item title; never identity |
| `Category` | multi-select | One or more procurement categories; category table and chart dimension |
| `Status` | multi-select | Workflow value: `Pending`, `Approved`, or `Confirmed` |
| `Price` | number | EUR amount included in euro charts; empty for non-EUR and unknown amounts |
| `Date` | date | Purchase/order date, distinct from payment and travel dates |
| `Merchant` | text | Merchant or provider named by purchase evidence |
| `Source ID` | text | Stable projection identity, including `gmail:<message_id>` for email-derived rows |
| `Source category` | text | Original extraction category before Notion category mapping |
| `Currency` | select or text; exact native type not captured | Original currency such as EUR or USD |
| `Original amount` | number | Amount in `Currency`; retained for EUR and foreign-currency records |
| `Evidence` | text | Concise evidence/source description, not the original evidence object |
| `Gmail link` | URL | Direct message link using the retained Gmail message ID |
| `Payment source` | select or text; exact native type not captured | Verified settlement source such as PayPal, Revolut, SSKM, Vinted Balance, Bank, or Mixed |
| `Payment date` | date | Verified settlement date, distinct from purchase/order date |
| `Reference` | text | Bank transfer reference or other payment/order reference when available |

The migration added `Merchant`, `Source ID`, `Source category`, `Currency`, `Original amount`, `Evidence`, `Gmail link`, `Payment source`, and `Payment date`. `Reference` appears in the current validated upload contract. Where the artifact does not retain the provider-native type, this specification records the semantic field and leaves the exact type subject to live verification.

### Presentation-helper properties

| Property | Function |
| --- | --- |
| `Chart helper` | Identifies zero-value calendar scaffold rows and excludes them from operational/category totals |
| `Day` | Daily chart grouping |
| `Week` | Weekly chart grouping |
| `Month` | Monthly chart grouping |
| `Quarter` | Quarterly chart grouping |
| `In last week` | Rolling-period membership for category-share chart |
| `In week to date` | Rolling-period membership for category-share chart |
| `In last month` | Rolling-period membership for category-share chart |
| `In month to date` | Rolling-period membership for category-share chart |
| `In last year` | Rolling-period membership for category-share chart |
| `In year to date` | Rolling-period membership for category-share chart |

The saved artifacts record the helper names and behavior but do not preserve every native formula or property type. A schema refresh must capture those definitions before attempting reconstruction. Helper rows have `Price = 0`, are hidden from operational views, and span 2025-07-08 through 2027-12-31. Each day has category-aware and status-aware scaffolding so filtering by Category, Status, or both does not remove empty time buckets.

## Category and status vocabularies

The configured category tables are `Projects`, `Home`, `Health`, `Sports`, `Mobility`, `Accommodation and Activities`, `Travel Equipment`, `Presents`, `Electronics`, `Consumables`, `Clothing`, and `Books and Study Material`. Historical artifacts contain spelling variants such as `Mobilität`, `Accomodation & Activities`, and `Books & Study Material`; these require explicit migration mappings rather than silent renaming.

Status order is `Pending`, `Approved`, `Confirmed`. The legacy value `Completed` was mapped to `Confirmed` during the unified migration. Status does not by itself prove settlement.

## Money and evidence rules

- EUR records store the amount in both `Price` and `Original amount`; euro charts aggregate `Price`.
- Foreign-currency records retain `Original amount` and `Currency`; `Price` remains empty unless a reviewed EUR conversion is supplied.
- Unknown amounts remain empty rather than zero.
- Gmail-derived rows use unique `gmail:<message_id>` source IDs. One email can support multiple item rows, so item-level identity must remain distinguishable when that occurs.
- Payment source and payment date are populated only from sufficiently strong evidence. Missing or ambiguous settlement evidence remains empty.
