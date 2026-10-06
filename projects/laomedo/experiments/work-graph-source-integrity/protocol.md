---
title: Work Graph source integrity protocol
status: draft
kind: experiment-protocol
owners: [laomedo-maintainers]
last_reviewed: 2026-10-05
applies_to: [laomedo]
supersedes: null
related: []
---

# Protocol

## Question and frozen scope

Can the installed Laomedo Work Graph package preserve stable GitHub issue identity, native blocker provenance, and readiness computed from the complete graph under adversarial source responses? Compare a separate, hand-checked oracle with the installed wheel, not with its own development tests. Freeze the source revision, wheel SHA-256, connector/schema version and [governing Work Graph contract](../../subsystems/work-graph/contract/work-graph.md) before executing. The initial source baseline is Laomedo `0ead228a0adea44afd0467dea4acec93177af0b9` and specs `7f6760e22cbdd0128e608a6591a1c94bdfd685bf`; the exact protocol and wheel revisions must be recorded in the attempt.

## Independent corpus and oracle

Use a new EXP-01 fixture corpus, independent of `examples/work-graph/github-pages.json` and `tests/test_work_graph.py`. Each named case provides captured-shape GraphQL response pages, a separately written expectation for item identities, source markers, edge endpoints and native provenance, completeness/warnings, readiness, and filtered projection. Include:

1. Two-page import with a closed prerequisite and an open dependent; compare page order, issue ID versus number, and deduplication of the same native edge reported from both endpoints.
2. Cross-repository and inaccessible blocker references; retain endpoint repository/URL and unknown readiness. A textual `#blocks` reference must create no dependency.
3. Truncated blocker and label connections, null issue/dependency nodes, interrupted later page, and inaccessible repository. Missing source evidence must never become ready.
4. Two-node cycle, self-loop, and an open dependent downstream of the cycle; distinguish cyclic membership from blocked downstream work.
5. A refresh that changes source update marker/state; both immutable snapshot artifacts must remain readable with different digests.
6. Open/closed and label filters with a matching isolated item and a hidden prerequisite. Projection may omit context but must retain readiness computed from the complete graph.

Use fixed UTC fetch times and synthetic issue bodies only. Preserve fixture response bytes and a digest for each case. The oracle is written before execution and contains expected values, not values copied from Laomedo output. Run the corpus via an installed wheel in a disposable environment outside Git and compare actual output to the frozen oracle. Record any rejected case, exception class and conservative readiness separately rather than silently changing a fixture or oracle to make a pass.

## Pass, failure and limits

Pass only if every reachable fixture meets its hand-checked expected identity, edge, completeness, readiness and projection values; refresh keeps both artifacts; tampering is rejected; and an incomplete or inaccessible source never makes an open item ready. A mismatch, source data lost without an explicit refusal, or readiness promoted by filtering is a **no-go** for the corresponding Work Graph claim. A rejected malformed source is acceptable only when the oracle explicitly expects refusal. Preserve source hashes, wheel hash, installed package version, exact command/check results and any negative observations in a dated evidence manifest.

This is a credential-free, zero-model, zero-GitHub-write test. Do not query a live repository without separately approving its exact repository and read scope; the fixture corpus can complete this protocol without that optional observation. Do not run EXP-16/17, alter GitHub issues, add UI, or infer launch authorization from source readiness.
