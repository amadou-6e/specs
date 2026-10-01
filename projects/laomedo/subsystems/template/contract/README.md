# Run catalogue example contract

This page owns the example catalogue's observable behavior. It references the
[subsystem overview](../README.md); internal components belong to its design.
The contract container owns `1 README.md` and currently has no additional pages.

Registering a previously unseen run ID creates one record containing its supplied
workspace reference, initial state and creation time. Registering the same ID
with conflicting identity fields rejects the request and preserves the existing
record. Looking up an unknown ID returns missing-record rather than a fabricated
queued state.

The catalogue accepts ordered runner updates. A duplicate update identifier does
not create another history event. Conflicting content for the same update ID is
rejected; an older update cannot replace the latest state. Terminal updates retain
output and trace refs when supplied; missing refs remain explicitly unknown.

Example: after updates 1 (queued) and 2 (running), receiving update 1 again keeps
the current state running. A caller cannot infer completion from an output ref
alone. Retention periods, access rules and the public serialization schema must
be specified for a real subsystem before this example becomes deployable guidance.
