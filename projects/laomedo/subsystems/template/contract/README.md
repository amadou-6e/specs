---
title: Resume contract example
status: template
kind: contract
owners: [laomedo-maintainers]
last_reviewed: 2026-10-01
applies_to: [laomedo]
supersedes: null
related: []
---

# Resume contract example

Illustrative requirement: resume identifies expected native thread and last post-run
hash. An absent snapshot fails before native dispatch or ledger reservation. Fresh mode
allocates a distinct workspace/run rather than replaying prior side effects. Cancellation
retains received partial events. An actual interface must name its documented errors.

Shared IDs: [records](../../../architecture/shared-contracts.md). Evidence: [validation](../validation.md).
Contract container: README.md (1), focused interface/configuration pages (0..*).
No new implementation guarantee is asserted by this example.
