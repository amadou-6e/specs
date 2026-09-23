"""Checks semantic links in the Financial Workspace replacement model."""
import json
from pathlib import Path

def validate(root, errors, parse):
    base = root / "projects/financial-workspace/exp-model"
    if not base.exists():
        return
    def error(p, msg):
        errors.append(str(p.relative_to(root)) + ": " + msg)
    def read(p):
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            error(p, "invalid structured contract: " + str(exc))
            return {}
    graph = read(base / "relationships/graph.yaml")
    objects = {o["id"]: o for o in graph.get("objects", [])}
    schemas = {}
    for p in base.rglob("metadata.yaml"):
        data = parse(p, errors)
        if not data:
            continue
        for k,v in data.items():
            if k.endswith("_ref") and isinstance(v, str):
                if not (p.parent / v).is_file():
                    error(p, "unresolved " + k + ": " + v)
            if k in {"representations", "evidence_forms", "mapping_refs"}:
                if not isinstance(v, list):
                    error(p, k + " must be a list")
                    continue
                for link in v:
                    target = p.parent / link
                    if not target.exists():
                        error(p, "unresolved " + k + ": " + link)
                    elif k != "mapping_refs" and target.parent.resolve() != (base/"representations").resolve():
                        error(p, "representation must resolve into representation catalogue")
        if ".template" in p.parts:
            continue
        if p.parent.parent == base / "objects":
            mandatory = {"purpose","includes","excludes","identity_field","schema_ref","graph_ref","relationship_ids","representations","evidence_forms","provenance_ref","mapping_refs","maturity"}
            missing = mandatory-data.keys()
            if missing:
                error(p, "missing object characteristics " + str(sorted(missing)))
            oid=p.parent.name
            schema=read(p.parent/"schema.yaml")
            schemas[oid]=schema
            fields=schema.get("fields",{})
            if not fields:
                error(p,"schema requires typed fields")
            for name,f in fields.items():
                if not {"type","required","nullable"} <= f.keys():
                    error(p,"incomplete field "+name)
                if f.get("required") and f.get("nullable"):
                    error(p,"required field cannot be nullable: "+name)
            identity=data.get("identity_field")
            if identity not in fields or identity != schema.get("identity_field") or identity != objects.get(oid,{}).get("identity"):
                error(p,"identity mismatch")
            expected={r["id"] for r in graph.get("relationships",[]) if oid in (r["source"],r["target"])}
            if set(data.get("relationship_ids",[])) != expected:
                error(p,"relationship_ids differ from canonical graph")
        if p.parent.parent == base/"representations":
            for k in ("media_types","variants","locator_types","provenance_ref","maturity"):
                if k not in data: error(p,"missing representation characteristic "+k)
    for r in graph.get("relationships",[]):
        if r["source"] not in objects or r["target"] not in objects:
            error(base/"relationships/graph.yaml","unknown edge endpoint")
    mapping=read(base/"mappings/cashflow/mapping.yaml")
    fields=schemas.get("cashflow-entry",{}).get("fields",{})
    rows=mapping.get("fields",[])
    if len({r["target_field"] for r in rows})!=len(rows):
        error(base/"mappings/cashflow/mapping.yaml","duplicate target fields")
    if {r["target_field"] for r in rows}!=set(fields):
        error(base/"mappings/cashflow/mapping.yaml","projection must cover every cashflow-entry field")
    for r in rows:
        if r.get("source"):
            oid,field=r["source"].split(".",1)
            if field not in schemas.get(oid,{}).get("fields",{}):
                error(base/"mappings/cashflow/mapping.yaml","unknown source field "+r["source"])
        elif not r.get("derivation"):
            error(base/"mappings/cashflow/mapping.yaml","missing derivation")
