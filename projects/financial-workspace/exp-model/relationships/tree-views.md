# Views of the same graph

Repeated Transaction nodes below reference the same IDs.

```text
Account
+-- Financial institution
+-- Transaction statement
|   +-- Transaction
+-- Transaction
    +-- Single expense [when settled]
    |   +-- Single expense item
    |   +-- Receipt
    |       +-- Representation: email / PDF / scan / image
    +-- Payment occurrence
    |   +-- Recurring expense
    +-- Receipt [income-statement kind]
    +-- Single income [when received]
    +-- Cashflow entry
        +-- Cashflow sheet (Notion dataset)

Cashflow sheet
+-- Cashflow entry [realized when linked to this transaction]
```

The Cashflow entry attributes are described in the [field catalogue](../objects/field_catalogue.yml); they are not child objects in this relationship tree.

## Recurring expense subtree

```text
Recurring expense
|-- [1 : 0..*] Commitment term
+-- [1 : 0..*] Payment occurrence
```

The zero lower bound makes Commitment term optional for a recurring expense. Each term belongs to exactly one recurring expense.

## Recurring income and receipt detail

```text
Recurring income
+-- [0..1 : 0..*] Receipt [income-statement kind]
    +-- [1 : 0..*] Income statement item
```

The payer or employer name is a field on Recurring income and the issuing name is a field on its Receipt. Neither is a separate object.

## Account and liability relationship tree view

```text
Account
|-- [0..1 : 0..*] Balance item
+-- [0..1 : 0..*] Liability
    |-- [1 : 0..*] Liability term
    +-- [0..1 : 0..*] Balance item
```

A Liability need not yet be linked to an Account. Its Liability terms are optional, and each Balance item belongs to either an Account or a Liability. Balance items remain dated observations, never cashflow rows.

## Planning relationship views

```text
Account
|-- [0..1 : 0..*] Budget
+-- [0..1 : 0..*] Forecast

Cashflow sheet
+-- [1 : 0..*] Cashflow entry [expected or realized]
    +-- [0..* : 0..1] Transaction [required when realized]

Budget
+-- [0..* : 0..*] Cashflow entry

Forecast
+-- [0..* : 0..*] Cashflow entry
```

An expected Cashflow entry has a reviewed commitment or contract basis, expected date, signed amount and currency. Receipt support is optional. On settlement, preserve entry_id, link the posted Transaction and set realization_status to realized. Income and expense objects classify or explain the row; Budget and Forecast connect to the row itself.

## Reimbursement links

~~~text
Receipt [income-statement kind]
+-- [1 : 0..*] Income statement item
    +-- [0..* : 0..*] Single income [income_kind: reimbursement]
        |-- [1 : 0..*] Single income item
        +-- [0..* : 0..*] Single expense or Single expense item
~~~

The Income statement item is a component of the salary evidence. It supports a reimbursement-kind Single income, which links to the expense being repaid. This does not create a second expense or a second booked salary transaction.
