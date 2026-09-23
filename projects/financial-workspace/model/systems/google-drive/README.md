---
title: Google Drive financial model
status: draft
kind: system-model
owners:
  - amadou-6e
last_reviewed: 2026-09-23
applies_to:
  - financial-workspace
supersedes: null
related:
  - model/mappings/cross-system
  - model/systems/repository
  - integrations/google-drive
  - processes/cash-flow
---

# Google Drive model

## Contained elements

```text
<model-entry>/
├── 1 README.md
├── 1 structure.md
├── 1 schema.md or schema/
├── 1 rules.md or rules/
├── 0..1 examples/
└── 0..1 presentation/
```
This entry defines the Google Drive objects that preserve original financial evidence and workspace navigation. Drive owns native file and folder identity, current native metadata, access, and content; the repository owns reproducible catalogs, cached bytes, hashes, derived artifacts, exceptions, and process runs.

## Ownership and consumers

The owned elements are Drive workspaces, files, folders, parent relationships, and provider-native metadata needed to locate or retrieve evidence. Financial meaning belongs to the [financial object models](../../objects/README.md), repository copies and run artifacts to the [repository model](../repository/README.md), and relationships spanning systems to the [cross-system model](../../mappings/cross-system/README.md).

Cash-flow, procurement, recurring-expense, monthly-close, travel, claims, and tax workflows consume Drive evidence. Repository acquisition code and reviewers depend on stable file IDs, bounded discovery, explicit coverage, and byte verification. Folder paths and filenames aid navigation and matching but cannot establish canonical financial identity or workflow completion.

## Guarantees

1. A Drive file is identified by its opaque native file ID; repository aliases use `drive:<file_id>`.
2. Every observation has a scope and time. Absence from an inventory means only non-observation in that scope.
3. Content identity uses a recorded cryptographic hash when bytes are available. Equal names or sizes are insufficient; a changed hash requires review.
4. Coverage dates remain explicit and carry a basis. Filename-derived coverage is an inference.
5. A cache is replaceable and cannot become the only original. Derived text retains its source reference and its own hash.
6. Drive evidence and domain entities have a many-to-many relationship represented by the cross-system model.
7. Missing, inaccessible, ambiguous, changed-during-download, or hash-mismatched sources remain failures or gaps.

## Maturity and limitations

Status remains **draft**. Implemented repository behavior includes a 30-object source catalog, dated Drive metadata inventory, local and cached SHA-256 checks, read-only rclone discovery/download, post-download metadata comparison, safe cache replacement, and exception logging. A saved run reports 30 of 30 pinned originals verified remotely on 2026-09-15. These are historical observations, not proof of current Drive state or complete account/month coverage.

The concrete [folder topology](structure.md) preserves both the remote hierarchy verified on 2026-09-13 and the intended target hierarchy. It is part of this model, rather than merely an integration fixture. No current full-tree inventory, permissions audit, revision/version contract, shortcut resolution contract, trash-state policy, retention policy, or Google-native export contract was verified. Evidence was inspected in the outer workspace on `main` at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`, with extensive pre-existing changes and untracked `financial-workspace/` and `specs/` trees.

## Basis

This inventory records evidence used for the Google Drive model. Repository paths refer to the outer workspace on `main` at `dcc72d596aac78bc90b5e45e6e89ba94be6baeef`, inspected 2026-09-23 with extensive pre-existing changes and untracked `financial-workspace/` and `specs/` trees.

| Evidence | Supports |
| --- | --- |
| `financial-workspace/config/cashflow/sources.yaml` | Thirty namespaced/native IDs, locators, metadata, coverage basis, hashes, cache paths, and verification flags |
| `financial-workspace/config/cashflow/drive_inventory.json` | Workspace folder ID and read-only metadata observed 2026-09-14 |
| 2024, 2025, and 2026 statement manifests | Legacy local-to-Drive ID associations; older manifests also pin sizes and SHA-256 |
| `financial-workspace/src/cashflow/sources.py` and tests | Catalog construction, coverage inference, hashes, duplicate rejection, and local/cache checks |
| `financial-workspace/src/cashflow/fetch.py` and `tests/cashflow/test_fetch.py` | Read-only rclone discovery/download, exact-ID selection, containment, hash gate, race check, replacement, and failures |
| `financial-workspace/data/cashflow/runs/verification-20260915T091436483129Z/verification.json` | Historical report of 30 successful online byte checks |
| `financial-workspace/docs/cashflow/README.md` and `source-coverage.md` | rclone setup, read-only acquisition behavior, cache semantics, coverage totals, and limitations |
| Integration, cross-system model, cash-flow process, and migration `0001-existing-system.md` | Ownership, consumers, proposed structure, identity handoffs, and migration constraints |
| Git history of `projects/financial-workspace/financial-structure.md` before commit `016f639` | Remote hierarchy verified 2026-09-13, stable folder IDs, filing exceptions, population notes, and target topology restored in `views/folder-topology.md` |

No live external system was inspected. Remote facts are limited to saved, dated inventory and verification artifacts. The repository links to the rclone Drive backend documentation at `https://rclone.org/drive/`; model guarantees rely on checked-in code and artifacts rather than undocumented tool behavior.

## Reading map

- [Structure](structure.md)
- [Schema](schema.md)
- [Rules](rules.md)
