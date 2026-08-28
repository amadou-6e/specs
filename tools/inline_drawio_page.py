#!/usr/bin/env python3
"""Move one Draw.io page below another page in the same document."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("drawio", type=Path)
    parser.add_argument("target_page")
    parser.add_argument("source_page")
    parser.add_argument("--offset-y", type=float, required=True)
    parser.add_argument("--section", required=True)
    return parser.parse_args()


def find_page(root: ET.Element, page_id: str) -> ET.Element:
    page = next(
        (
            diagram
            for diagram in root.findall("diagram")
            if diagram.get("id") == page_id or diagram.get("name") == page_id
        ),
        None,
    )
    if page is None:
        raise SystemExit(f"Page not found: {page_id}")
    return page


def main() -> None:
    args = parse_args()
    tree = ET.parse(args.drawio)
    root = tree.getroot()
    target_page = find_page(root, args.target_page)
    source_page = find_page(root, args.source_page)
    target_model = target_page.find("mxGraphModel")
    source_model = source_page.find("mxGraphModel")
    target_root = target_model.find("root")
    source_root = source_model.find("root")

    target_ids = {cell.get("id") for cell in target_root}
    source_cells = [cell for cell in source_root if cell.get("id") not in {"0", "1"}]
    collisions = sorted(
        cell.get("id") for cell in source_cells if cell.get("id") in target_ids
    )
    if collisions:
        raise SystemExit(f"Cell ID collisions: {', '.join(collisions)}")

    for source_cell in source_cells:
        cell = copy.deepcopy(source_cell)
        cell.set("bloghubSection", args.section)
        geometry = cell.find("mxGeometry")
        if (
            geometry is not None
            and cell.get("parent") == "1"
            and geometry.get("relative") != "1"
            and geometry.get("y") is not None
        ):
            geometry.set(
                "y", f"{float(geometry.get('y', '0')) + args.offset_y:g}"
            )
        target_root.append(cell)

    target_width = max(
        float(target_model.get("pageWidth", "0")),
        float(source_model.get("pageWidth", "0")),
    )
    target_height = max(
        float(target_model.get("pageHeight", "0")),
        args.offset_y + float(source_model.get("pageHeight", "0")),
    )
    target_model.set("pageWidth", f"{target_width:g}")
    target_model.set("pageHeight", f"{target_height:g}")

    root.remove(source_page)
    root.set("pages", str(len(root.findall("diagram"))))
    ET.indent(tree, space="  ")
    tree.write(args.drawio, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
