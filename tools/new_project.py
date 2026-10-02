#!/usr/bin/env python3
"""Create a small, consistent project specification scaffold."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("name")
    parser.add_argument("--source-repository", default="")
    args = parser.parse_args()

    if not SLUG_PATTERN.fullmatch(args.slug):
        parser.error("slug must contain lowercase letters, numbers, and single hyphens")

    project = ROOT / "projects" / args.slug
    if project.exists():
        parser.error(f"project already exists: {project.relative_to(ROOT)}")

    (project / "features").mkdir(parents=True)
    (project / "architecture").mkdir()
    (project / "contracts").mkdir()
    (project / "ui").mkdir()

    manifest = {
        "name": args.name,
        "slug": args.slug,
        "source_repository": args.source_repository,
        "status": "active",
        "description": "",
    }
    (project / "spec.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    (project / "README.md").write_text(
        f"# {args.name}\n\n"
        "This is a bootstrap, not a completed specification or typed authoring system.\n"
        "Define the problem, users, scope, constraints and open decisions before implementation.\n\n"
        "Use the [authoring overview](../../shared/skills/spec-authoring-system/references/workflow.md)\n"
        "to establish SPECS.md, manifest categories, container READMEs and project-owned templates.\n"
        "The bootstrap directories may be reorganized as part of that explicit setup;\n"
        "they do not declare category ownership or opt into typed validation.\n",
        encoding="utf-8",
    )
    print(f"Created {project.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

