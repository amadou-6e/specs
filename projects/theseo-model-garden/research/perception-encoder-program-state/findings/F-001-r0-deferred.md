# F-001 — v2r2 R0 deferred continuation

## Characterization

- Classification: source-reported experimental result
- Status: supported
- Confidence: high

## Finding

The retained v2r2 R0 result records `defer` and the stop
`no_topology_identifiable`: two held-out bins lacked negative-label support and the
supported `6+` bin failed all four conservative audit checks. No encoder architecture
was ranked or rejected.

## Supporting sources

- [S-004 — v2r2 R0 result](../sources/S-004-r0-result.md)

## Evidence

The result reports filled quotas, label support by span, the four failed bounds for
the supported bin, exact replay from saved predictions, and no candidate updates.

## Applicability to Model Garden

The finding governs interpretation of this registered audit and prevents treating its
stop as an encoder comparison. It applies only to the stated patch prior, spatial
transfer, controls, and budget.

## Limitations and counterevidence

The transfer `6+` entropy point estimate was low, so the source explicitly rejects the
stronger claim that hidden geometry was proven random or universally unidentifiable.

## Consequences

Any successor must use a new, reviewed contract rather than silently changing the
failed bins or thresholds under the same identities.
