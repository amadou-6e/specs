# Object template

<!-- BEGIN GENERATED: contained-elements -->
## Contained elements

```text
.template/
├── 1 README.md
├── 1 schema.yaml
├── 1 relationships.md
└── 1 representations.md
```
<!-- END GENERATED: contained-elements -->
Define one identifiable object: meaning and boundary, stable identity, fields, graph edges and source forms. Use common nouns. Register edges in the canonical graph. Source examples require verified native references; originals remain outside the spec.

## Required semantic metadata

Object metadata must declare purpose, includes, excludes, identity_field, schema_ref, graph_ref, relationship_ids, representations, evidence_forms, provenance_ref, mapping_refs and maturity. Direct representations and supporting evidence are distinct. Empty association lists must be explicit. Schema files use readable YAML. Put the single identity field under primary_key, every ref/ref[] field under foreign_keys, and all remaining attributes under fields. Every field requires type, requiredness and null policy; the schema owns these definitions and constraints.
