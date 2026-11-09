---
title: Authoring a new Google-backed provider
status: draft
kind: specification
owners: [laomedo-maintainers]
applies_to: [laomedo]
---

# User story: implement a provider and run it

As an engineer adding a Google-backed agent, I want to implement the declared
provider behavior, supply explicit configuration and run it through Laomedo,
without copying workspace management, Docker cleanup or durable journal logic.

Google-backed is the hypothetical provider in this story. No particular Google
SDK, ACP support or container topology is assumed. This document records the
current experience and proposed acceptance criteria; it does not implement Google
support, dynamic registration or the pending provider refactor.

## First contact: where do I import the contracts?

```python
from laomedo.agents.agents.base import BaseAgent, BaseAgentRunner, BaseAgentRuntime
```

All target contracts are exported by that package's __init__.py. Their defining
files are adjacent concern modules, not a second base/ package. The values remain
in base/models/. Concrete Docker delegation is in base/docker.py. Public exports
refer to the original defining classes, not duplicate definitions or renamed copies.

interim.py is an internal live-migration boundary. A new provider author should
not discover two public BaseAgentRuntime choices with identical names. The old
providers still use those internal contracts until behavior is migrated.

## What would I experience with the implementation today?

| What I implemented or attempted | Actual current experience | Reason |
| --- | --- | --- |
| I subclass BaseAgent and implement only native prompting | Python refuses instantiation if required abstract members remain | BaseAgent still requires provider, runtime_binding, recover_interrupted, preflight, resume and _execute |
| I implement all BaseAgent abstract members | Instantiation is possible with valid host paths/state, but this does not establish a fully wired provider | Catalogue and credential composition also use catalog_type/credential_type, which are not abstract members; other host dependencies are explicit |
| I call model_catalog without that composition | The inherited property accesses missing catalog_type instead of constructing a shared default | It currently composes a provider-owned catalogue from a class attribute |
| I implement BaseAgentRunner's two methods | I can instantiate my execution component | It is a target contract; no host auto-registers it or supplies a run just because it exists |
| I call that runner's run | I must supply InvocationRequest, BaseInvocationJournal and StopContext | Host admission, durable writes and cancellation control are collaborators, not produced by the abstract runner |
| I implement only runtime policy hooks | BaseAgentRuntime is still abstract | Shared orchestration is not implemented in that base yet; public lifecycle methods are abstract as well |
| I ask the normal host registry for google | It rejects unregistered_agent_provider before provider construction | AgentProviderRegistry explicitly admits codex, claude and opencode only |
| I run a Python file that just declares my class | No agent task, HTTP service or graph integration starts automatically | Class declaration is not a launcher; existing host composition is separate |

The catalogue missing-attribute case is traced from current source, not a claim
that a live Google provider was launched. Constructor success also requires the
existing workspace/state/skill-store checks and may perform interrupted-run
recovery before concrete initialization has finished.

The crucial limitation: the target runner is not yet consumed by the shared Agent
lifecycle. Today _execute/resume/preflight remain provider hooks. Flattening and
exporting interfaces does not supply that missing integration.

## Proposed author journey after the refactor

1. I read one public contract index and see exactly which behavior my provider
   must supply, what shared behavior already exists, and which capabilities are optional.
2. I implement provider-specific protocol behavior and any genuinely needed
   credential/discovery interpretation. I reuse shared workspace, journal, runtime
   mechanics and cancellation coordination rather than writing competing copies.
3. I supply typed host configuration and native credentials through the declared
   admission boundary. No implicit credential discovery or copied login state is
   implied by subclassing.
4. I explicitly register/select the provider through trusted host composition.
   Graph input cannot import arbitrary Python classes or choose executable paths.
5. I launch the normal host and submit a task. Configuration/capability errors are
   reported before dispatch, rather than surfacing later as missing attributes.
6. I can observe model discovery/readiness, start a fresh execution, inspect its
   status and output, and request cancellation. Resume and optional features have
   explicit native support/error semantics, never fake success or Fresh fallback.
7. On failures or cancellation, shared machinery retains truthful records and
   performs exact owned-resource cleanup. I debug my provider policy/protocol,
   not a second copy of generic infrastructure.

## What does "I implemented the base class, nothing else" mean?

If it means only writing a subclass, with no configuration, credentials, host
selection or task request, there is nothing to execute. Those inputs cannot be
invented safely by the framework.

If it means implementing all required provider behavior and reusing stock shared
infrastructure, that is the intended architectural goal. The current code does
not yet meet it. A single provider class is not presently a sufficient public
integration point, and implementing one abstract role is not equivalent to
implementing the entire provider.

How many provider-specific objects are actually required must follow their real
responsibilities. This story does not authorize adding mandatory catalogue,
credential, transport or runtime classes solely for symmetry. Whether one adapter
can compose stock implementations for a Google-backed provider remains a concrete
design decision to resolve before claiming a minimal authoring API is complete.

## Observable acceptance criteria for that future journey

- [x] The developer sees one canonical public contract per target role and imports
  it from the base package; internal migration classes are not competing exports.
- [ ] Required provider configuration/collaborators are declared and checked before
  dispatch; no hidden catalog_type/credential_type assumptions leak as AttributeError.
- [ ] Shared Agent execution invokes the provider's BaseAgentRunner contract for
  Fresh/Resume with host-owned journal and stop control; no concrete-type branching.
- [ ] Native resource policy plugs into shared runtime behavior without the provider
  reimplementing generic launch, rollback, creator-thread or cleanup-cache algorithms.
- [ ] Trusted host registration and actual graph/HTTP capability integration are
  documented and exercised; no automatic dynamic plugin loading is assumed.
- [ ] The developer can follow one real example through construction, host launch,
  a request, results, cancellation and failure handling, with the exact supported
  provider-specific differences stated.
- [ ] Real-provider acceptance is recorded separately from structural/double-based
  checks; credentials and model turns require the existing explicit authorization.

Checkboxes record observed implementation, not independent review or owner acceptance.
Only the flattened public export/layout part is implemented by this checkpoint.
The rest remains the #277 migration/design scope, not a new feature silently
implemented while moving modules. Review of this story is pending.

## Source map

Implementation observations were traced from BaseAgent in agent.py,
BaseAgentRunner in invocation.py, BaseAgentRuntime in runtime.py and
AgentProviderRegistry in agents/registry.py. These current-source observations
are separate from the proposed journey. See [provider roles](provider-roles.md)
for the governing ownership and lifecycle constraints.
