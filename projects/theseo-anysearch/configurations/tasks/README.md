# Task configuration boundary

Status: draft. Parent: [configuration architecture](../overview.md).

## Fixed task catalogs

A user-authored routing task defines its objective and searchable classification:

- readable task ID;
- task type;
- start plus either one goal or ordered waypoints;
- family;
- zero or more labels.
- physical task constraints such as the body radius for which clearance is required.

It does not configure the environment action space or agent body and does not require
the user to author provenance, derivation explanations, world hashes, or content hashes.

The catalog may be inline or stored in a task YAML. Both forms use the same schema.

## Generated tasks

A task generator defines how concrete episode objectives are sampled from the active
geometry and accepted. It may own endpoint regions, distance constraints, attempt and
planner budgets, reachability requirements, recovery margin, and difficulty bands.

Every accepted generated task is materialized in runtime evidence with its resolved
coordinates, bound world identity, generated task identity, and verification result.

## World-bundled tasks

A verified world may expose a catalog of imported or derived tasks. The experiment may
import that catalog from a named geometry-source index. Importing does not select one
task or assign an experimental role.

## Phase-specific use

Training, validation, and evaluation select eligible tasks by IDs, families, or labels.
They separately define consumption behavior:

- training commonly samples eligible tasks;
- validation commonly enumerates or deterministically samples a stable set;
- final evaluation commonly executes every selected task for a fixed number of seeds or
  repetitions.

The same world may legally and technically provide different tasks to different phases.
The run manifest reports overlap; the user chooses the intended generalization design.

## Verification boundary

Generated verification evidence records the body and movement assumptions under which
a task/reference route was checked. A task's declared physical constraints are checked
against the configured agent; they do not resize it. If verification assumptions are
incompatible with the configured agent or action space, loading fails or produces an
explicit reviewed compatibility decision. Imported task metadata never silently changes
runtime settings.
