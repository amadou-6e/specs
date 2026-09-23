# Identity crosswalk

This view answers which identifiers join evidence, processing, and publication.

| Layer | Identity | Never substitute |
| --- | --- | --- |
| Domain | transaction, purchase, journey, matter, or claim ID | Description, amount, date |
| Drive | file ID and `drive:<id>` source ID | Path or filename |
| Gmail | message ID and `gmail:<id>` source ID | Subject, sender, thread display |
| Repository | run ID, artifact path plus hash, link ID | Timestamp alone |
| Notion | data-source ID, page ID, external ID | Title or view membership |

An allocation retains both endpoint IDs, exact amount/currency, evidence, and decision state. A returned Notion page ID is a projection alias, not a replacement domain ID.
