# Laomedo specification authoring system

Apply the [shared typed-folder convention](../../shared/conventions/typed_folder_system/README.md).
Agent authoring check, user critique pending: 2026-10-01; inspected specs revision 2854612a32a40b6b455734cd2d758f92f86f1897.
This migration reviews local documents, not freshly executed implementation or upstream APIs.

## Closed taxonomy

| Category | Type | Canonical responsibility |
| --- | --- | --- |
| architecture | fixed | Shared records, edges, target relationships, historical component proposal |
| decisions | document collection | Reconstructed discussion trails, durable product choices, alternatives and open questions |
| subsystems | folder collection | Execution/isolation, skill registry/drafts, raw traces/projection |
| experiments | folder collection | Bounded protocol, attempts, evidence manifests, results |
| research | folder collection | Characterized sources, atomic findings and exploratory synthesis |
| implementation | fixed | Contributor workflow and migration documentation |
| deprecated | fixed | Existing historical UI workshop and unchanged reference assets |
| components, feasibility, monitoring, sandboxing | fixed compatibility containers | Closed sets of pointers preserving published paths; no new authoring or behavioral ownership |

The seven authoring categories above remain the content taxonomy. The four
compatibility containers are declared in `spec.json` for structural validation,
with `superseded` pointer entries only. They have no templates and are not
destinations for new work. See the [published-reference audit](implementation/spec-migration.md#published-reference-audit)
before proposing removal of any pointer.

Change the category set only by reviewing SPECS.md and spec.json together. Both providers
share execution/session ownership. Revision and draft share immutable skill identity and
promotion separation. Traces have independent storage/projection ownership. The decisions
collection records user-confirmed choices and reconstructed discussion trails, with draft
status until reviewed; it does not make unverified mechanisms accepted. No bugs or live
UI-design collection is instantiated because the sources do not yet contain durable defect
records or reviewed Laomedo surfaces.

## Copy-and-rename workflow

Copy [subsystem](subsystems/template/README.md), [experiment](experiments/template/README.md)
or [research](research/template/README.md) directly to a kebab-case peer, or copy
[decision](decisions/template.md) to the next numbered Markdown entry. For example,
copy experiments/template/ to experiments/snapshot-rejection/, replace identity, example
facts and links, and replace status: template in every copied entry page before indexing it.
Do not nest another template directory. Required files are declared in spec.json; internal
schema/cardinalities are in template READMEs. Fixed categories have no folder-copy mechanism.

A contract owns observable behavior; design explains mechanisms; validation links dated
evidence and gaps. Shared records stay in architecture. Other pages link canonical owners.
Concrete subsystem pages are draft target requirements, even where a narrower pilot exists.

## Metadata and evidence lifecycle

Entry fields: title, status, kind, owners, last_reviewed, applies_to, supersedes, related.
Maintainers is a role, not a newly assigned individual. last_reviewed records the agent
content check in this trial; user acceptance remains pending. Statuses: draft, active, complete,
deprecated, superseded; templates use template. Lifecycle is independent of implementation
maturity, experiment go/no-go or issue state. Complete research/pilot records mean recording
is complete, not product acceptance. Related/supersedes use declared entry identities if set.

Freeze prospective protocols before tests. Reconstructed protocols must be retrospective;
unavailable timestamps, hardware, controls and replication remain unknown. Separate attempts
and results from artifact manifests. Record producer, revision/hash, location and access/
retention limitations. Keep raw private transcripts, sessions and credentials outside Git.
Never overwrite older versions, budgets or negative findings with newer pilot evidence.

## Each implementation PR

Follow [spec impact](implementation/spec-impact.md). Select update, existing coverage or
no impact with exact contract sections/revisions and separate evidence. Behavior, interfaces,
defaults, persistence/identity, permissions and failure semantics require current coverage.
Affected specs must merge to specs main before dependent implementation merges; pin the
merged specs commit. Branch evidence may be reviewed in parallel but is not a merged contract.
An open issue or research recommendation is not implementation authorization.

## Review and validation

Inspect contract-to-validation-to-evidence paths for duplicate authority, lost negative
findings, misleading lifecycle, copied template facts and unsupported claims. Run
python tools/validate_specs.py from the specs root and git diff --check. The existing
validator checks declared shapes, entry metadata, related identities and relative file links.
It does not check anchors, nested attempt metadata, closed taxonomy, semantic sufficiency,
chronological truth or PR merge status. Review those manually.

This is authored policy and project manifest opt-in, not activated CI or branch protection.
No repository workflow, agent configuration or GitHub issue changes occur in the trial.
See [migration mapping](implementation/spec-migration.md) for preserved historical owners.
