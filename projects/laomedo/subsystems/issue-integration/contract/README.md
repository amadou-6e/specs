---
title: Issue integration contracts
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-02
applies_to: [laomedo]
supersedes: null
related: []
---

# Issue integration contract index

[Interfaces](interfaces.md) own the proposed issue-context and reviewed
follow-up publication boundaries. Cross-system identities remain in
[shared contracts](../../../architecture/shared-contracts.md); this page does
not define an independent serialization.

Contract container: README.md (1), focused interface/configuration pages
(0..*). [Validation](../validation.md) records evidence and gaps.

- [GitHub Issue node](langflow-node.md): live repository/label/issue selection and narrow graph-triggered operations.
- [GitHub PR node](pr-node.md): matching PR selection, read-only viewing and scoped operations; separate creation proposal.
