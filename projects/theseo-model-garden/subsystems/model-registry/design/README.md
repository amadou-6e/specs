# Model-registry design

This page explains how the local registry realizes its limited publication and
loading contract, including which state is authoritative and where failures can leave
that state inconsistent.

## Components and data flow

```text
trained model + GardenConfig
            |
            v
      GardenStore.save
       |            |
       v            v
 package directory  ~/.anysearch/garden_registry.yaml
       |            |
       +------ resolve_ref ------+
                                  v
                        RLlib encoder loader
```

The package directory is the model payload. The global YAML registry is only a local
alias index. A path can be consumed without being registered, while a registry entry
can become stale if its directory is moved or deleted.

## State ownership

`GardenStore` owns package files beneath the root supplied to its constructor. Module
helpers own two user-home registries. Import-time preset discovery may update the
model registry, and the CLI may update it after training. No single manifest is an
authoritative inventory of all packages because explicit paths and store-local models
need not appear in the global file.

## Publication sequence and failure boundary

Publication creates the destination, serializes full-model and encoder state, writes
metadata and loss history, then rewrites the alias registry. These operations are not
staged or committed atomically. A failure can therefore leave a partial directory;
conversely, a registry-write failure can leave a complete but undiscoverable package.
Repeated publication to the same alias mutates the release in place.

## Loading boundary

Checkpoint deserialization uses PyTorch's `weights_only=True`, reducing the object
surface compared with loading an arbitrary pickled model. The surrounding JSON and
YAML remain trusted local files without checksum verification. Consumer architecture
construction happens in Anysearch's CNN model rather than in the registry, coupling
the current package metadata to `VoxelEncoder3D`.

## Trade-offs

The design is intentionally small: human-readable registries, ordinary directories,
and direct Python calls make local experimentation easy and require no service. The
same simplicity prevents reproducible distribution: alias mutation, import side
effects, missing locks, and the absence of content identity make it unsuitable as an
immutable multi-process or cross-machine registry without further work.

## Historical and proposed design

The [monolithic design record](../../../architecture/model-garden-monolith.md) and
[certification plan](../contract/certification.md) describe broader ambitions. They
are design and research inputs, not evidence that integrity, compatibility, or
promotion enforcement exists in the current registry.
