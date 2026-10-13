---
title: Discover and select skills from a linked source
status: draft
kind: specification
owners: [laomedo-maintainers]
last_reviewed: 2026-10-13
applies_to: [laomedo]
supersedes: null
related: []
---

# Discover and select skills from a linked source

Tracking: [specs #372](https://github.com/amadou-6e/specs/issues/372) and
[Laomedo #157](https://github.com/amadou-6e/laomedo/issues/157). This specifies the
linked-source selector implementation; activating its host service is separately
gated. Source-empty saved nodes retain manual exact references. The existing
[node contract](../contract/langflow-node.md) and [file inspection](skill-files.md)
retain the immutable descriptor boundary.

The [editable interaction model](skill-source-selection.drawio) owns the controls
and transitions. This page specifies their data and discovery behavior.

## Owner-selected controls

| ID | Control and behavior |
| --- | --- |
| SS01 | Source accepts either a repository URL or a local folder link/path. Discover on source change and expose refresh on the searchable dropdowns, with status and fixed errors. Repository URLs and local paths remain visible as the source. |
| SS02 | Skill is a searchable dropdown listing discovered skills from that source. Typing narrows the list; selection chooses a discovered skill rather than accepting an invented ID. |
| SS03 | Revision uses the same searchable dropdown interaction, scoped to the selected skill. Typing filters discovered revisions rather than accepting an unverified free-text revision. |
| SS04 | Changing Source clears the previous skill/revision and ignores obsolete discovery responses. Changing Skill clears the previous revision. Never display an old result as belonging to a new selection. |
| SS05 | Loading, empty source, no filter matches and unavailable source/revision are distinct visible states. Empty or failed discovery offers no implicit executable fallback. |
| SS06 | Once resolved, Skill files opens exactly the selected immutable bundle. Refreshing available choices must not silently change an existing selected revision or an active run. |

## Resolution and compatibility

Discover skills by their SKILL.md entry point. Display a human-readable name and
relative folder so same-named skills in different locations can be distinguished.
Keep an unambiguous source-scoped identity behind the display label. Discovery
reads files and metadata; it never executes skill scripts or invokes an agent.

Revision choices may have useful source labels when available, but each accepted
selection must resolve to concrete source bytes and the content-addressed bundle
identity. A Git commit identifies a repository snapshot; the skill revision is
the hash of that skill's bundle. Do not present them as interchangeable hashes.
The output remains the existing skill_id/revision_id/tree_hash descriptor, verified
and materialized in the runner's registry before dispatch. No repository login,
local path or credential is forwarded as the skill reference.

Existing flows containing exact registry references remain loadable. Selecting a
new source uses the discovery controls; compatibility must not silently substitute
another skill or revision. Registry import/promotion must preserve immutable old
revisions. Unknown existence is not successful discovery.

## Source access boundary

A local link identifies a host-side source. Do not assume that a Windows path is
readable inside the Langflow container. The implementation must resolve it through
the trusted local controller or an explicitly configured read-only source mount.
Do not expose the host filesystem generally to either the browser or agent.
Reject links/path escapes and bound traversal, file sizes and network/cache work.

A repository link identifies source content to discover, not permission to run
its hooks, scripts or submodules. Fetch into a bounded controller-owned cache;
resolve the selected repository revision before importing a skill bundle. Use
an existing scoped connection where applicable, without reading or exporting
personal login files. Missing access is a visible discovery error.

## Bounded source policy and API

A standalone authenticated loopback host service owns discovery, the cache and
registry import. The Langflow backend forwards only fixed discover/revisions/resolve
requests using a backend token file. Tokens never appear in node fields or exports.
Reuse the existing local transport connection during activation; no extra human
sign-in is introduced. This token is transport protection, not a same-user boundary.

The initial Git route accepts public HTTPS repository-root URLs on GitHub or GitLab
(two path segments). It lists heads and tags with full commit IDs and bundle hashes;
it does not expose arbitrary historical commit selection. GitLab subgroups and
private-repository authentication are not implemented. A private repository can be
supplied as an already available allowed local checkout. A failed private fetch is
an access failure, never a prompt to reveal credentials. Git runs with no inherited
provider credentials, personal Git settings or credential helpers; redirects,
hooks, submodules and non-HTTPS protocols are disabled. A bare cache is read as
objects without checking out or executing repository content.

Local sources accept absolute paths, file URIs and links to SKILL.md within explicit
configured roots. The registry root is recognized separately. Sources outside those
roots, filesystem links and unsafe paths are refused. Discovery excludes hidden,
.local, virtual-environment and dependency directories. This is bounded source
selection, not general host browsing or a comprehensive secret-content detector.
The trusted single-user resolver does not claim an OS boundary against concurrent
same-user filesystem tampering.

Local revisions are observed UTC timestamp plus bundle hash. Prior imported choices
persist across refresh/restart; old exact references resolve even after source bytes
change. Git choices retain imported snapshots as refs move/disappear. Registry revision labels include recorded source/path/ref/commit provenance plus
the exact SHA-256; old revisions are explicitly marked origin unrecorded. Origin
metadata is kept outside hashed bundles, so same-named imports are distinguishable. Importing another revision of an
existing skill does not advance its latest pointer. A new skill gets the store's
initial pointer. Each accepted output is the existing three-key descriptor.

Limits: 128 skills, 32 repository refs, 4096 discovery entries; 128 files, 512 KiB per
file and 4 MiB per bundle, maximum path depth 17; 64 cached choices per skill/source;
Git operations monitor state/cache against 128 MiB and use a 60-second operation deadline, with 45 seconds per Git
command. Timeout kills the Git process tree. Portable path checks reject traversal,
credential filenames, case collisions and Windows reserved names before staging.
Exceeding a choice bound refuses before importing bundles or committing the new
choice map. Imported history is not automatically evicted. The cache has no
automatic cleanup; after stopping the service an operator can clear only its
state/index while preserving registry bundles and source-origins.json. Saved
display choices must then be rediscovered; exact exported references remain valid.
Refresh prunes deleted remote branches. Proxy environment configuration is not
inherited or supported. Holding the shared runner transport token also permits
source discovery/import in this local service.

POST /v1/skill-sources/discover takes source; revisions takes source and skill;
resolve takes source, skill and revision. Authentication precedes parsing, bodies
are bounded and unexpected keys fail. Fixed failure categories omit raw paths,
Git stderr, URLs and secrets. The frontend clears dependent selections immediately
and refuses stale source/skill/revision responses. Skill files opens a source-linked
selection only when its hidden resolved tuple matches all three current controls.

## Acceptance

Credential-free fixtures must show two skills, two revisions of one skill, folder
name disambiguation, typed filtering in both dropdowns, and exact reference output.
Cover loading, empty/no matches, failed access, changed selections and late stale
responses. Prove arbitrary typed values cannot become accepted references, old
saved flows remain valid, and folder inspection uses the selected bundle. Test
local/container path resolution separately from public-repository acquisition.
No model call is necessary to prove the selector behavior. Live repository access
and active-demo deployment require their concrete connection/configuration scope.

## Recorded credential-free checks (2026-10-13)

The implementation's host suite passed 684 tests with 15 skips before the final
portable-path testcase. The pinned Langflow image passed eleven source tests
(including Linux links) and five native component tests (including refresh keeping
a selected revision). The imported source-only flow passed an Edge browser check
of both searchable selectors, old exact bundle inspection, clearing on skill/source
change, delayed obsolete response refusal and fixed access failure. Its repository
route used a trusted local Git fixture adapter, not live GitHub authentication.
No model turns, provider credentials or publication writes were involved. These
observations are bounded fixture evidence, not an active-demo deployment claim.
