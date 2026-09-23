# Repository schema

## Identity and required fields

| Object | Stable identity | Non-identity locators |
| --- | --- | --- |
| Git state | Commit plus disclosed working-tree state | Branch name |
| Drive source | `drive:<native file ID>` | Path, URL, filename, legacy path, cache path |
| Run | Generated run ID | Directory display name |
| Artifact | Run ID, relative path, content hash | Report title |
| Exception | Register record reference | Free-text description |
| Canonical record | Domain ID from domain or cross-system contract | Provider references |

A source record requires provider ID, SHA-256, byte size, source type, current and cache locators, availability, and coverage with an explicit basis. Unknown coverage dates remain null. SHA-256 proves byte equality, not provider-object identity.
