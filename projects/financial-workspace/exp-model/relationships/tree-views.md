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
    |   +-- Recurring expense
    +-- Income statement
    |   +-- Employer
    +-- Cashflow entry
        +-- Cashflow sheet (Notion dataset)

Cashflow sheet
+-- Cashflow entry [one per transaction]
```

The Cashflow entry attributes are described in the [field catalogue](../objects/field_catalogue.yml); they are not child objects in this relationship tree.

## Recurring expense subtree

```text
Recurring expense
|-- [1 : 0..*] Commitment term
+-- [1 : 0..*] Payment occurrence
```

The zero lower bound makes Commitment term optional for a recurring expense. Each term belongs to exactly one recurring expense.

## Employment income subtree

```text
Employer
|-- [1 : 0..*] Recurring income
|   +-- [0..1 : 0..*] Income statement
+-- [1 : 0..*] Income statement
    +-- [1 : 0..*] Income statement item
```

## Account and liability relationship tree view

```text
Account
|-- [0..1 : 0..*] Balance item
+-- [0..1 : 0..*] Liability
    |-- [1 : 0..*] Liability term
    +-- [0..1 : 0..*] Balance item
```

A Liability need not yet be linked to an Account. Its Liability terms are optional, and each Balance item belongs to either an Account or a Liability. Balance items remain dated observations, never cashflow rows.
