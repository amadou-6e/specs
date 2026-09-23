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
# <slug> for folder-collection entry directory names (never "template").
FOLDER_ENTRY_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Filenames that are never treated as a spec entry, even inside a declared category
# (README.md is the container; SKILL.md marks an invokable agent skill, not a spec).
NON_ENTRY_FILENAMES = {"README.md", "SKILL.md"}

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def files() -> list[Path]:
    discovered: list[Path] = []
    for directory, names, filenames in os.walk(ROOT):
        names[:] = [name for name in names if name not in IGNORED_PARTS]
        discovered.extend(Path(directory) / filename for filename in filenames)
    return discovered


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


def check_fixed_category(
    project: Path, name: str, errors: list[str], *, allowed_statuses: set[str]
) -> set[str]:
    category = project / name
    readme = category / "README.md"
    refs: set[str] = set()
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    # Container READMEs are bare containers, not entries: the convention's own
    # metadata rule ("every entry, not bare containers") exempts them from frontmatter.
    if (category / "template").is_dir():
        errors.append(
            f"{name}/template/: a fixed top-structured category has no copy-and-rename "
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
) -> set[str]:
    category = project / name
    readme = category / "README.md"
    refs: set[str] = set()
    if not readme.exists():
        errors.append(f"{name}/README.md: missing container README")
    else:
        text = readme.read_text(encoding="utf-8")
        if not re.search(r"\b0\.\.\*|\b0\.\.1\b|(?<!\.)\b1\b", text):
            errors.append(f"{name}/README.md: container README must state cardinality (1 / 0..1 / 0..*)")

    template_dir = category / "template"
    if not template_dir.is_dir():
        errors.append(f"{name}/template/: missing copyable template folder")

    entries = sorted(p for p in category.iterdir() if p.is_dir())
    for entry in entries:
        is_template = entry.name == "template"
        if not is_template and not FOLDER_ENTRY_NAME_PATTERN.match(entry.name):
            errors.append(
                f"{name}/{entry.name}/: entry folder name must be lowercase kebab-case "
                "(e.g. widget-store)"
            )
        for required in entry_files:
            required_path = entry / required
            if not required_path.exists():
                errors.append(f"{name}/{entry.name}/{required}: missing")
            elif required.endswith(".md"):
                check_entry_frontmatter(
                    required_path,
                    project,
                    errors,
                    expect_template=is_template,
                    allowed_statuses=allowed_statuses,
                )
        if not is_template:
            refs.add(f"{name}/{entry.name}")
    return refs


def check_references(
    project: Path, name: str, category_type: str, errors: list[str], known_refs: set[str]
) -> None:
    """Check that every non-empty `related` entry and non-null `supersedes` value
    resolves to a real entry declared somewhere in this project's categories."""
    category = project / name
    if category_type == "folder-collection":
        candidates = [p / "README.md" for p in category.iterdir() if p.is_dir() and p.name != "template"]
    else:
        candidates = [
            p for p in category.glob("*.md")
            if p.name not in NON_ENTRY_FILENAMES and p.name != "template.md"
        ]
    for path in candidates:
        if not path.exists():
            continue
        fields = parse_frontmatter(path.read_text(encoding="utf-8"))
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

    known_refs: set[str] = set()
    per_category: list[tuple[str, str]] = []
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
        per_category.append((name, category_type))
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
            )

    for name, category_type in per_category:
        check_references(project, name, category_type, errors, known_refs)


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
