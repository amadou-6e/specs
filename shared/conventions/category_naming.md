# Category naming

Use this convention when naming categories, types, classes, groups, or other reusable classification identifiers in specifications and metadata.

## Meta-rule

Name a category after the intrinsic, conventionally recognized kind of thing its members are, at the lowest stable level of abstraction shared by those members. Do not name a category after a temporary workflow role, current contents, pipeline position, implementation detail, product instance, or project-specific interpretation.

A category must remain accurate when the subject is considered outside the workflow and project in which it was first introduced.

## Selection order

Prefer candidate terms in this order:

```text
Established industry term
  > common product-category term
  > common technical noun phrase
  > carefully defined project-specific term
  > invented compound label
```

Before introducing an identifier, check whether the phrase:

1. Is used in vendor documentation, architecture diagrams, procurement catalogs, or ordinary professional discussion.
2. Would be understood by someone unfamiliar with this repository.
3. Describes approximately the same class when used by independent teams.
4. Returns the intended class of things when searched without project context.
5. Remains accurate if the subject's workflow role or stored content changes.

A description may refine a common term. It must not be used to rescue an unclear or invented identifier when a familiar term exists.

## Required tests

### Intrinsic kind

Name what the subject is. Store what it does in one workflow as a separate relationship or role.

```text
cloud-file-storage     # intrinsic category
statement-source       # contextual workflow role
```

### Stable abstraction

Choose a term specific enough to distinguish meaningful kinds and broad enough to survive ordinary implementation changes.

```text
storage                     # too broad
Google Drive invoice store  # too specific
cloud-file-storage           # stable category
```

### Consistent granularity

Sibling categories use comparable levels of abstraction. Do not mix a broad capability, a product name, a workflow-specific subtype, and a technical class in one category set.

```text
cloud-file-storage
email-service
git-repository
collaborative-workspace
```

### Category versus instance

A category describes a reusable class. A product, provider, deployment, or named component is an instance or entity.

```text
google-drive          # system entity
cloud-file-storage    # category
```

### Category versus workflow role

Workflow roles are modeled separately and may vary by process without changing the category.

```yaml
system: google-drive
categories:
  - cloud-file-storage
workflow_roles:
  procurement:
    - invoice-source
  monthly-close:
    - statement-source
```

## Identifier form

- Use lowercase kebab-case.
- Prefer a short noun or noun phrase.
- Prefer singular class names unless normal professional usage is plural.
- Avoid unexplained abbreviations.
- Avoid product names in reusable categories.
- Avoid vague suffixes such as `platform`, `solution`, `engine`, or `system` when a more precise established term exists.
- Do not combine several unrelated dimensions into one identifier.

## Examples

| Prefer | Avoid | Reason |
| --- | --- | --- |
| `cloud-file-storage` | `files-and-documents` | Names a recognized system category rather than its current contents. |
| `email-service` | `communication-evidence-platform` | Uses the common product category rather than a workflow interpretation. |
| `git-repository` | `processing-and-audit-system` | Names the technology class rather than current responsibilities. |
| `collaborative-workspace` | `review-and-publishing-system` | Remains valid outside one publishing workflow. |
| `payment-provider` | `financial-movement-source` | Uses established financial terminology. |
| `relational-database` | `structured-record-engine` | Uses the conventional architecture term. |

## Introducing an uncommon category

When no established term fits, record:

- the candidate terms considered;
- evidence that no common term expresses the intended class;
- the precise membership boundary;
- how the new term differs from adjacent categories; and
- why a workflow role, property, or relation cannot represent the distinction instead.

Project-specific naming guidance may add domain examples and prohibited ambiguities. It cannot weaken this convention.
