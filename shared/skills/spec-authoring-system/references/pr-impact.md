# PR specification impact

Every implementation PR selects one disposition and identifies its evidence:

Use [create-spec-linked-pr](../../create-spec-linked-pr/SKILL.md) when preparing
the actual PR. Every PR includes a spec-derived acceptance checklist and an
explicit failure/blocker report. Definitive unresolved blockers link follow-up
issues; an issue link does not excuse an unmet acceptance criterion.

| Disposition | Required statement |
| --- | --- |
| Spec update | Canonical owner and affected guarantees, linked specs PR or exact spec revision, and validation evidence |
| Existing coverage | Exact applicable contract sections and why the implementation conforms without changing behavior |
| No spec impact | Concrete justification, such as a behavior-preserving internal refactor, and checks supporting that claim |

Changes to behavior, interfaces, configuration/defaults, persistence/identity,
permissions, error behavior, or supported use cases need authoritative coverage.
New experimental observations update experiment records and validation links;
they do not automatically alter the target contract. Routine changes need no
meaningless documentation diff.

For separate implementation/spec repositories, define the required merge order
and pin reviewed spec identities. A genuine merge gate must validate that the
linked change belongs to the designated specs repository and has reached the
required base branch. A URL or checkbox alone does not prove coverage.

When enforcement implementation is requested, prefer existing workflows and
validator code. Structural checks can validate metadata, templates, links, and
declared entry files. PR checks can validate disposition and referenced revision
or merge status. Reviewers assess substantive coverage. Describe unsupported
semantic checks honestly. Required-check and repository-rule configuration is a
separate activation step, not something a Markdown skill can enforce by itself.

Keep declarations in structured fields or one maintained PR section so the
check does not depend on arbitrary prose. A contributor-friendly failure names
the missing declaration or invalid reference and explains how to correct it.
Avoid unapproved administrative API calls, privilege broadening, or personal
credentials in CI. Test prospective checks with representative update,
existing-coverage, no-impact, missing-field, and invalid-reference cases before
describing them as operational.
