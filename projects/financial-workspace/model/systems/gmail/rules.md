# Gmail rules

This contract defines observable Gmail identity, evidence, coverage, and failure semantics without assigning financial meaning.

## Schema

See [schema](schema.md) for fields and identifiers.

## Relationships, time, and evidence

A known thread groups one or many independently addressable messages. A message has zero or many parts and attachments. Messages and attachments can support zero or many assertions and domain entities; domain entities can cite zero or many Gmail objects through explicit cross-system links.

Provider sent/internal/received time, retrieval time, and dates stated in content remain distinct. Order, invoice, service, travel, payment, posting, refund, and claim dates keep financial object-domain meanings. Labels and thread presentation are mutable.

Assertions cite the exact message and relevant part or attachment, observation time, method, and parser/rule version when automated. Captured bytes add MIME type, size, hash, and lineage. Hashes prove integrity only for captured bytes and never replace native identity. Subjects, snippets, filenames, and links may guide review but cannot replace body or attachment content.

An order confirmation supports an order but not a posted movement. A refund email neither erases the purchase nor proves a posted credit. Multi-item assertions need stable locators; ordinals are valid only under deterministic extraction. Thread context cannot silently lend evidence to every message.

## Coverage, correction, and failure

Candidate scope enumerates supplied IDs and cannot exclude other messages. Complete-period coverage requires exact query, mailbox, time interpretation, retrieval time, every page/cursor, terminal `has_more: false` or equivalent, returned IDs, exclusions, and failures. Missing pages, unknown account, unrecorded query, or access errors make coverage partial.

Re-extraction creates a new derived artifact or superseding assertion while retaining source identity. Inaccessible content, identity conflict, attachment failure, hash mismatch, parser failure, ambiguous items, and incomplete coverage create gaps. Deletion, legal hold, retention, permission history, label history, and exact thread mutation semantics remain unsupported until evidenced.

## Verification

See [checks and historical results](../../../integrations/gmail/model-validation.md).
