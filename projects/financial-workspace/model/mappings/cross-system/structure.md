# Cross System structure

This view answers where facts originate and what accompanies them across boundaries.

```mermaid
flowchart LR
  D[Drive evidence] -->|native ID, metadata, bytes/hash, coverage| R[Repository run]
  G[Gmail evidence] -->|message/thread IDs, bytes/hash, events| R
  B[Notion baseline] -->|page/data-source IDs, current values| R
  R -->|canonical IDs, links, decisions, exceptions, hash| P[Reviewed package]
  P -->|package-bound approval| N[Notion projection]
  N -->|receipt and comparison| A[Repository audit]
```

Drive and Gmail remain authoritative for originals. The repository owns normalization, links, decisions, gaps, and runs. Notion owns native presentation. A Drive review folder may hold a frozen package but not the only manifest or decisions. Failures return as explicit gaps or exceptions.
