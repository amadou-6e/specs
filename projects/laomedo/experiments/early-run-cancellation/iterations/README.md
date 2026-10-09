# Iterations

- [2026-10-09](2026-10-09/README.md): installed Langflow graph cancelled one real Codex turn under the shared 4/4 cap. Visible Playground Stop and durable cross-store correlation remain unverified.
- [2026-10-09 visible Stop](2026-10-09-visible-stop/README.md): the visible Playground Stop cancelled one real Codex turn. Durable cross-store correlation remains unverified; the extended ledger is 5/12.
- [2026-10-09 pre-thread Stop](2026-10-09-prethread-stop/README.md): visible Stop cancelled one real prepared run before native thread creation. The extended ledger is 6/12, with no native model call in this case.
- [2026-10-09 server identity](2026-10-09-server-identity/README.md): two no-model invocations of one saved flow exposed distinct graph run IDs and matching flow/stage IDs; durable cross-store binding remains untested.
- [2026-10-09 Playground seam](2026-10-09-playground-seam/README.md): a no-model visible Send and Stop reached a fake host bridge with one persistent synthetic binding. Real runner dispatch and restart remain untested.
- [2026-10-09 host join](2026-10-09-host-join/README.md): zero-model restart and bridge-attribution gates passed; one later real Codex request joined across the stores but failed before a visible Stop. The shared ledger is 7/12.
