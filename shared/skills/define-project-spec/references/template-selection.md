# Choose and adapt category templates

Read the target project's SPECS.md first. The
[Theseo guide](../../../../projects/theseo-anysearch/SPECS.md) is a worked
instance, not a universal requirement to create nine categories. Its templates
demonstrate ownership and entry cardinalities; its Python/Rust/Ray/RLlib partitions
are specific to Theseo.

| Purpose | Structural type | Reference and important boundary |
| --- | --- | --- |
| System relationships | Fixed | [Architecture](../../../../projects/theseo-anysearch/architecture/template.md); spans subsystem owners rather than duplicating contracts |
| Stable behavior | Folder collection | [Subsystem](../../../../projects/theseo-anysearch/subsystems/template/README.md); overview, contract, design and validation, with optional guides/interfaces |
| Investigation | Folder collection | [Research](../../../../projects/theseo-anysearch/research/template/README.md); method, characterized sources, findings and synthesis |
| Bounded empirical test | Folder collection | [Experiment](../../../../projects/theseo-anysearch/experiments/template/README.md); protocol and sources precede iterations, execution, evidence and results |
| Durable choice | Document collection | [Decision](../../../../projects/theseo-anysearch/decisions/template.md); rationale, alternatives and migration consequences |
| Contributor conventions | Fixed | [Implementation](../../../../projects/theseo-anysearch/implementation/README.md); explicitly declared partitions, no arbitrary copyable partition template |
| Primary UI surface | Folder collection | [UI design](../../../../projects/theseo-anysearch/ui-design/template/README.md); adapt to the project's view-owned paths and Draw.io authority |
| Durable defect knowledge | Document collection | [Bug](../../../../projects/theseo-anysearch/bugs/template.md); GitHub retains current work status |
| Historical evidence | Document collection | [Legacy](../../../../projects/theseo-anysearch/legacy/template.md); active migration instructions stay with the current owner |

The three types control expansion, not authority or lifecycle. A folder collection
has one directly copyable `template/`; a document collection has `template.md`.
Fixed categories can contain declared documents or partitions, but contributors
cannot create arbitrary top-level partitions. Each organizing container documents
its children with `1`, `0..1` and `0..*`. Every real entry has project-valid
frontmatter; a template keeps the sentinel `template` status.

For an interactive session, review one populated example before scaffolding its
category. Ask who owns its behavior, which parts apply to the project, and which
checks would verify it. Remove inherited implementation choices unless supported
by the project. Copy the entry directly under its category, not beneath another
template layer. Keep example data visibly illustrative.

When several documents describe the same feature, place observable behavior in
its subsystem contract, cross-owner relationships in architecture, the choice's
rationale in a decision, exploratory evidence in research/experiments and source
organization in implementation. A view links to its behavioral owner. A directory
named after a provider can be an implementation partition or extension rather than
a subsystem; determine its responsibility before choosing its location.
