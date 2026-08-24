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
