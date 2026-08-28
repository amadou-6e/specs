#!/usr/bin/env python3
"""Extract rectangular regions of a Draw.io page as normalized diagram pages."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class Region:
    diagram_id: str
    name: str
    x: float
    y: float
    width: float
    height: float


def parse_region(value: str) -> Region:
    parts = value.split("|")
    if len(parts) != 6:
        raise argparse.ArgumentTypeError(
            "region must be ID|NAME|X|Y|WIDTH|HEIGHT"
        )
    diagram_id, name, x, y, width, height = parts
    try:
        return Region(diagram_id, name, float(x), float(y), float(width), float(height))
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid region coordinates: {value}") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("source_page", help="Exact source diagram ID or name")
    parser.add_argument(
        "--region",
        action="append",
        required=True,
        type=parse_region,
        help="Output page as ID|NAME|X|Y|WIDTH|HEIGHT; may be repeated",
    )
    parser.add_argument("--margin", type=float, default=40)
    parser.add_argument(
        "--font-family",
        help="Replace explicit fontFamily style values in the extracted pages",
    )
    return parser.parse_args()


def geometry(cell: ET.Element) -> ET.Element | None:
    return cell.find("mxGeometry")


def cell_bounds(cell: ET.Element) -> tuple[float, float, float, float] | None:
    node = geometry(cell)
    if node is None or node.get("relative") == "1":
        return None
    try:
        return (
            float(node.get("x", "0")),
            float(node.get("y", "0")),
            float(node.get("width", "0")),
            float(node.get("height", "0")),
        )
    except ValueError:
        return None


def inside_region(
    bounds: tuple[float, float, float, float], region: Region, epsilon: float = 0.01
) -> bool:
    x, y, width, height = bounds
    return (
        x >= region.x - epsilon
        and y >= region.y - epsilon
        and x + width <= region.x + region.width + epsilon
        and y + height <= region.y + region.height + epsilon
    )


def selected_ids(cells: list[ET.Element], region: Region) -> set[str]:
    selected = {
        cell.get("id", "")
        for cell in cells
        if (bounds := cell_bounds(cell)) is not None and inside_region(bounds, region)
    }

    changed = True
    while changed:
        changed = False
        for cell in cells:
            cell_id = cell.get("id", "")
            if cell_id not in selected and cell.get("parent") in selected:
                selected.add(cell_id)
                changed = True

    for cell in cells:
        if cell.get("edge") == "1" and {
            cell.get("source"),
            cell.get("target"),
        } <= selected:
            selected.add(cell.get("id", ""))
    return selected


def replace_font_family(style: str, font_family: str) -> str:
    parts = [part for part in style.split(";") if part]
    replaced = False
    for index, part in enumerate(parts):
        if part.startswith("fontFamily="):
            parts[index] = f"fontFamily={font_family}"
            replaced = True
    if not replaced:
        return style
    return ";".join(parts) + ";"


def extract_region(
    source_model: ET.Element,
    region: Region,
    margin: float,
    font_family: str | None,
) -> ET.Element:
    model = ET.Element(source_model.tag, source_model.attrib)
    model.set("pageWidth", f"{region.width + 2 * margin:g}")
    model.set("pageHeight", f"{region.height + 2 * margin:g}")
    root = ET.SubElement(model, "root")

    source_root = source_model.find("root")
    if source_root is None:
        raise SystemExit("Source diagram has no mxGraphModel/root")
    cells = list(source_root)
    keep = selected_ids(cells, region)

    for cell in cells:
        cell_id = cell.get("id", "")
        if cell_id not in {"0", "1"} and cell_id not in keep:
            continue
        cloned = copy.deepcopy(cell)
        if font_family and cloned.get("style"):
            cloned.set("style", replace_font_family(cloned.get("style", ""), font_family))
        node = geometry(cloned)
        if node is not None and cloned.get("parent") == "1":
            if node.get("x") is not None:
                node.set("x", f"{float(node.get('x', '0')) - region.x + margin:g}")
            if node.get("y") is not None:
                node.set("y", f"{float(node.get('y', '0')) - region.y + margin:g}")
        root.append(cloned)

    return model


def main() -> None:
    args = parse_args()
    tree = ET.parse(args.source)
    source_root = tree.getroot()
    source_diagram = next(
        (
            diagram
            for diagram in source_root.findall("diagram")
            if diagram.get("id") == args.source_page
            or diagram.get("name") == args.source_page
        ),
        None,
    )
    if source_diagram is None:
        raise SystemExit(f"Source page not found: {args.source_page}")
    source_model = source_diagram.find("mxGraphModel")
    if source_model is None:
        raise SystemExit("Compressed Draw.io pages are not supported")

    output_root = ET.Element(source_root.tag, source_root.attrib)
    for region in args.region:
        diagram = ET.SubElement(
            output_root, "diagram", {"id": region.diagram_id, "name": region.name}
        )
        diagram.append(
            extract_region(source_model, region, args.margin, args.font_family)
        )

    output_tree = ET.ElementTree(output_root)
    ET.indent(output_tree, space="  ")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output_tree.write(args.output, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main()
