#!/usr/bin/env python3
"""Extract selected Draw.io pages into a standalone, editable document."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "pages",
        nargs="+",
        help="Exact diagram IDs or names to preserve, in source order.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tree = ET.parse(args.source)
    source_root = tree.getroot()
    wanted = set(args.pages)
    selected = [
        diagram
        for diagram in source_root.findall("diagram")
        if diagram.get("id") in wanted or diagram.get("name") in wanted
    ]
    matched = {diagram.get("id") for diagram in selected} | {
        diagram.get("name") for diagram in selected
    }
    missing = [page for page in args.pages if page not in matched]
    if missing:
        raise SystemExit(f"Pages not found in {args.source}: {', '.join(missing)}")

    output_root = ET.Element(source_root.tag, source_root.attrib)
    for diagram in selected:
        output_root.append(copy.deepcopy(diagram))

    output_tree = ET.ElementTree(output_root)
    ET.indent(output_tree, space="  ")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output_tree.write(args.output, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
