# Generate and attach a verified world

This guide takes a world provider from discovery to an experiment that can load its generated world. A provider converts or generates geometry and routing tasks; `worlds add` attaches an accepted result to an existing training or tuning experiment. Neither command trains a model. The commands below describe `theseo-anysearch` revision `72a413a`; paths and provider options are examples to replace with your own. The command implementation is `theseo_anysearch/cli/commands/worlds.py`, and the same flow is described in `docs/world_providers.md` in that repository.

Before starting, install Theseo and, if you need more than the built-in `fixture-boxes` provider, install the provider's optional distribution and satisfy its source-data rights and dependencies. Have a training or tuning experiment YAML ready if you intend to attach the result. Choose a **new** output directory: generation refuses one that already exists. A successful run leaves a verified bundle with routing sidecars, previews, and `verification.json`; attachment updates the experiment YAML but does not launch it.

## 1. Discover a provider

```console
anysearch worlds list
```

The output lists the built-in and installed providers, their declared parameters, unavailable-provider diagnostics, and locally registered worlds with a fresh `verified` or `missing-or-changed` check. `anysearch worlds list --remote` shows catalog **metadata** only; it neither installs nor authorizes a provider. Inspect a provider's declared parameters before invoking it. Optional plugins are executable Python code imported during discovery, so install only distributions you trust (`theseo_anysearch/world_providers/api.py`).

## 2. Generate and inspect a bundle

The built-in fixture needs only the common options:

```console
anysearch worlds fixture-boxes --seed 1 --output generated-world
```

Other providers may require their own declared flags, for example `anysearch worlds <provider> --seed <integer> --output <new-directory> <provider-options>`. Those angle-bracket values are placeholders, not literal shell syntax. The CLI validates declared options, asks the provider to write occupancy and routing sidecars, independently checks the result, renders six previews, and then writes the verification report and local-registry entry (`theseo_anysearch/world_providers/service.py`, `theseo_anysearch/world_providers/bundle.py`, `theseo_anysearch/world_providers/render.py`).

Inspect `generated-world/verification.json`, `generated-world/previews/`, its task and reference sidecars, and the provider's reported limitations before using it. Verification checks the recorded rights and voxel-route clearance; it does not prove that a physical controller can execute a route or that a benchmark task label is correct. See the [contract](../contract/README.md) for the exact admission boundary.

If generation fails, the output directory may be partial because the provider writes directly to the final path. It will not be registered as verified, but retrying at the same path is refused. Inspect that directory and select a new output path; do not treat the presence of files alone as admission.

## 3. Attach to an existing experiment

```console
anysearch worlds add generated-world --config path/to/experiment.yaml
```

Review the printed YAML diff and selected task identity. At this revision, attachment accepts a verified **`train`** member only, picks the lexicographically first task identity, and rejects conflicting geometry, waypoint, or same-study assignments (`theseo_anysearch/world_providers/selection.py`). It does not provide a task picker, attach non-training roles, or launch a run. The experiment loader later revalidates the bundle, runtime pack, waypoints, rights, and study assignment (`theseo_anysearch/experiments/loader.py`). Editing a verified bundle after attachment can therefore make experiment loading fail.

The proposed separation of main experiment YAML, geometry-generation YAML, and task files is future design work, not a configuration feature of these commands.
