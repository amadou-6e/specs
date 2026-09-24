"""Checks semantic links in the Financial Workspace replacement model."""
import json
import re
from pathlib import Path

from schema_yaml import load_schema

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
    schema_groups = {}
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
            schema_path=p.parent/"schema.yaml"
            try:
                schema=load_schema(schema_path)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                error(schema_path,"invalid YAML object schema: "+str(exc))
                schema={}
            groups={key:schema.get(key) for key in ("primary_key","foreign_keys","fields")}
            if any(not isinstance(value,dict) for value in groups.values()):
                error(schema_path,"primary_key, foreign_keys and fields must be mappings")
                groups={key:value if isinstance(value,dict) else {} for key,value in groups.items()}
            primary=groups["primary_key"]
            foreign=groups["foreign_keys"]
            other=groups["fields"]
            field_names=[name for group in groups.values() for name in group]
            if len(field_names)!=len(set(field_names)):
                error(schema_path,"key groups overlap")
            fields={**primary,**foreign,**other}
            schema_groups[oid]=groups
            schemas[oid]={**schema,"fields":fields}
            if not fields:
                error(schema_path,"schema requires typed fields")
            identity=data.get("identity_field")
            if len(primary)!=1 or identity not in primary or identity != schema.get("identity_field") or identity != objects.get(oid,{}).get("identity"):
                error(schema_path,"primary key or identity mismatch")
            for name,f in fields.items():
                if not isinstance(f,dict) or not {"type","required","nullable"} <= f.keys():
                    error(schema_path,"incomplete field "+name)
                    continue
                if f.get("required") and f.get("nullable"):
                    error(schema_path,"required field cannot be nullable: "+name)
                if name in foreign and (f.get("type") not in {"ref","ref[]"} or not f.get("target")):
                    error(schema_path,"foreign key must be typed ref/ref[] with target: "+name)
                if name not in foreign and f.get("type") in {"ref","ref[]"}:
                    error(schema_path,"reference field must be in foreign_keys: "+name)
            expected={r["id"] for r in graph.get("relationships",[]) if oid in (r["source"],r["target"])}
            if set(data.get("relationship_ids",[])) != expected:
                error(p,"relationship_ids differ from canonical graph")
        if p.parent.parent == base/"representations":
            for k in ("media_types","variants","locator_types","provenance_ref","maturity"):
                if k not in data: error(p,"missing representation characteristic "+k)
    for r in graph.get("relationships",[]):
        if r["source"] not in objects or r["target"] not in objects:
            error(base/"relationships/graph.yaml","unknown edge endpoint")
    catalogue_path=base/"objects/field_catalogue.yml"
    catalogue={}
    current_object=None
    current_group=None
    in_objects=False
    try:
        for line in catalogue_path.read_text(encoding="utf-8").splitlines():
            if line == "objects:":
                in_objects=True
                continue
            if not in_objects:
                continue
            object_match=re.fullmatch(r"  ([a-z][a-z0-9-]*):",line)
            group_match=re.fullmatch(r"    (primary_key|foreign_keys|fields):(?: {})?",line)
            field_match=re.fullmatch(r'      ([a-z][a-z0-9_]*): (".*")',line)
            if object_match:
                current_object=object_match.group(1)
                if current_object in catalogue:
                    error(catalogue_path,"duplicate object "+current_object)
                catalogue[current_object]={key:set() for key in ("primary_key","foreign_keys","fields")}
                current_group=None
            elif group_match and current_object:
                current_group=group_match.group(1)
            elif field_match and current_object and current_group:
                name=field_match.group(1)
                description=json.loads(field_match.group(2))
                if not description:
                    error(catalogue_path,"empty description "+current_object+"."+name)
                if name in catalogue[current_object][current_group]:
                    error(catalogue_path,"duplicate field "+current_object+"."+name)
                catalogue[current_object][current_group].add(name)
    except (OSError, ValueError) as exc:
        error(catalogue_path,"invalid field catalogue: "+str(exc))
    if set(catalogue)!=set(schema_groups):
        error(catalogue_path,"catalogue objects differ from object schemas")
    for oid,groups in schema_groups.items():
        for key in ("primary_key","foreign_keys","fields"):
            if catalogue.get(oid,{}).get(key,set())!=set(groups[key]):
                error(catalogue_path,oid+"."+key+" differs from schema")
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
