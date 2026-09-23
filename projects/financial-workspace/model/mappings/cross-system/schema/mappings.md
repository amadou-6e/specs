# Mappings and handoff envelopes

This page defines minimum conceptual records until shared versioned schemas implement them.

- A source reference carries schema version, namespaced source ID, system/object type, native ID, observation time, availability, provenance, and, when available, URL, coverage, MIME type, size, hash, account, provider, and parser version.
- A reconciliation link carries link ID, typed endpoints, relation/status, method, evidence, decision source, and schema/rule version. Monetary links add exact allocation, currency, tolerance, and remainder.
- A projection carries destination/data source, stable external ID, canonical ID, schema version, values, run ID, output hash, and action intent. Returned page IDs become verified aliases.
- Review carries run/package hash, baseline identity/hash/time, validation, exceptions, reviewer, decision/time, and exact action set. Publication adds per-action outcomes and verification.

Approval is invalid when package hash, destination, baseline-dependent action set, or schema changes. Identity-safe round-trip resolution is required even when provider presentation is lossy.
