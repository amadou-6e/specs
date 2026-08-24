from __future__ import annotations

import argparse
import html
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


@dataclass(slots=True)
class RegionCandidate:
    id: int
    color: str
    threshold: int
    x: int
    y: int
    width: int
    height: int
    area_pixels: int
    bbox_area: int
    extent: float
    solidity: float
    confidence: float
    svg_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect large layout/image regions from a raster layout.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--top-colors", type=int, default=14)
    parser.add_argument("--thresholds", nargs="+", type=int, default=[14, 18, 24, 32])
    parser.add_argument("--min-area", type=int, default=25000)
    parser.add_argument("--min-width", type=int, default=100)
    parser.add_argument("--min-height", type=int, default=100)
    parser.add_argument("--merge-overlap", type=float, default=0.72)
    parser.add_argument("--containment", type=float, default=0.88)
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def dominant_colors(image_rgb: np.ndarray, top_k: int) -> list[tuple[int, int, int]]:
    quantized = ((image_rgb.astype(np.uint16) // 8) * 8).astype(np.uint32)
    flat = quantized.reshape((-1, 3))
    packed = flat[:, 0] * 65536 + flat[:, 1] * 256 + flat[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    order = np.argsort(counts)[::-1]
    colors: list[tuple[int, int, int]] = []
    for index in order[:top_k]:
        value = int(values[index])
        colors.append(((value // 65536) + 4, ((value // 256) % 256) + 4, (value % 256) + 4))
    return colors


def estimate_background(image_rgb: np.ndarray) -> tuple[int, int, int]:
    border = np.concatenate(
        [image_rgb[0, :, :], image_rgb[-1, :, :], image_rgb[:, 0, :], image_rgb[:, -1, :]],
        axis=0,
    )
    quantized = ((border.astype(np.uint16) // 8) * 8).astype(np.uint32)
    packed = quantized[:, 0] * 65536 + quantized[:, 1] * 256 + quantized[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    value = int(values[int(np.argmax(counts))])
    return ((value // 65536) + 4, ((value // 256) % 256) + 4, (value % 256) + 4)


def color_mask(image_rgb: np.ndarray, color: tuple[int, int, int], threshold: int) -> np.ndarray:
    target = np.array(color, dtype=np.float32)
    distance = np.linalg.norm(image_rgb.astype(np.float32) - target, axis=2)
    mask = (distance <= threshold).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    return mask


def contour_to_path(contour: np.ndarray) -> str:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.006 * perimeter, True)
    points = approx.reshape((-1, 2))
    if len(points) < 3:
        return ""
    chunks = [f"M {int(points[0][0])} {int(points[0][1])}"]
    for point in points[1:]:
        chunks.append(f"L {int(point[0])} {int(point[1])}")
    chunks.append("Z")
    return " ".join(chunks)


def bbox(candidate: RegionCandidate) -> tuple[int, int, int, int]:
    return candidate.x, candidate.y, candidate.width, candidate.height


def overlap_area(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x0 = max(ax, bx)
    y0 = max(ay, by)
    x1 = min(ax + aw, bx + bw)
    y1 = min(ay + ah, by + bh)
    return max(0, x1 - x0) * max(0, y1 - y0)


def candidate_rank(candidate: RegionCandidate) -> tuple[float, int, float]:
    # Prefer compact large regions over broad bands caused by loose thresholds.
    return (candidate.extent, candidate.area_pixels, candidate.solidity)


def merge_candidates(candidates: list[RegionCandidate], merge_overlap: float, containment: float) -> list[RegionCandidate]:
    kept: list[RegionCandidate] = []
    for candidate in sorted(candidates, key=candidate_rank, reverse=True):
        candidate_box = bbox(candidate)
        candidate_area = max(candidate.width * candidate.height, 1)
        duplicate = False
        for kept_candidate in kept:
            kept_box = bbox(kept_candidate)
            kept_area = max(kept_candidate.width * kept_candidate.height, 1)
            overlap = overlap_area(candidate_box, kept_box)
            union = candidate_area + kept_area - overlap
            iou = overlap / max(union, 1)
            candidate_inside_kept = overlap / candidate_area
            kept_inside_candidate = overlap / kept_area
            if iou >= merge_overlap:
                duplicate = True
                break
            if candidate_inside_kept >= containment and kept_candidate.area_pixels >= candidate.area_pixels:
                duplicate = True
                break
            if kept_inside_candidate >= containment and candidate.area_pixels > kept_candidate.area_pixels:
                kept.remove(kept_candidate)
                break
        if not duplicate:
            kept.append(candidate)
    kept.sort(key=lambda item: (item.y, item.x))
    for index, candidate in enumerate(kept, start=1):
        candidate.id = index
    return kept


def detect_regions(image_rgb: np.ndarray, args: argparse.Namespace) -> tuple[list[RegionCandidate], tuple[int, int, int], list[tuple[int, int, int]]]:
    background = estimate_background(image_rgb)
    colors = []
    for color in dominant_colors(image_rgb, args.top_colors):
        if np.linalg.norm(np.array(color, dtype=np.float32) - np.array(background, dtype=np.float32)) > 35:
            colors.append(color)

    candidates: list[RegionCandidate] = []
    for color in colors:
        for threshold in args.thresholds:
            mask = color_mask(image_rgb, color, threshold)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                area = int(cv2.contourArea(contour))
                if area < args.min_area:
                    continue
                x, y, width, height = cv2.boundingRect(contour)
                if width < args.min_width or height < args.min_height:
                    continue
                component = np.zeros(mask.shape, dtype=np.uint8)
                cv2.drawContours(component, [contour], -1, 255, thickness=-1)
                pixels = int(np.count_nonzero(component))
                bbox_area = max(width * height, 1)
                hull = cv2.convexHull(contour)
                hull_area = max(float(cv2.contourArea(hull)), 1.0)
                extent = pixels / bbox_area
                solidity = float(area / hull_area)
                confidence = min(1.0, 0.25 + extent * 0.45 + solidity * 0.2 + min(pixels / 120000.0, 1.0) * 0.1)
                candidates.append(
                    RegionCandidate(
                        id=0,
                        color=rgb_to_hex(color),
                        threshold=int(threshold),
                        x=int(x),
                        y=int(y),
                        width=int(width),
                        height=int(height),
                        area_pixels=pixels,
                        bbox_area=bbox_area,
                        extent=round(float(extent), 4),
                        solidity=round(float(solidity), 4),
                        confidence=round(float(confidence), 4),
                        svg_path=contour_to_path(contour),
                    )
                )
    return merge_candidates(candidates, args.merge_overlap, args.containment), background, colors


def write_svg(path: Path, width: int, height: int, background: str, regions: list[RegionCandidate]) -> None:
    strokes = ["#FF2E88", "#00A8FF", "#FFB000", "#00C853", "#7C4DFF"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <rect width="100%" height="100%" fill="{html.escape(background)}"/>',
        '  <g id="layout-regions" stroke-linejoin="round">',
    ]
    for index, region in enumerate(regions):
        stroke = strokes[index % len(strokes)]
        lines.append(
            f'    <path id="region-{region.id}" d="{html.escape(region.svg_path)}" fill="{html.escape(region.color)}" fill-opacity="0.55" stroke="{stroke}" stroke-width="3"/>'
        )
        lines.append(
            f'    <text x="{region.x + 6}" y="{region.y + 18}" font-family="monospace" font-size="14" fill="{stroke}" stroke="#fff" stroke-width="1.5" paint-order="stroke">#{region.id} {region.width}x{region.height}</text>'
        )
    lines.extend(['  </g>', '</svg>', ''])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_overlay(path: Path, image_rgb: np.ndarray, regions: list[RegionCandidate]) -> None:
    image = Image.fromarray(image_rgb).convert("RGB")
    draw = ImageDraw.Draw(image)
    colors = [(255, 46, 136), (0, 168, 255), (255, 176, 0), (0, 200, 83), (124, 77, 255)]
    for index, region in enumerate(regions):
        color = colors[index % len(colors)]
        draw.rectangle((region.x, region.y, region.x + region.width, region.y + region.height), outline=color, width=4)
        draw.text((region.x + 6, region.y + 6), f"#{region.id} {region.width}x{region.height}", fill=color)
    image.save(path)


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    out_dir = resolve_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    image_rgb = load_rgb(image_path)
    regions, background, colors = detect_regions(image_rgb, args)
    height, width = image_rgb.shape[:2]
    payload = {
        "image": str(image_path),
        "background_color": rgb_to_hex(background),
        "searched_colors": [rgb_to_hex(color) for color in colors],
        "region_count": len(regions),
        "regions": [asdict(region) for region in regions],
        "notes": [
            "This detector targets large layout/image regions and intentionally ignores small texture/text fragments.",
            "Run scripts/detect_shapes.py for fine-grained color-island extraction.",
        ],
    }
    out_dir.joinpath("detected_regions.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_svg(out_dir.joinpath("detected_regions.svg"), width, height, rgb_to_hex(background), regions)
    write_overlay(out_dir.joinpath("detected_regions_overlay.png"), image_rgb, regions)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
