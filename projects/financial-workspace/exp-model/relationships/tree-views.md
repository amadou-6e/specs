# Views of the same graph

Repeated Transaction nodes below reference the same IDs.

```text
Account
+-- Financial institution
+-- Transaction statement
|   +-- Transaction
+-- Transaction
    +-- Procurement
    |   +-- Procurement item
    |   +-- Receipt
    |       +-- Representation: email / PDF / scan / image
    +-- Recurring-payment occurrence
    |   +-- Recurring-payment agreement
    +-- Income statement
    |   +-- Employer
    +-- Cashflow entry
        +-- Cashflow sheet (Notion dataset)

Cashflow sheet
+-- Cashflow entry [one per transaction]
    +-- Amount, Currency, Date, Account [from transaction]
    +-- Type and Expense category [reviewed classification]
    +-- Receipt links and item descriptions [when available]
    +-- Agreement and service period [when applicable]
    +-- Income statement details [when applicable]
    +-- Personal/work, reporting treatment, match status
```

## Recurring-payment agreement subtree

```text
Recurring-payment agreement
|-- [1 : 0..*] Agreement term
+-- [1 : 0..*] Recurring-payment occurrence
```

The zero lower bound makes Agreement term optional for an agreement. Each term belongs to exactly one agreement.
