---
title: Worlds and geometry
status: draft
kind: subsystem
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-anysearch]
related:
  - legacy/rust-voxel-spec
  - legacy/rust-world
  - legacy/rust-ingest
---

# Worlds and geometry

This subsystem supplies occupancy and geometry to environments without requiring every world to be materialized as a dense array. It owns coordinate conversion, bounded reads, immutable base geometry, per-episode mutations, compiled packs and their integrity. Episode rules, route feasibility, provider discovery, and task selection belong elsewhere.

This description is based on product repository `theseo-anysearch` revision `72a413a` (`origin/develop`). It is **draft**: the historical fixed-1000³/HashMap-only descriptions in [the archived world document](../../legacy/rust-world.md) are not the current universal contract, and performance claims for every possible world shape have not been established.

Environment runtime, planners, observation builders, world providers, and the replay viewer consume bounded occupancy or compiled artifacts. A compiled world can be shared as one base allocation while each episode keeps its own overlay. Live environment axes remain bounded by the native task-coordinate limit even though the storage manifest uses wider coordinates.

Read the [contract](contract/README.md) for behavior, the [design](design/README.md) for storage and compiler flow, and [validation](validation.md) for evidence and remaining gaps.
