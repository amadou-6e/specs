# F-001 — Centerline presence does not always establish coordinate semantics

## Characterization

- Classification: synthesis
- Status: supported
- Confidence: high

## Finding

A dataset may contain both a surface and centerline files without explicitly stating
that the coordinates share the same physical world frame.

## Supporting sources

- [S-001 — AAA-100](../sources/S-001-aaa-100.md)
- [S-002 — AneuriskData](../sources/S-002-aneurisk.md)
- [S-003 — ASOCA](../sources/S-003-asoca.md)
- [S-004 — AneuX](../sources/S-004-aneux.md)

## Evidence

The originating survey found an explicit world-coordinate statement for AAA-100 but
classified equivalent coordinate semantics as unspecified for AneuriskData, ASOCA,
and AneuX.

## Applicability to Theseo

An adapter must verify or encode the surface-to-path transform rather than assuming
alignment from matching file presence.

## Limitations and counterevidence

The absence of a statement in the inspected material does not prove misalignment; it
means the relationship remains unverified.

## Consequences

Require coordinate-frame evidence or an empirical alignment check before admitting a
dataset route to evaluation.
