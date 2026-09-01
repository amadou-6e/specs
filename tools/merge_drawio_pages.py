#!/usr/bin/env python3
"""Append pages from one Draw.io document to another without altering page content."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "pages",
        nargs="*",
        help="Exact source page IDs or names; all pages are appended when omitted",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_tree = ET.parse(args.target)
    target_root = target_tree.getroot()
    source_root = ET.parse(args.source).getroot()

    wanted = set(args.pages)
    source_pages = [
        page
        for page in source_root.findall("diagram")
        if not wanted or page.get("id") in wanted or page.get("name") in wanted
    ]
    matched = {page.get("id") for page in source_pages} | {
        page.get("name") for page in source_pages
    }
    missing = [page for page in args.pages if page not in matched]
    if missing:
        raise SystemExit(f"Pages not found in {args.source}: {', '.join(missing)}")

    existing_ids = {page.get("id") for page in target_root.findall("diagram")}
    duplicate_ids = [page.get("id") for page in source_pages if page.get("id") in existing_ids]
    if duplicate_ids:
        raise SystemExit(f"Duplicate page IDs: {', '.join(duplicate_ids)}")

    for page in source_pages:
        target_root.append(copy.deepcopy(page))
    target_root.set("pages", str(len(target_root.findall("diagram"))))

    ET.indent(target_tree, space="  ")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    target_tree.write(args.output, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
