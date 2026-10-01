# Run catalogue example validation

This page maps the [example contract](contract/README.md) to verification.
These are planned checks with synthetic records; none has been implemented or run.

| Guarantee | Check and expected observation | Evidence state |
| --- | --- | --- |
| Stable identity | Register run-001 twice with different workspace refs; reject the second and retrieve the first unchanged | Planned |
| Explicit absence | Query missing-001; receive missing-record without a run state | Planned |
| Idempotent ordered updates | Deliver queued update 1, running update 2, then update 1 again; retain two events and running state | Planned |
| Conflicting update refusal | Resubmit update 2 with changed content; reject it and preserve history | Planned |
| Recoverable projection | Rebuild from retained events; compare current state and refs with the original projection | Planned |

For a real entry, replace planned cases with concrete test paths, fixtures and
commands when they exist. Record actual execution results separately from test
presence. Access policy, retention and concurrent writers remain coverage gaps
until the real contract settles those subjects.
