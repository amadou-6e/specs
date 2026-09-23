# Gmail schema

## Records and identity

| Record | Required representation | Optional when observed |
| --- | --- | --- |
| Mailbox observation | account scope, observation time, access result | provider account ID, limitations |
| Message | mailbox scope, Gmail message ID, retrieval status | thread ID, link, RFC Message-ID, participants, subject, sent/internal/received times, labels, MIME metadata |
| MIME part | parent message ID, part path, MIME type | disposition, charset, encoding, size |
| Attachment | parent message ID, Gmail attachment ID | part path, filename, MIME type, size, SHA-256 |
| Assertion | exact source, field, value, extraction method | confidence, parser/rule version, locator |
| Coverage | scope type, account, query or supplied IDs, retrieval time, result IDs, status and failures | pages/cursors, exclusions |

Unknown values remain null or unavailable; producers must not synthesize IDs, hashes, dates, recipients, or references. Gmail-native keys are `(mailbox_scope, gmail_message_id)`, `(mailbox_scope, gmail_thread_id)`, and `(mailbox_scope, gmail_message_id, gmail_attachment_id)`. Legacy `gmail:<message-id>` aliases are safe only in their documented single-mailbox scope. Derived `gmail:<message-id>:item:<ordinal>` identifies a repository candidate, not a Gmail object.

A browser link is navigation metadata. Account slot, label, sender, subject, date, filename, RFC Message-ID, and hash are not Gmail message keys. Exact native keys deduplicate observations. Conflicting content under one key is blocking; byte-equal attachments in different messages remain distinct.

