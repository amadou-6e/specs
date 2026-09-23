# Existing Cash Flow presentation

This view records the concrete Notion layout preserved by `notion/examples/kanban_configuration.json` and `unified_procurement.json`. It was verified on 2026-09-09 and requires a live parity check before being described as current.

## Page and database layout

The grouping below is conceptual. The saved ID catalog identifies Cash flow, Procurement, Recurring expenses, and Liabilities, but does not verify their parent-child placement as of 2026-09-14. Procurement configuration separately records its Financial Workspace parent on 2026-09-09.

```text
Financial Workspace
`-- Cash flow
    |-- Procurement
    |   |-- Unified Procurement database
    |   |   |-- Workflow                         # First view; board grouped by Status.
    |   |   |-- All purchases                    # General table.
    |   |   `-- <Category>                       # One filtered table per category.
    |   |-- Spend by category                    # Separate bar-chart element.
    |   |-- Procurement over time                # Separate tabbed line-chart element.
    |   |-- Procurement over time by category    # Separate tabbed line-chart element.
    |   `-- Procurement share by category        # Separate tabbed donut-chart element.
    |-- Recurring expenses                       # Existing source; layout not captured locally.
    `-- Liabilities                              # Existing source; layout not captured locally.
```

The legacy Procurement page is `page:17814a27-4b73-804e-af3a-c9bde0a909b6`. The unified Procurement workspace replaced its operational role while retaining legacy databases as a nested historical area. An earlier database with data source `collection:838a0ea4-5da5-475d-a0e1-b99dad396768` was recorded as trashed.

## Operational views

| View | Native identity | Layout | Configuration |
| --- | --- | --- | --- |
| Workflow | `view:3d614a27-4b73-815f-959e-000c90ca62d2` | Board | First view; grouped by Status in `Pending`, `Approved`, `Confirmed` order |
| All purchases | `view:3d614a27-4b73-81b5-8e06-000cc2a08cc4` | Table | General ungrouped inspection view |
| Projects | `view:3d614a27-4b73-81a5-b8bd-000c429313a3` | Table | Category-filtered |
| Home | `view:3d614a27-4b73-81f9-9eae-000cef25e7f2` | Table | Category-filtered |
| Health | `view:3d614a27-4b73-810a-b3e5-000cd9b3297c` | Table | Category-filtered |
| Sports | `view:3d614a27-4b73-819b-ae26-000cbabe5218` | Table | Category-filtered |
| Mobility | `view:3d614a27-4b73-81f0-9ddf-000cb5f84bf4` | Table | Category-filtered |
| Accommodation and Activities | `view:3d614a27-4b73-8199-99c8-000caae8eafb` | Table | Category-filtered |
| Travel Equipment | `view:3d614a27-4b73-81e7-9a9e-000c1e55e16f` | Table | Category-filtered |
| Presents | `view:3d614a27-4b73-817a-961c-000c1bf66b4a` | Table | Category-filtered |
| Electronics | `view:3d614a27-4b73-81aa-a802-000cce7b323d` | Table | Category-filtered |
| Consumables | `view:3d614a27-4b73-810a-b427-000cfa1830ea` | Table | Category-filtered |
| Clothing | `view:3d614a27-4b73-81ac-898e-000c26058406` | Table | Category-filtered |
| Books and Study Material | `view:3d614a27-4b73-81c4-b947-000c414f1426` | Table | Category-filtered |

Notion hides empty select groups. At the observation date, at least one row existed in each workflow status so all three board columns were visible. This behavior is presentation state and must not be satisfied by fabricating financial records.

## Chart elements

| Element | Layout and aggregation | Tabs or grouping | Filters and behavior |
| --- | --- | --- | --- |
| Spend by category | Bar; sum of Price | Category | User filters: Category, Status, Date, Price; fixed exclusion of Chart helper rows |
| Procurement over time | Line; sum of Price; period ascending | By week, By month, By quarter, By day | Uses Week, Month, Quarter, Day and calendar scaffold to retain empty periods |
| Procurement over time by category | Line; sum of Price; Category series | By week, By month, By quarter, By day | User filters: Category, Status, Date, Price; empty periods retained |
| Procurement share by category | Donut; sum of Price; value descending | Last week, Week to date, Last month, Month to date, Last year, Year to date, All time | Category, Status, Date, Price plus rolling-period helper |

All charts are separate linked database elements on the Procurement page rather than tabs on the operational database. The saved placements put Spend by category below the main database, Procurement over time below it, Procurement over time by category below that, and Procurement share by category in the right column beside Spend by category.

## Observed population

At 2026-09-09T12:26:30Z the unified source configuration recorded 407 rows: 22 Pending, 1 Approved, and 384 Confirmed. This comprises 260 legacy records, one retained example, and 146 imported purchases. Zero-value scaffold rows are separately described in the saved configuration. Counts are historical observations, not invariants.
