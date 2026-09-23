#!/usr/bin/env python3
"""Validate the typed-and-named-folder-hierarchy worked example.

This checks the bundled `example/projects/example-project/` tree against the
rules documented in `README.md` next to this script: the three structural
types (fixed top-structured, expandable folder collection, expandable
document collection), the container/README/cardinality rule, the
copy-and-rename template convention, and the entry frontmatter contract.

It is a teaching fixture, not the repository-wide validator: see
`tools/validate_specs.py` at the specs repository root for that.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR / "example" / "projects" / "example-project"

REQUIRED_MANIFEST_FIELDS = {"name", "slug", "source_repository", "status"}
PROJECT_STATUSES = {"active", "paused", "archived"}

REQUIRED_FRONTMATTER_FIELDS = {
    "title", "status", "kind", "owners", "last_reviewed", "applies_to",
}
ALLOWED_STATUSES = {
    "draft", "active", "complete", "deprecated", "superseded", "template",
}

# category -> structural type
CATEGORIES = {
    "architecture": "fixed",
    "subsystems": "folder-collection",
    "decisions": "document-collection",
}

# required files inside every subsystems/<entry>/ (template and real entries alike)
SUBSYSTEM_ENTRY_FILES = ("README.md", "contract/README.md", "design/README.md", "validation.md")

DECISION_ENTRY_PATTERN = re.compile(r"^\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


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
        # No inline value: collect following `- item` list lines, if any.
        items = []
        index += 1
        while index < len(lines) and lines[index].lstrip().startswith("- "):
            items.append(lines[index].lstrip()[2:].strip().strip("'\""))
            index += 1
        fields[key] = items
    return fields


def check_entry_frontmatter(path: Path, errors: list[str], *, expect_template: bool) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    relative = path.relative_to(PROJECT_ROOT)
    if fields is None:
        errors.append(f"{relative}: missing frontmatter block")
        return None
    missing = REQUIRED_FRONTMATTER_FIELDS - fields.keys()
    if missing:
        errors.append(f"{relative}: frontmatter missing {sorted(missing)}")
    status = fields.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{relative}: frontmatter status {status!r} is not one of {sorted(ALLOWED_STATUSES)}")
    elif expect_template and status != "template":
        errors.append(f"{relative}: template entry must use status: template, found {status!r}")
    elif not expect_template and status == "template":
        errors.append(f"{relative}: real entry must not use status: template")
    return fields


def check_manifest(errors: list[str]) -> None:
    manifest_path = PROJECT_ROOT / "spec.json"
    if not manifest_path.exists():
        errors.append("spec.json: missing")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"spec.json: invalid JSON: {exc}")
        return
    missing = REQUIRED_MANIFEST_FIELDS - manifest.keys()
    if missing:
        errors.append(f"spec.json: missing {sorted(missing)}")
    if manifest.get("slug") != PROJECT_ROOT.name:
        errors.append(f"spec.json: slug must be {PROJECT_ROOT.name!r}")
    if manifest.get("status") not in PROJECT_STATUSES:
        errors.append(f"spec.json: status must be one of {sorted(PROJECT_STATUSES)}")


def check_root_documents(errors: list[str]) -> None:
    for name in ("README.md", "SPECS.md"):
        path = PROJECT_ROOT / name
        if not path.exists():
            errors.append(f"{name}: missing")
    check_manifest(errors)


def check_fixed_category(name: str, errors: list[str]) -> None:
    category = PROJECT_ROOT / name
    readme = category / "README.md"
    if not readme.exists():
        errors.append(f"{name}/README.md: missing")
    else:
        check_entry_frontmatter(readme, errors, expect_template=False)
    for forbidden in ("template", "template.md"):
        if (category / forbidden).exists():
            errors.append(f"{name}/{forbidden}: a fixed top-structured category must not have a copyable template")


def check_folder_collection_category(name: str, errors: list[str]) -> None:
    category = PROJECT_ROOT / name
    readme = category / "README.md"
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        fields = check_entry_frontmatter(readme, errors, expect_template=False)
        text = readme.read_text(encoding="utf-8")
        if fields is not None and not re.search(r"\b0\.\.\*|\b0\.\.1\b|(?<!\.)\b1\b", text):
            errors.append(f"{name}/README.md: container README must state cardinality (1 / 0..1 / 0..*)")

    template_dir = category / "template"
    if not template_dir.is_dir():
        errors.append(f"{name}/template/: missing copyable template folder")

    entries = sorted(p for p in category.iterdir() if p.is_dir())
    if template_dir not in entries and template_dir.is_dir():
        entries.append(template_dir)
    for entry in entries:
        is_template = entry.name == "template"
        for required in SUBSYSTEM_ENTRY_FILES:
            required_path = entry / required
            if not required_path.exists():
                errors.append(f"{name}/{entry.name}/{required}: missing")
            elif required.endswith(".md"):
                check_entry_frontmatter(required_path, errors, expect_template=is_template)


def check_document_collection_category(name: str, errors: list[str]) -> None:
    category = PROJECT_ROOT / name
    readme = category / "README.md"
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        check_entry_frontmatter(readme, errors, expect_template=False)

    template_doc = category / "template.md"
    if not template_doc.exists():
        errors.append(f"{name}/template.md: missing copyable template document")
    else:
        check_entry_frontmatter(template_doc, errors, expect_template=True)

    for path in sorted(category.glob("*.md")):
        if path.name in {"README.md", "template.md"}:
            continue
        if not DECISION_ENTRY_PATTERN.match(path.name):
            errors.append(f"{name}/{path.name}: entry filename must match <NNNN>-<slug>.md")
        check_entry_frontmatter(path, errors, expect_template=False)


def main() -> int:
    errors: list[str] = []

    if not PROJECT_ROOT.is_dir():
        print(f"error: example project not found at {PROJECT_ROOT}", file=sys.stderr)
        return 1

    check_root_documents(errors)
    for category, structural_type in CATEGORIES.items():
        if not (PROJECT_ROOT / category).is_dir():
            errors.append(f"{category}/: declared category is missing")
            continue
        if structural_type == "fixed":
            check_fixed_category(category, errors)
        elif structural_type == "folder-collection":
            check_folder_collection_category(category, errors)
        elif structural_type == "document-collection":
            check_document_collection_category(category, errors)

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    print(f"Validated {PROJECT_ROOT.relative_to(SCRIPT_DIR)}: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
