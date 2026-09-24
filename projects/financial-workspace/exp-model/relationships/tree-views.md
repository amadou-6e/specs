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
    +-- Payment occurrence
    |   +-- Recurring commitment
    +-- Income statement
    |   +-- Employer
    +-- Cashflow entry
        +-- Cashflow sheet (Notion dataset)

Cashflow sheet
+-- Cashflow entry [one per transaction]
    +-- Amount, Currency, Date, Account [from transaction]
    +-- Type and Expense category [reviewed classification]
    +-- Receipt links and item descriptions [when available]
    +-- Commitment and service period [when applicable]
    +-- Income statement details [when applicable]
    +-- Personal/work, reporting treatment, match status
```

## Recurring commitment subtree

```text
Recurring commitment
|-- [1 : 0..*] Commitment term
+-- [1 : 0..*] Payment occurrence
```

The zero lower bound makes Commitment term optional for an commitment. Each term belongs to exactly one commitment.

## Income statement subtree

```text
Employer
+-- [1 : 0..*] Income statement
    +-- [1 : 0..*] Income statement item
```

## Account balance and Liability subtree

```text
Account
|-- [1 : 0..*] Balance item
+-- [0..1 : 0..*] Liability
```

A Liability need not yet be linked to an Account. Balance items remain dated observations, never cashflow rows.
