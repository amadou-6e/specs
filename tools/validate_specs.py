#!/usr/bin/env python3
"""Validate repository structure without third-party dependencies."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 100 * 1024 * 1024
WARN_FILE_BYTES = 25 * 1024 * 1024
REQUIRED_MANIFEST_FIELDS = {"name", "slug", "source_repository", "status"}
PROJECT_STATUSES = {"active", "paused", "archived"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*]\((?![a-z]+:|#)([^)]+)\)", re.IGNORECASE)
IGNORED_PARTS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

# --- Typed and named folder hierarchy enforcement (opt-in via spec.json "categories") ---
#
# A project opts in by adding a "categories" object to its spec.json, mapping each
# declared category name to its structural type (see
# shared/conventions/typed_folder_system/README.md). Projects without a "categories"
# key are unaffected by any of the checks below: this is deliberately additive so
# existing, not-yet-migrated projects don't start failing CI over a convention they
# never declared.
#
# Example:
#   "categories": {
#     "architecture": {"type": "fixed"},
#     "decisions": {"type": "document-collection"},
#     "subsystems": {"type": "folder-collection", "entry_files": ["README.md"]}
#   }

REQUIRED_FRONTMATTER_FIELDS = {
    "title", "status", "kind", "owners", "last_reviewed", "applies_to",
}
ALLOWED_STATUSES = {
    "draft", "active", "complete", "deprecated", "superseded", "template",
}
ALLOWED_CATEGORY_TYPES = {"fixed", "document-collection", "folder-collection"}

# <NNNN>-<slug>.md, for document-collection categories that opt into sequential
# numbering (spec.json category entry: {"numbered": true}) — the convention's own
# generic doc calls this "typical", not universal, so an unnumbered category (e.g.
# a plain historical-archive collection) instead only needs a valid kebab-case slug.
NUMBERED_ENTRY_PATTERN = re.compile(r"^\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
SLUG_ENTRY_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
# <slug> for folder-collection entry directory names (never ".template").
FOLDER_ENTRY_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Filenames that are never treated as a spec entry, even inside a declared category
# (README.md is the container; SKILL.md marks an invokable agent skill, not a spec).
NON_ENTRY_FILENAMES = {"README.md", "SKILL.md"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
CONTAINED_ELEMENTS_HEADING = re.compile(
    r"^## Contained elements(?: and relationships)?\s*$", re.MULTILINE
)
CARDINALITY_TOKEN = re.compile(r"\b0\.\.\*|\b0\.\.1\b|(?<!\.)\b1\b")
TREE_CONNECTOR = re.compile(r"(?:├──|└──|\|--|`--)")


def files() -> list[Path]:
    discovered: list[Path] = []
    for directory, names, filenames in os.walk(ROOT):
        names[:] = [name for name in names if name not in IGNORED_PARTS]
        discovered.extend(Path(directory) / filename for filename in filenames)
    return discovered


FOLDER_CONTRACT_FIELDS = {
    "schema_version", "name", "kind", "purpose", "authority", "owner", "children",
}
FOLDER_LIST_FIELDS = {"children", "includes", "excludes", "applies_to", "related"}
OBJECT_DOMAIN_METADATA_FIELDS = {"title", "status", "last_reviewed", "applies_to", "supersedes", "related"}
EXCLUDED_DUMP_FIELDS = {
    "schema_version", "name", "kind", "purpose", "owner", "type_check", "temporary",
}
GENERATED_START = "<!-- BEGIN GENERATED: contained-elements -->"
GENERATED_END = "<!-- END GENERATED: contained-elements -->"
OBJECT_SUMMARY_START = "<!-- BEGIN GENERATED: object-domain-summary -->"
OBJECT_SUMMARY_END = "<!-- END GENERATED: object-domain-summary -->"
CHILD_SPEC = re.compile(r'^(1|0\.\.1|0\.\.\*)\s+(.+)$')


def parse_folder_contract(path: Path, errors: list[str]) -> dict[str, object] | None:
    """Parse the intentionally small metadata.yaml subset: scalars plus a children list."""
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: unreadable folder contract: {exc}")
        return None
    data: dict[str, object] = {}
    index = 0
    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            index += 1
            continue
        if raw[:1].isspace() or ":" not in raw:
            errors.append(f"{path.relative_to(ROOT)}:{index + 1}: invalid metadata.yaml syntax")
            return None
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in FOLDER_LIST_FIELDS:
            children: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index][:1].isspace()):
                item = lines[index].strip()
                if item:
                    if not item.startswith("- "):
                        errors.append(f"{path.relative_to(ROOT)}:{index + 1}: children must be list items")
                        return None
                    children.append(item[2:].strip().strip("'\""))
                index += 1
            data[key] = children
            continue
        data[key] = value.strip("'\"")
        index += 1
    if data.get("type_check") == "exclude":
        missing = EXCLUDED_DUMP_FIELDS - data.keys()
        if missing:
            errors.append(
                f"{path.relative_to(ROOT)}: excluded dump metadata missing {sorted(missing)}"
            )
        if data.get("kind") != "tmp-data-dump" or data.get("temporary") != "true":
            errors.append(
                f"{path.relative_to(ROOT)}: type_check exclusion is permitted only for "
                "kind: tmp-data-dump with temporary: true"
            )
        data["_type_check_excluded"] = True
        return data
    if "type_check" in data and data.get("type_check") != "include":
        errors.append(
            f"{path.relative_to(ROOT)}: type_check must be include or exclude"
        )
    missing = FOLDER_CONTRACT_FIELDS - data.keys()
    if missing:
        errors.append(f"{path.relative_to(ROOT)}: missing folder metadata {sorted(missing)}")
    if data.get("schema_version") != "1":
        errors.append(f"{path.relative_to(ROOT)}: schema_version must be 1")
    children = data.get("children")
    if not isinstance(children, list) or not children:
        errors.append(f"{path.relative_to(ROOT)}: children must be a non-empty list")
    else:
        for child in children:
            if CHILD_SPEC.match(child) is None:
                errors.append(
                    f"{path.relative_to(ROOT)}: child {child!r} must start with 1, 0..1, or 0..*"
                )
    if data.get("kind") == "object-domain":
        missing_domain_fields = OBJECT_DOMAIN_METADATA_FIELDS - data.keys()
        if missing_domain_fields:
            errors.append(
                f"{path.relative_to(ROOT)}: object-domain metadata missing "
                f"{sorted(missing_domain_fields)}"
            )
        for field in ("includes", "excludes", "applies_to"):
            values = data.get(field)
            if not isinstance(values, list) or not values:
                errors.append(
                    f"{path.relative_to(ROOT)}: object-domain metadata requires a non-empty {field} list"
                )
        related = data.get("related")
        if not isinstance(related, list):
            errors.append(
                f"{path.relative_to(ROOT)}: object-domain metadata requires related to be a list"
            )
        status = data.get("status")
        if status not in ALLOWED_STATUSES - {"template"}:
            errors.append(
                f"{path.relative_to(ROOT)}: object-domain status {status!r} is not one of "
                f"{sorted(ALLOWED_STATUSES - {'template'})}"
            )
    return data


def render_contained_elements(folder_name: str, contract: dict[str, object]) -> str:
    children = contract["children"]
    lines = [f"{folder_name}/"]
    for index, child in enumerate(children):
        connector = "└──" if index == len(children) - 1 else "├──"
        lines.append(f"{connector} {child}")
    tree = "\n".join(lines)
    return (
        f"{GENERATED_START}\n"
        "## Contained elements\n\n"
        f"```text\n{tree}\n```\n"
        f"{GENERATED_END}"
    )


def render_object_domain_summary(contract: dict[str, object]) -> str:
    purpose = str(contract["purpose"])
    includes = "\n".join(f"- {item}" for item in contract["includes"])
    excludes = "\n".join(f"- {item}" for item in contract["excludes"])
    return (
        f"{OBJECT_SUMMARY_START}\n"
        f"> {purpose}\n\n"
        "## Domain boundary\n\n"
        "**Includes:**\n\n"
        f"{includes}\n\n"
        "**Excludes:**\n\n"
        f"{excludes}\n"
        f"{OBJECT_SUMMARY_END}"
    )


def sync_object_domain_summary(
    readme: Path, contract: dict[str, object], errors: list[str], *, write: bool
) -> None:
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8-sig")
    generated = render_object_domain_summary(contract)
    if OBJECT_SUMMARY_START in text or OBJECT_SUMMARY_END in text:
        if text.count(OBJECT_SUMMARY_START) != 1 or text.count(OBJECT_SUMMARY_END) != 1:
            errors.append(f"{readme.relative_to(ROOT)}: malformed generated object-domain-summary markers")
            return
        start = text.index(OBJECT_SUMMARY_START)
        end = text.index(OBJECT_SUMMARY_END, start) + len(OBJECT_SUMMARY_END)
        updated = text[:start] + generated + "\n\n" + text[end:].lstrip("\n")
    else:
        h1 = re.search(r"^# [^\n]+$", text, re.MULTILINE)
        if h1 is None:
            errors.append(f"{readme.relative_to(ROOT)}: cannot place generated object-domain summary")
            return
        updated = text[:h1.end()] + "\n\n" + generated + "\n" + text[h1.end():].lstrip("\n")
    if updated != text:
        if write:
            readme.write_text(updated, encoding="utf-8")
        else:
            errors.append(f"{readme.relative_to(ROOT)}: generated object-domain summary is stale")


def sync_contained_elements(
    readme: Path,
    contract: dict[str, object],
    display_name: str,
    errors: list[str],
    *,
    write: bool,
) -> None:
    if not readme.exists():
        errors.append(f"{readme.relative_to(ROOT)}: missing README for folder contract")
        return
    text = readme.read_text(encoding="utf-8-sig")
    generated = render_contained_elements(display_name, contract)
    if GENERATED_START in text or GENERATED_END in text:
        if text.count(GENERATED_START) != 1 or text.count(GENERATED_END) != 1:
            errors.append(f"{readme.relative_to(ROOT)}: malformed generated contained-elements markers")
            return
        start = text.index(GENERATED_START)
        end = text.index(GENERATED_END, start) + len(GENERATED_END)
        updated = text[:start] + generated + text[end:]
    else:
        heading = CONTAINED_ELEMENTS_HEADING.search(text)
        if heading:
            tail = text[heading.end():]
            next_heading = re.search(r"^## ", tail, re.MULTILINE)
            end = heading.end() + (next_heading.start() if next_heading else len(tail))
            updated = text[:heading.start()] + generated + "\n\n" + text[end:].lstrip("\n")
        else:
            h1 = re.search(r"^# [^\n]+$", text, re.MULTILINE)
            if h1 is None:
                errors.append(f"{readme.relative_to(ROOT)}: cannot place generated contained-elements section")
                return
            updated = text[:h1.end()] + "\n\n" + generated + "\n" + text[h1.end():].lstrip("\n")
    if updated != text:
        if write:
            readme.write_text(updated, encoding="utf-8")
        else:
            errors.append(f"{readme.relative_to(ROOT)}: generated contained-elements section is stale")


def validate_contract_children(
    folder: Path, contract: dict[str, object], errors: list[str]
) -> None:
    for spec in contract.get("children", []):
        match = CHILD_SPEC.match(spec)
        if match is None:
            continue
        cardinality, display = match.groups()
        # Placeholder children describe a repeatable class, not one literal path.
        if "<" in display and ">" in display:
            continue
        label = re.sub(r"\s+#.*$", "", display).strip()
        alternatives = [part.strip() for part in re.split(r"\s+or\s+|\|", label)]
        paths = [folder / item.rstrip("/") for item in alternatives]
        existing = [path for path in paths if path.exists()]
        if cardinality == "1" and len(existing) != 1:
            errors.append(
                f"{folder.relative_to(ROOT)}/metadata.yaml: requires exactly one of {alternatives}"
            )
        if cardinality == "0..1" and len(existing) > 1:
            errors.append(
                f"{folder.relative_to(ROOT)}/metadata.yaml: permits at most one of {alternatives}"
            )
        for path in existing:
            if path.is_dir() and path.name != ".template" and not (path / "metadata.yaml").exists():
                errors.append(
                    f"{path.relative_to(ROOT)}/metadata.yaml: nested folder must define its own relationship level"
                )


def sync_recursive_folder_contracts(
    project: Path, categories: dict, errors: list[str], *, write: bool
) -> None:
    required_contracts = [project]
    inherited_entries: list[tuple[Path, Path]] = []
    for name, spec in categories.items():
        category = project / name
        required_contracts.append(category)
        category_type = spec.get("type") if isinstance(spec, dict) else None
        groups = spec.get("groups") if isinstance(spec, dict) else None
        if category_type == "folder-collection":
            if groups:
                for group_name in groups:
                    group = category / group_name
                    template = group / ".template"
                    required_contracts.extend((group, template))
                    for entry in group.iterdir() if group.exists() else []:
                        if entry.is_dir() and entry.name != ".template":
                            inherited_entries.append((entry, template))
            else:
                template = category / ".template"
                required_contracts.append(template)
                for entry in category.iterdir() if category.exists() else []:
                    if entry.is_dir() and entry.name != ".template":
                        inherited_entries.append((entry, template))

    seen: set[Path] = set()
    required_resolved = {folder.resolve() for folder in required_contracts}
    # Explicit contracts include required structural folders and nested subfolders.
    explicit_files = set(project.rglob("metadata.yaml"))
    for folder in required_contracts:
        contract_path = folder / "metadata.yaml"
        if not contract_path.exists():
            errors.append(f"{contract_path.relative_to(ROOT)}: missing recursive folder contract")
            continue
        explicit_files.add(contract_path)
    for contract_path in sorted(explicit_files):
        contract = parse_folder_contract(contract_path, errors)
        if contract is None or "children" not in contract:
            continue
        folder = contract_path.parent
        seen.add(folder.resolve())
        if contract.get("_type_check_excluded"):
            if folder.resolve() in required_resolved:
                errors.append(
                    f"{contract_path.relative_to(ROOT)}: structural folders cannot be excluded from type checking"
                )
            continue
        sync_contained_elements(folder / "README.md", contract, folder.name, errors, write=write)
        if contract.get("kind") == "object-domain":
            sync_object_domain_summary(folder / "README.md", contract, errors, write=write)
        validate_contract_children(folder, contract, errors)

    for entry, template in inherited_entries:
        if entry.resolve() in seen:
            continue
        template_contract = parse_folder_contract(template / "metadata.yaml", errors)
        if template_contract is None or "children" not in template_contract:
            continue
        sync_contained_elements(entry / "README.md", template_contract, entry.name, errors, write=write)
        validate_contract_children(entry, template_contract, errors)


def validate_manifest(project: Path, errors: list[str]) -> None:
    manifest_path = project / "spec.json"
    if not manifest_path.exists():
        errors.append(f"{project.relative_to(ROOT)}: missing spec.json")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"{manifest_path.relative_to(ROOT)}: invalid JSON: {exc}")
        return
    missing = REQUIRED_MANIFEST_FIELDS - manifest.keys()
    if missing:
        errors.append(f"{manifest_path.relative_to(ROOT)}: missing {sorted(missing)}")
    if manifest.get("slug") != project.name:
        errors.append(f"{manifest_path.relative_to(ROOT)}: slug must be {project.name!r}")
    if manifest.get("status") not in PROJECT_STATUSES:
        errors.append(
            f"{manifest_path.relative_to(ROOT)}: status must be one of {sorted(PROJECT_STATUSES)}"
        )


def parse_frontmatter(text: str) -> dict[str, object] | None:
    """Parse a minimal YAML-subset frontmatter block: scalars and simple lists."""
    text = text.lstrip("﻿")
    match = FRONTMATTER.match(text)
    if match is None:
        return None
    fields: dict[str, object] = {}
    lines = match.group(1).splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.startswith("#"):
            index += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest.startswith("[") and rest.endswith("]"):
            items = [item.strip().strip("'\"") for item in rest[1:-1].split(",") if item.strip()]
            fields[key] = items
            index += 1
            continue
        if rest:
            fields[key] = rest.strip("'\"")
            index += 1
            continue
        items = []
        index += 1
        while index < len(lines) and lines[index].lstrip().startswith("- "):
            items.append(lines[index].lstrip()[2:].strip().strip("'\""))
            index += 1
        fields[key] = items
    return fields


def check_entry_frontmatter(
    path: Path,
    project: Path,
    errors: list[str],
    *,
    expect_template: bool,
    allowed_statuses: set[str],
) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    relative = path.relative_to(project)
    if fields is None:
        errors.append(f"{relative}: missing frontmatter block")
        return None
    missing = REQUIRED_FRONTMATTER_FIELDS - fields.keys()
    if missing:
        errors.append(f"{relative}: frontmatter missing {sorted(missing)}")
    status = fields.get("status")
    accepted_statuses = allowed_statuses | {"template"}
    if status not in accepted_statuses:
        errors.append(
            f"{relative}: frontmatter status {status!r} is not one of "
            f"{sorted(accepted_statuses)}"
        )
    elif expect_template and status != "template":
        errors.append(f"{relative}: template entry must use status: template, found {status!r}")
    elif not expect_template and status == "template":
        errors.append(f"{relative}: real entry must not use status: template")
    return fields


def check_contained_elements(path: Path, project: Path, errors: list[str]) -> None:
    """Require a visible contained-elements tree in every typed container README."""
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(project)
    match = CONTAINED_ELEMENTS_HEADING.search(text)
    if match is None:
        errors.append(f"{relative}: missing '## Contained elements' section")
        return
    tail = text[match.end():]
    next_heading = re.search(r"^## ", tail, re.MULTILINE)
    section = tail[:next_heading.start()] if next_heading else tail
    if "```" not in section or TREE_CONNECTOR.search(section) is None:
        errors.append(f"{relative}: Contained elements section must include a fenced tree")
    if CARDINALITY_TOKEN.search(section) is None:
        errors.append(
            f"{relative}: Contained elements tree must state cardinality (1 / 0..1 / 0..*)"
        )


def check_fixed_category(
    project: Path, name: str, errors: list[str], *, allowed_statuses: set[str]
) -> set[str]:
    category = project / name
    readme = category / "README.md"
    refs: set[str] = set()
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        check_contained_elements(readme, project, errors)
    # Container READMEs are bare containers, not entries: the convention's own
    # metadata rule ("every entry, not bare containers") exempts them from frontmatter.
    if (category / ".template").is_dir():
        errors.append(
            f"{name}/.template/: a fixed top-structured category has no copy-and-rename "
            "entry mechanism, so it cannot have a folder template"
        )
    template_doc = category / "template.md"
    if template_doc.exists():
        # Optional per the convention: illustrates expected content, but nothing
        # copies it to create a new entry (a fixed category has no new entries).
        check_entry_frontmatter(
            template_doc,
            project,
            errors,
            expect_template=True,
            allowed_statuses=allowed_statuses,
        )
    for path in sorted(category.glob("*.md")):
        if path.name in NON_ENTRY_FILENAMES or path.name == "template.md":
            continue
        check_entry_frontmatter(
            path,
            project,
            errors,
            expect_template=False,
            allowed_statuses=allowed_statuses,
        )
        refs.add(f"{name}/{path.stem}")
    return refs


def check_document_collection_category(
    project: Path,
    name: str,
    errors: list[str],
    *,
    numbered: bool,
    allowed_statuses: set[str],
) -> set[str]:
    category = project / name
    readme = category / "README.md"
    refs: set[str] = set()
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        check_contained_elements(readme, project, errors)

    template_doc = category / "template.md"
    if not template_doc.exists():
        errors.append(f"{name}/template.md: missing copyable template document")
    else:
        check_entry_frontmatter(
            template_doc,
            project,
            errors,
            expect_template=True,
            allowed_statuses=allowed_statuses,
        )

    pattern = NUMBERED_ENTRY_PATTERN if numbered else SLUG_ENTRY_PATTERN
    pattern_help = (
        "<NNNN>-<slug>.md (four-digit sequence, lowercase kebab-case slug)"
        if numbered
        else "<slug>.md (lowercase kebab-case)"
    )
    for path in sorted(category.glob("*.md")):
        if path.name in NON_ENTRY_FILENAMES or path.name == "template.md":
            continue
        if not pattern.match(path.name):
            errors.append(f"{name}/{path.name}: entry filename must match {pattern_help}")
        check_entry_frontmatter(
            path,
            project,
            errors,
            expect_template=False,
            allowed_statuses=allowed_statuses,
        )
        refs.add(f"{name}/{path.stem}")
    return refs


def check_folder_collection_category(
    project: Path,
    name: str,
    entry_files: list[str],
    errors: list[str],
    *,
    allowed_statuses: set[str],
    groups: list[str] | None = None,
) -> set[str]:
    category = project / name
    readme = category / "README.md"
    refs: set[str] = set()
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        check_contained_elements(readme, project, errors)

    entries: list[Path] = []
    if groups:
        for group_name in groups:
            group = category / group_name
            group_readme = group / "README.md"
            if not group.is_dir():
                errors.append(f"{name}/{group_name}/: declared group is missing")
                continue
            if not group_readme.exists():
                errors.append(f"{name}/{group_name}/README.md: missing group README")
            else:
                check_contained_elements(group_readme, project, errors)
            template_dir = group / ".template"
            if not template_dir.is_dir():
                errors.append(
                    f"{name}/{group_name}/.template/: missing copyable template folder"
                )
            entries.extend(sorted(p for p in group.iterdir() if p.is_dir()))
    else:
        template_dir = category / ".template"
        if not template_dir.is_dir():
            errors.append(f"{name}/.template/: missing copyable template folder")
        entries = sorted(p for p in category.iterdir() if p.is_dir())

    for entry in entries:
        is_template = entry.name == ".template"
        if not is_template and not FOLDER_ENTRY_NAME_PATTERN.match(entry.name):
            errors.append(
                f"{entry.relative_to(project)}/: entry folder name must be lowercase "
                "kebab-case (e.g. widget-store)"
            )
        for required in entry_files:
            required_path = entry / required
            if not required_path.exists():
                errors.append(f"{entry.relative_to(project)}/{required}: missing")
            elif required.endswith(".md"):
                metadata_backed_readme = False
                if required == "README.md" and not is_template:
                    metadata_path = entry / "metadata.yaml"
                    if metadata_path.exists():
                        metadata = parse_folder_contract(metadata_path, errors)
                        metadata_backed_readme = bool(
                            metadata and metadata.get("kind") == "object-domain"
                        )
                if not metadata_backed_readme:
                    check_entry_frontmatter(
                        required_path,
                        project,
                        errors,
                        expect_template=is_template,
                        allowed_statuses=allowed_statuses,
                    )
                if required == "README.md":
                    check_contained_elements(required_path, project, errors)
        if not is_template:
            refs.add(str(entry.relative_to(project)).replace(os.sep, "/"))
    return refs


def check_references(
    project: Path,
    name: str,
    category_type: str,
    errors: list[str],
    known_refs: set[str],
    *,
    groups: list[str] | None = None,
) -> None:
    """Check related and supersedes values against declared project entries."""
    category = project / name
    if category_type == "folder-collection":
        if groups:
            candidates = [
                entry / "README.md"
                for group_name in groups
                for entry in (category / group_name).iterdir()
                if entry.is_dir()
            ]
        else:
            candidates = [
                p / "README.md"
                for p in category.iterdir()
                if p.is_dir() and p.name != ".template"
            ]
    else:
        candidates = [
            p for p in category.glob("*.md")
            if p.name not in NON_ENTRY_FILENAMES and p.name != "template.md"
        ]
    for path in candidates:
        if not path.exists():
            continue
        fields = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fields is None and path.name == "README.md":
            metadata_path = path.parent / "metadata.yaml"
            if metadata_path.exists():
                metadata = parse_folder_contract(metadata_path, errors)
                if metadata and metadata.get("kind") == "object-domain":
                    fields = metadata
        if fields is None:
            continue
        relative = path.relative_to(project)
        for ref in fields.get("related", []) or []:
            if ref and ref not in known_refs:
                errors.append(f"{relative}: related entry {ref!r} does not resolve to a known entry")
        supersedes = fields.get("supersedes")
        if supersedes and supersedes != "null" and supersedes not in known_refs:
            errors.append(f"{relative}: supersedes {supersedes!r} does not resolve to a known entry")


def check_typed_categories(project: Path, categories: dict, errors: list[str]) -> None:
    for name in ("README.md", "SPECS.md"):
        if not (project / name).exists():
            errors.append(f"{name}: missing (required once a project declares categories in spec.json)")
    root_readme = project / "README.md"
    if root_readme.exists():
        check_contained_elements(root_readme, project, errors)

    known_refs: set[str] = set()
    per_category: list[tuple[str, str, list[str] | None]] = []
    for name, spec in categories.items():
        category_type = spec.get("type") if isinstance(spec, dict) else None
        if category_type not in ALLOWED_CATEGORY_TYPES:
            errors.append(
                f"spec.json: categories.{name}.type must be one of {sorted(ALLOWED_CATEGORY_TYPES)}"
            )
            continue
        if not (project / name).is_dir():
            errors.append(f"{name}/: declared category is missing")
            continue
        groups = spec.get("groups") if isinstance(spec.get("groups"), list) else None
        configured_statuses = spec.get("statuses")
        if configured_statuses is None:
            allowed_statuses = ALLOWED_STATUSES - {"template"}
        elif (
            not isinstance(configured_statuses, list)
            or not configured_statuses
            or any(
                not isinstance(status, str) or not status.strip()
                for status in configured_statuses
            )
        ):
            errors.append(
                f"spec.json: categories.{name}.statuses must be a non-empty list "
                "of status names"
            )
            allowed_statuses = ALLOWED_STATUSES - {"template"}
        else:
            allowed_statuses = set(configured_statuses) - {"template"}
        per_category.append((name, category_type, groups))
        if category_type == "fixed":
            known_refs |= check_fixed_category(
                project, name, errors, allowed_statuses=allowed_statuses
            )
        elif category_type == "document-collection":
            numbered = bool(spec.get("numbered", True))
            known_refs |= check_document_collection_category(
                project,
                name,
                errors,
                numbered=numbered,
                allowed_statuses=allowed_statuses,
            )
        elif category_type == "folder-collection":
            entry_files = spec.get("entry_files") or ["README.md"]
            known_refs |= check_folder_collection_category(
                project,
                name,
                entry_files,
                errors,
                allowed_statuses=allowed_statuses,
                groups=groups,
            )

    for name, category_type, groups in per_category:
        check_references(
            project, name, category_type, errors, known_refs, groups=groups
        )


def validate_markdown(path: Path, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path.relative_to(ROOT)}: Markdown is not UTF-8")
        return
    link_content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    link_content = re.sub(r"`[^`\n]*`", "", link_content)
    for match in MARKDOWN_LINK.finditer(link_content):
        target = match.group(1).split("#", 1)[0].strip().strip("<>")
        if not target or target.startswith("/"):
            continue
        if not (path.parent / target).resolve().exists():
            errors.append(f"{path.relative_to(ROOT)}: broken relative link {target!r}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    all_files = files()

    projects = sorted(path for path in (ROOT / "projects").iterdir() if path.is_dir())
    if not projects:
        errors.append("projects/: at least one project is required")
    for project in projects:
        validate_manifest(project, errors)
        manifest_path = project / "spec.json"
        if manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                manifest = {}
            categories = manifest.get("categories")
            if isinstance(categories, dict):
                write_contracts = "--check" not in sys.argv
                sync_recursive_folder_contracts(
                    project, categories, errors, write=write_contracts
                )
                check_typed_categories(project, categories, errors)

    for path in all_files:
        relative = path.relative_to(ROOT)
        if path.name.startswith(".~lock.") or path.suffix in {".pyc", ".tmp", ".swp"}:
            errors.append(f"{relative}: temporary or generated file is tracked")
        size = path.stat().st_size
        if size >= MAX_FILE_BYTES:
            errors.append(f"{relative}: {size / 1024 / 1024:.1f} MiB exceeds GitHub's limit")
        elif size >= WARN_FILE_BYTES:
            warnings.append(f"{relative}: large file ({size / 1024 / 1024:.1f} MiB)")
        if path.suffix.lower() == ".md":
            validate_markdown(path, errors)

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    print(
        f"Validated {len(projects)} project(s) and {len(all_files)} file(s): "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
