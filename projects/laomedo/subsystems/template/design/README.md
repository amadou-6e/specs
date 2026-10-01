# Run catalogue example design

This page explains one illustrative realization of the
[catalogue contract](../contract/README.md). The design container owns
`1 README.md` and currently has no technology partitions.

A request handler validates identity fields, then writes registration or update
events to a storage adapter. A read projection derives the latest state from the
accepted sequence. Updating history and the projection in one transaction prevents
a lookup from seeing a state whose history is absent. The storage adapter owns
persistence; the request handler owns input validation; neither launches agents.

A uniqueness check on run and update IDs implements duplicate detection. Compare
the existing event payload before treating an update as a retry. Projection
rebuilds read the retained event order, which permits recovery after projection
loss. This example leaves the storage engine open: a real design must name its
concurrency assumptions, persistence guarantees and trade-offs.
