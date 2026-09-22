---
title: Custom encoder extension contract
status: draft
kind: subsystem-extension-contract
owners: [theseo-team]
last_reviewed: 2026-09-22
applies_to: [theseo-model-garden]
related: [README.md]
---

# Custom encoder extension contract

This page defines the current dynamic-import boundary for third-party model classes.
It describes what the loader enforces separately from what downstream training code
merely assumes.

## Discovery and trust boundary

Set `architecture: custom` and provide `custom_encoder.class` as a fully qualified
`module.ClassName`. `CustomEncoderConfig.instantiate()` imports the module with
`importlib.import_module`, resolves the named attribute, and calls it with the
configured `kwargs`.

This executes trusted local Python code with the process's privileges. There is no
sandbox, allowlist, signature verification, or package isolation.

## Enforced interface

The loader enforces only that the class path contains a module and attribute name and
that the resolved object can be called with the supplied keyword arguments. It does
not require `torch.nn.Module`, inspect a forward signature, run a sample tensor, or
check latent dimensions.

Downstream pretraining generally assumes an `nn.Module` with a compatible `.loss()`
or forward behavior, depending on the trainer path. Because `build_model()` returns
the custom object directly, a custom encoder is currently a custom *full training
model*, not merely a latent encoder automatically wrapped by a built-in objective.

## Failure semantics

Import errors, missing attributes, constructor errors, tensor mismatches, and missing
training methods propagate from Python, PyTorch, or the trainer. They are not
normalized into an extension-specific error type.

## Conformance gap

There is no automated custom-extension conformance suite. Before treating this as a
stable external extension API, the project needs an explicit protocol, a construction
and forward smoke test, objective-specific requirements, and tests for malformed or
incompatible providers.
