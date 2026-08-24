from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


@dataclass(slots=True)
class RgbColor:
    r: int
    g: int
    b: int

    @property
    def hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"


@dataclass(slots=True)
class ShapeCandidate:
    id: int
    layer: int
    color: str
    kind: str
    x: int
    y: int
    width: int
    height: int
    area_pixels: int
    contour_area: float
    perimeter: float
    vertices: int
    circularity: float
    solidity: float
    extent: float
    estimated_radius: float
    text_overlap_ratio: float
    confidence: float
    svg_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect flat UI shapes while masking/reconstructing text occlusions."
    )
    parser.add_argument("image", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--shape-color", default=None, help="Optional #RRGGBB shape fill color")
    parser.add_argument("--background-color", default=None, help="Optional #RRGGBB background color to ignore")
    parser.add_argument("--color-distance", type=float, default=28.0)
    parser.add_argument("--min-area", type=int, default=80)
    parser.add_argument("--close-kernel", type=int, default=11)
    parser.add_argument("--open-kernel", type=int, default=3)
    parser.add_argument("--split-erode-kernel", type=int, default=0)
    parser.add_argument("--text-dilate", type=int, default=3)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--top-colors", type=int, default=8)
    parser.add_argument("--json-output", type=Path, default=None)
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def parse_hex_color(value: str) -> RgbColor:
    cleaned = value.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError(f"Expected #RRGGBB color, got {value}")
    return RgbColor(
        r=int(cleaned[0:2], 16),
        g=int(cleaned[2:4], 16),
        b=int(cleaned[4:6], 16),
    )


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def color_distance(image_rgb: np.ndarray, color: RgbColor) -> np.ndarray:
    target = np.array([color.r, color.g, color.b], dtype=np.float32)
    return np.linalg.norm(image_rgb.astype(np.float32) - target, axis=2)


def dominant_quantized_colors(image_rgb: np.ndarray, top_k: int) -> list[RgbColor]:
    quantized = ((image_rgb.astype(np.uint16) // 8) * 8).astype(np.uint32)
    flat = quantized.reshape((-1, 3))
    packed = flat[:, 0] * 65536 + flat[:, 1] * 256 + flat[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    order = np.argsort(counts)[::-1]
    colors: list[RgbColor] = []
    for index in order[:top_k]:
        value = int(values[index])
        colors.append(
            RgbColor(
                r=(value // 65536) + 4,
                g=((value // 256) % 256) + 4,
                b=(value % 256) + 4,
            )
        )
    return colors


def estimate_background_color(image_rgb: np.ndarray) -> RgbColor:
    border = np.concatenate(
        [
            image_rgb[0, :, :],
            image_rgb[-1, :, :],
            image_rgb[:, 0, :],
            image_rgb[:, -1, :],
        ],
        axis=0,
    )
    quantized = ((border.astype(np.uint16) // 8) * 8).astype(np.uint32)
    packed = quantized[:, 0] * 65536 + quantized[:, 1] * 256 + quantized[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    value = int(values[int(np.argmax(counts))])
    return RgbColor(r=(value // 65536) + 4, g=((value // 256) % 256) + 4, b=(value % 256) + 4)


def make_text_like_mask(
    image_rgb: np.ndarray,
    shape_mask_raw: np.ndarray,
    background_color: RgbColor,
    text_dilate: int,
) -> np.ndarray:
    bg_dist = color_distance(image_rgb, background_color)
    not_background = bg_dist > 24.0
    text_like = np.logical_and(not_background, np.logical_not(shape_mask_raw > 0))
    text_like_u8 = (text_like.astype(np.uint8) * 255)
    if text_dilate > 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (text_dilate, text_dilate))
        text_like_u8 = cv2.dilate(text_like_u8, kernel, iterations=1)
    return text_like_u8


def repair_shape_mask(
    shape_mask_raw: np.ndarray,
    close_kernel_size: int,
    open_kernel_size: int,
) -> np.ndarray:
    mask = shape_mask_raw.copy()
    if close_kernel_size > 0:
        close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_kernel_size, close_kernel_size))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=1)
    if open_kernel_size > 0:
        open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel_size, open_kernel_size))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
    return fill_external_holes(mask)


def seed_components(mask: np.ndarray, open_kernel_size: int, split_erode_kernel_size: int) -> np.ndarray:
    seed = mask.copy()
    if open_kernel_size > 0:
        open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (open_kernel_size, open_kernel_size))
        seed = cv2.morphologyEx(seed, cv2.MORPH_OPEN, open_kernel, iterations=1)
    if split_erode_kernel_size > 0:
        split_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (split_erode_kernel_size, split_erode_kernel_size))
        seed = cv2.erode(seed, split_kernel, iterations=1)
    return seed


def grow_seed_inside_mask(seed: np.ndarray, allowed_mask: np.ndarray, max_iterations: int = 256) -> np.ndarray:
    grown = seed.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    for _ in range(max_iterations):
        expanded = cv2.dilate(grown, kernel, iterations=1)
        expanded = cv2.bitwise_and(expanded, allowed_mask)
        if np.array_equal(expanded, grown):
            return grown
        grown = expanded
    return grown


def partition_raw_mask_by_seed(raw_mask: np.ndarray, seed_labels: np.ndarray, label_count: int) -> tuple[np.ndarray, dict[int, int]]:
    seed_binary = (seed_labels > 0).astype(np.uint8)
    if np.count_nonzero(seed_binary) == 0:
        return np.zeros(raw_mask.shape, dtype=np.int32), {}

    distance_input = np.where(seed_binary > 0, 0, 255).astype(np.uint8)
    _, nearest_seed_component = cv2.distanceTransformWithLabels(
        distance_input,
        cv2.DIST_L2,
        5,
        labelType=cv2.DIST_LABEL_CCOMP,
    )
    label_to_nearest: dict[int, int] = {}
    for label in range(1, label_count):
        y_values, x_values = np.where(seed_labels == label)
        if len(y_values) == 0:
            continue
        label_to_nearest[label] = int(nearest_seed_component[int(y_values[0]), int(x_values[0])])

    partition_labels = np.where(raw_mask > 0, nearest_seed_component, 0).astype(np.int32)
    return partition_labels, label_to_nearest


def repair_partitioned_component(
    raw_mask: np.ndarray,
    partition_labels: np.ndarray,
    partition_label: int,
    close_kernel_size: int,
    open_kernel_size: int,
) -> np.ndarray:
    component_raw = np.where(partition_labels == partition_label, 255, 0).astype(np.uint8)
    points = cv2.findNonZero(component_raw)
    if points is None:
        return component_raw

    x, y, width, height = cv2.boundingRect(points)
    padding = max(close_kernel_size * 2, open_kernel_size * 2, 6)
    x0 = max(0, int(x) - padding)
    y0 = max(0, int(y) - padding)
    x1 = min(raw_mask.shape[1], int(x + width) + padding)
    y1 = min(raw_mask.shape[0], int(y + height) + padding)

    roi = component_raw[y0:y1, x0:x1]
    repaired_roi = repair_shape_mask(roi, close_kernel_size, open_kernel_size)

    output = np.zeros(raw_mask.shape, dtype=np.uint8)
    output[y0:y1, x0:x1] = repaired_roi
    return output

def fill_external_holes(mask: np.ndarray) -> np.ndarray:
    padded = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    h, w = padded.shape
    flood = padded.copy()
    flood_canvas = np.zeros((h + 2, w + 2), dtype=np.uint8)
    cv2.floodFill(flood, flood_canvas, (0, 0), 255)
    outside = flood == 255
    original = padded > 0
    holes = np.logical_not(outside) & np.logical_not(original)
    filled = np.where(original | holes, 255, 0).astype(np.uint8)
    return filled[1:-1, 1:-1]


def contour_to_svg_path(contour: np.ndarray) -> str:
    points = contour.reshape((-1, 2))
    if points.size == 0:
        return ""
    chunks = [f"M {int(points[0][0])} {int(points[0][1])}"]
    for point in points[1:]:
        chunks.append(f"L {int(point[0])} {int(point[1])}")
    chunks.append("Z")
    return " ".join(chunks)


def classify_shape(vertices: int, width: int, height: int, circularity: float, radius: float) -> str:
    aspect = width / max(height, 1)
    if vertices == 3:
        return "triangle"
    if vertices == 4:
        return "square" if 0.9 <= aspect <= 1.1 else "rectangle"
    if circularity > 0.82 and 0.85 <= aspect <= 1.15:
        return "circle"
    if radius > 3 and vertices >= 8:
        return "rounded_rect_or_complex_ui_shape"
    if vertices > 8:
        return "complex_polygon"
    return "polygon"


def estimate_corner_radius(component_mask: np.ndarray, x: int, y: int, width: int, height: int) -> float:
    roi = component_mask[y : y + height, x : x + width]
    if roi.size == 0:
        return 0.0
    distance = cv2.distanceTransform(roi, cv2.DIST_L2, 5)
    # On rounded UI shapes, the largest inscribed corner-ish distance is a reasonable radius proxy.
    return round(float(np.percentile(distance[distance > 0], 92)) if np.any(distance > 0) else 0.0, 2)


def detect_color_shapes(
    image_rgb: np.ndarray,
    color: RgbColor,
    background_color: RgbColor,
    args: argparse.Namespace,
    layer: int,
) -> tuple[list[ShapeCandidate], np.ndarray, np.ndarray]:
    dist = color_distance(image_rgb, color)
    raw_mask = (dist <= args.color_distance).astype(np.uint8) * 255
    text_mask = make_text_like_mask(image_rgb, raw_mask, background_color, args.text_dilate)
    seed_mask = seed_components(raw_mask, args.open_kernel, args.split_erode_kernel)
    label_count, seed_labels, stats, _ = cv2.connectedComponentsWithStats(seed_mask, connectivity=8)

    partition_labels, label_to_partition = partition_raw_mask_by_seed(raw_mask, seed_labels, label_count)
    repaired_mask = np.zeros(raw_mask.shape, dtype=np.uint8)
    candidates: list[ShapeCandidate] = []
    next_id = 1

    for label in range(1, label_count):
        if int(stats[label, cv2.CC_STAT_AREA]) < args.min_area:
            continue
        partition_label = label_to_partition.get(label)
        if partition_label is None:
            continue

        component_repaired = repair_partitioned_component(
            raw_mask=raw_mask,
            partition_labels=partition_labels,
            partition_label=partition_label,
            close_kernel_size=args.close_kernel,
            open_kernel_size=args.open_kernel,
        )
        repaired_mask = cv2.bitwise_or(repaired_mask, component_repaired)
        contours, _ = cv2.findContours(component_repaired, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in sorted(contours, key=cv2.contourArea, reverse=True):
            area = float(cv2.contourArea(contour))
            if area < args.min_area:
                continue
            x, y, width, height = cv2.boundingRect(contour)
            component_mask = np.zeros(repaired_mask.shape, dtype=np.uint8)
            cv2.drawContours(component_mask, [contour], -1, 255, thickness=-1)
            component_pixels = int(np.count_nonzero(component_mask))
            if component_pixels < args.min_area:
                continue

            perimeter = float(cv2.arcLength(contour, True))
            epsilon = 0.012 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            hull = cv2.convexHull(contour)
            hull_area = max(float(cv2.contourArea(hull)), 1.0)
            circularity = 0.0 if perimeter == 0 else float(4.0 * np.pi * area / (perimeter * perimeter))
            solidity = float(area / hull_area)
            extent = float(area / max(width * height, 1))
            radius = estimate_corner_radius(component_mask, x, y, width, height)
            text_overlap = int(np.count_nonzero(cv2.bitwise_and(component_mask, text_mask)))
            text_overlap_ratio = float(text_overlap / max(component_pixels, 1))
            kind = classify_shape(len(approx), width, height, circularity, radius)
            confidence = min(1.0, 0.35 + 0.35 * solidity + 0.2 * extent + 0.1 * min(area / 5000.0, 1.0))
            candidates.append(
                ShapeCandidate(
                    id=next_id,
                    layer=layer,
                    color=color.hex,
                    kind=kind,
                    x=int(x),
                    y=int(y),
                    width=int(width),
                    height=int(height),
                    area_pixels=component_pixels,
                    contour_area=round(area, 2),
                    perimeter=round(perimeter, 2),
                    vertices=len(approx),
                    circularity=round(circularity, 4),
                    solidity=round(solidity, 4),
                    extent=round(extent, 4),
                    estimated_radius=radius,
                    text_overlap_ratio=round(text_overlap_ratio, 4),
                    confidence=round(confidence, 4),
                    svg_path=contour_to_svg_path(approx),
                )
            )
            next_id += 1

    if not candidates:
        repaired_mask = repair_shape_mask(raw_mask, args.close_kernel, args.open_kernel)

    return candidates, raw_mask, repaired_mask

def candidate_center(candidate: ShapeCandidate) -> tuple[float, float]:
    return (candidate.x + candidate.width / 2.0, candidate.y + candidate.height / 2.0)


def bbox_contains_point(candidate: ShapeCandidate, point: tuple[float, float]) -> bool:
    px, py = point
    return candidate.x <= px <= candidate.x + candidate.width and candidate.y <= py <= candidate.y + candidate.height


def select_frontmost_candidates(candidates: list[ShapeCandidate]) -> list[ShapeCandidate]:
    if len(candidates) < 2:
        return candidates

    container_ids: set[int] = set()
    for candidate in candidates:
        for other in candidates:
            if candidate.id == other.id:
                continue
            if other.area_pixels >= candidate.area_pixels * 0.45:
                continue
            if bbox_contains_point(candidate, candidate_center(other)):
                container_ids.add(candidate.id)
                break

    frontmost = [candidate for candidate in candidates if candidate.id not in container_ids]
    return frontmost if frontmost else candidates

def draw_overlay(image_rgb: np.ndarray, candidates: list[ShapeCandidate]) -> np.ndarray:
    overlay = image_rgb.copy()
    for candidate in candidates:
        color = (60, 230, 120)
        cv2.rectangle(
            overlay,
            (candidate.x, candidate.y),
            (candidate.x + candidate.width, candidate.y + candidate.height),
            color,
            1,
        )
        cv2.putText(
            overlay,
            f"{candidate.id}:{candidate.kind}",
            (candidate.x, max(10, candidate.y - 3)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.32,
            color,
            1,
            cv2.LINE_AA,
        )
    return overlay


def save_mask(path: Path, mask: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), mask)


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    out_dir = resolve_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    image_rgb = load_rgb(image_path)

    background_color = parse_hex_color(args.background_color) if args.background_color else estimate_background_color(image_rgb)
    if args.shape_color:
        colors = [parse_hex_color(args.shape_color)]
    else:
        colors = []
        for color in dominant_quantized_colors(image_rgb, args.top_colors):
            if np.linalg.norm(np.array([color.r, color.g, color.b]) - np.array([background_color.r, background_color.g, background_color.b])) > 40:
                colors.append(color)

    all_candidates: list[ShapeCandidate] = []
    debug_colors: list[dict[str, str]] = []
    for layer in range(args.layers):
        layer_candidates: list[ShapeCandidate] = []
        for color in colors:
            candidates, raw_mask, repaired_mask = detect_color_shapes(image_rgb, color, background_color, args, layer + 1)
            layer_candidates.extend(candidates)
            save_mask(out_dir.joinpath(f"layer_{layer + 1}_{color.hex.lstrip('#')}_raw_mask.png"), raw_mask)
            save_mask(out_dir.joinpath(f"layer_{layer + 1}_{color.hex.lstrip('#')}_repaired_mask.png"), repaired_mask)
            debug_colors.append({"layer": str(layer + 1), "color": color.hex})
        selected_candidates = layer_candidates
        if layer + 1 < args.layers:
            selected_candidates = select_frontmost_candidates(layer_candidates)
        all_candidates.extend(selected_candidates)
        if not selected_candidates:
            break
        # Remove detected shape-colored pixels from later layers. This peels frontmost same-color shapes first.
        for candidate in selected_candidates:
            component = np.zeros(image_rgb.shape[:2], dtype=np.uint8)
            path_points = []
            tokens = candidate.svg_path.split()
            for index, token in enumerate(tokens):
                if token in {"M", "L"} and index + 2 < len(tokens):
                    path_points.append([int(tokens[index + 1]), int(tokens[index + 2])])
            if len(path_points) >= 3:
                cv2.fillPoly(component, [np.array(path_points, dtype=np.int32)], 255)
                image_rgb[component > 0] = np.array([background_color.r, background_color.g, background_color.b], dtype=np.uint8)

    for index, candidate in enumerate(all_candidates, start=1):
        candidate.id = index

    overlay = draw_overlay(load_rgb(image_path), all_candidates)
    cv2.imwrite(str(out_dir.joinpath("detected_shapes_overlay.png")), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    payload = {
        "image": str(image_path),
        "background_color": background_color.hex,
        "searched_colors": debug_colors,
        "shape_count": len(all_candidates),
        "docling_available": importlib.util.find_spec("docling") is not None,
        "shapes": [asdict(candidate) for candidate in all_candidates],
        "notes": [
            "Text-like pixels are masked as non-background pixels that are not close to the active shape color.",
            "Shape masks are morphologically closed and hole-filled to bridge text occlusions.",
            "Docling is reported in docling_available; when unavailable, this run uses deterministic OpenCV flat-color geometry.",
        ],
    }
    output_path = resolve_path(args.json_output) if args.json_output else out_dir.joinpath("detected_shapes.json")
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())









