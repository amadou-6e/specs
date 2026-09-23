# Template rules

Define filing, identity, consistency, lifecycle, and interpretation constraints. Link to the owning procedure for operational steps and checks.

## Basis

Record sources and dates supporting concrete claims.

## Instance and artifact rules

1. A real model entry may show only examples derived from verified instances in the Financial Workspace model.
2. Every example records the owning source system, provider-native identity, native position or safe stable link, and observation date.
3. Raw statements, salary documents, receipts, emails, attachments, and exports remain in their source system. Local copies may exist only in ignored temporary or cache directories and are not specification content.
4. A redacted checked-in projection contains only fields required to explain the model and retains traceability to its source.
5. Proposed or hypothetical shapes belong in `schema.md`; they are not model instances and must not be placed under a real entry's `examples/` folder.
6. When no verified model instance exists, omit `examples/` and record the evidence gap explicitly.
