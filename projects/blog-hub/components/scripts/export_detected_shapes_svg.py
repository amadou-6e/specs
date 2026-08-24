from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

from PIL import Image


STROKES = [
    "#FF2E88",
    "#00A8FF",
    "#FFB000",
    "#00C853",
    "#7C4DFF",
    "#FF5F1F",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export detected shape JSON files as inspectable SVGs.")
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path("scripts", "shape_detection_round_complex"),
        help="Directory to scan for detected_shapes.json files.",
    )
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def image_size(payload: dict[str, Any], shapes: list[dict[str, Any]]) -> tuple[int, int]:
    image_value = payload.get("image")
    if isinstance(image_value, str) and image_value:
        image_path = resolve_path(Path(image_value))
        if image_path.exists():
            with Image.open(image_path) as image:
                return image.size

    max_x = 1
    max_y = 1
    for shape in shapes:
        max_x = max(max_x, int(shape.get("x", 0)) + int(shape.get("width", 0)))
        max_y = max(max_y, int(shape.get("y", 0)) + int(shape.get("height", 0)))
    return max_x, max_y


def draw_order(shape: dict[str, Any]) -> tuple[int, int]:
    layer = int(shape.get("layer", 1))
    area = int(shape.get("area_pixels", 0))
    return (-layer, -area)


def label_position(shape: dict[str, Any]) -> tuple[int, int]:
    x = int(shape.get("x", 0))
    y = int(shape.get("y", 0))
    return x + 4, max(12, y + 12)


def export_svg(json_path: Path) -> Path:
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    shapes = list(payload.get("shapes", []))
    width, height = image_size(payload, shapes)
    background = str(payload.get("background_color", "#FFFFFF"))
    title = json_path.parent.name or json_path.parent.parent.name

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <title>{html.escape(title)} detected shapes</title>',
        f'  <rect width="100%" height="100%" fill="{html.escape(background)}"/>',
        '  <g id="detected-shapes" stroke-linejoin="round">',
    ]

    for index, shape in enumerate(sorted(shapes, key=draw_order), start=1):
        path_data = str(shape.get("svg_path", "")).strip()
        if not path_data:
            continue
        fill = str(shape.get("color", "#000000"))
        stroke = STROKES[(index - 1) % len(STROKES)]
        shape_id = html.escape(str(shape.get("id", index)))
        layer = html.escape(str(shape.get("layer", 1)))
        kind = html.escape(str(shape.get("kind", "shape")))
        confidence = html.escape(str(shape.get("confidence", "")))
        label_x, label_y = label_position(shape)
        lines.extend(
            [
                f'    <path id="shape-{shape_id}" d="{html.escape(path_data)}" fill="{html.escape(fill)}" fill-opacity="0.72" stroke="{stroke}" stroke-width="2"/>',
                f'    <text x="{label_x}" y="{label_y}" font-family="monospace" font-size="9" fill="{stroke}" stroke="#FFFFFF" stroke-width="0.8" paint-order="stroke">#{shape_id} L{layer} {kind} {confidence}</text>',
            ]
        )

    lines.extend(
        [
            '  </g>',
            '</svg>',
            '',
        ]
    )
    svg_path = json_path.parent.joinpath("detected_shapes.svg")
    svg_path.write_text("\n".join(lines), encoding="utf-8")
    return svg_path


def main() -> int:
    args = parse_args()
    root = resolve_path(args.root)
    json_paths = sorted(root.rglob("detected_shapes.json"))
    for json_path in json_paths:
        svg_path = export_svg(json_path)
        print(svg_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
