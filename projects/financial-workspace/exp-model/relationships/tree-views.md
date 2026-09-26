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

~~~text
Account
|-- [0..1 : 0..*] Budget
+-- [0..1 : 0..*] Forecast

Budget
|-- [0..* : 0..*] Single expense
+-- [0..* : 0..*] Single income

Forecast
|-- [0..* : 0..*] Single expense
+-- [0..* : 0..*] Single income

Single expense
|-- [1 : 0..*] Single expense item
|   +-- [0..* : 0..*] Receipt [when the receipt documents this item]
+-- [0..* : 0..*] Receipt [when the receipt documents the whole expense]

Single income
|-- [1 : 0..*] Single income item
+-- [0..* : 0..*] Transaction [only once received]
~~~

Budget and Forecast are optional Account-scoped planning objects. Planned Single expense and Single income events may have no Transaction. Their links to budgets and forecasts do not create cashflow rows.

## Reimbursement links

~~~text
Receipt [income-statement kind]
+-- [1 : 0..*] Income statement item
    +-- [0..* : 0..*] Single income [income_kind: reimbursement]
        |-- [1 : 0..*] Single income item
        +-- [0..* : 0..*] Single expense or Single expense item
~~~

The Income statement item is a component of the salary evidence. It supports a reimbursement-kind Single income, which links to the expense being repaid. This does not create a second expense or a second booked salary transaction.
