from __future__ import annotations

import argparse
import html
import io
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cairosvg
import cv2
import numpy as np
from PIL import Image


@dataclass(slots=True)
class FitResult:
    shape_id: int
    layer: int
    color: str
    kind: str
    fit_kind: str
    score_iou: float
    score_soft_mae: float
    diff_pixels: int
    target_pixels: int
    candidate_pixels: int
    svg_element: str
    debug_svg_element: str
    params: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fit clean rounded SVG primitives to detected shape masks.")
    parser.add_argument("detected_json", type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--max-radius", type=float, default=28.0)
    parser.add_argument("--radius-step", type=float, default=1.0)
    parser.add_argument("--rect-adjust", type=int, default=3)
    parser.add_argument("--width-adjust", type=int, default=4)
    parser.add_argument("--height-adjust", type=int, default=4)
    parser.add_argument("--min-component-area", type=int, default=40)
    parser.add_argument("--simplicity-iou-tolerance", type=float, default=0.007)
    parser.add_argument("--preferred-radius", type=float, default=8.0)
    parser.add_argument("--soft-edge-scale", type=int, default=4)
    parser.add_argument("--disable-soft-score", action="store_true")
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_hex_rgb(value: str) -> np.ndarray:
    cleaned = value.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError(f"Expected #RRGGBB color, got {value}")
    return np.array(
        [int(cleaned[0:2], 16), int(cleaned[2:4], 16), int(cleaned[4:6], 16)],
        dtype=np.float32,
    )


def load_source_rgb(payload: dict[str, Any]) -> np.ndarray | None:
    image_value = payload.get("image")
    if not isinstance(image_value, str) or not image_value:
        return None
    image_path = resolve_path(Path(image_value))
    if not image_path.exists():
        return None
    return np.array(Image.open(image_path).convert("RGB"), dtype=np.float32)


def soft_alpha_target(
    image_rgb: np.ndarray | None,
    component_mask: np.ndarray,
    foreground_color: str,
    background_color: str,
) -> np.ndarray | None:
    if image_rgb is None:
        return None
    foreground = parse_hex_rgb(foreground_color)
    background = parse_hex_rgb(background_color)
    direction = foreground - background
    denominator = float(np.dot(direction, direction))
    if denominator <= 1e-6:
        return None

    projected = np.tensordot(image_rgb - background, direction, axes=([2], [0])) / denominator
    projected = np.clip(projected, 0.0, 1.0).astype(np.float32)

    hard = component_mask > 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.dilate(hard.astype(np.uint8), kernel, iterations=1) > 0
    eroded = cv2.erode(hard.astype(np.uint8), kernel, iterations=1) > 0
    edge_band = dilated & ~eroded

    target = hard.astype(np.float32)
    target[edge_band] = projected[edge_band]
    target[~dilated] = 0.0
    return target

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


def layer_mask_path(json_path: Path, shape: dict[str, Any]) -> Path:
    layer = int(shape.get("layer", 1))
    color = str(shape.get("color", "#000000")).lstrip("#")
    return json_path.parent.joinpath(f"layer_{layer}_{color}_repaired_mask.png")


def bbox_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    x0 = max(ax, bx)
    y0 = max(ay, by)
    x1 = min(ax + aw, bx + bw)
    y1 = min(ay + ah, by + bh)
    return max(0, x1 - x0) * max(0, y1 - y0)


def fallback_polygon_mask(shape: dict[str, Any], width: int, height: int) -> np.ndarray:
    tokens = str(shape.get("svg_path", "")).split()
    points: list[list[int]] = []
    for index, token in enumerate(tokens):
        if token in {"M", "L"} and index + 2 < len(tokens):
            points.append([int(float(tokens[index + 1])), int(float(tokens[index + 2]))])
    mask = np.zeros((height, width), dtype=np.uint8)
    if len(points) >= 3:
        cv2.fillPoly(mask, [np.array(points, dtype=np.int32)], 255)
    return mask


def component_mask_for_shape(json_path: Path, shape: dict[str, Any], width: int, height: int, min_area: int) -> np.ndarray:
    mask_path = layer_mask_path(json_path, shape)
    if not mask_path.exists():
        return fallback_polygon_mask(shape, width, height)

    layer_mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
    if layer_mask is None:
        return fallback_polygon_mask(shape, width, height)

    _, binary = cv2.threshold(layer_mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    shape_bbox = (
        int(shape.get("x", 0)),
        int(shape.get("y", 0)),
        int(shape.get("width", 0)),
        int(shape.get("height", 0)),
    )
    best_contour = None
    best_score = -1
    for contour in contours:
        area = int(cv2.contourArea(contour))
        if area < min_area:
            continue
        bbox = cv2.boundingRect(contour)
        overlap = bbox_overlap(shape_bbox, bbox)
        shape_box_area = max(shape_bbox[2] * shape_bbox[3], 1)
        contour_box_area = max(bbox[2] * bbox[3], 1)
        overlap_ratio = overlap / shape_box_area
        bbox_size_penalty = abs(math.log(max(contour_box_area / shape_box_area, 1e-6)))
        area_size_penalty = abs(math.log(max(area / max(int(shape.get("area_pixels", shape_box_area)), 1), 1e-6)))
        score = overlap_ratio * 1000 - bbox_size_penalty * 180 - area_size_penalty * 40
        if score > best_score:
            best_score = score
            best_contour = contour

    if best_contour is None:
        return fallback_polygon_mask(shape, width, height)

    component = np.zeros((height, width), dtype=np.uint8)
    cv2.drawContours(component, [best_contour], -1, 255, thickness=-1)
    return component


def mask_bbox(mask: np.ndarray) -> tuple[int, int, int, int]:
    points = cv2.findNonZero(mask)
    if points is None:
        return (0, 0, 1, 1)
    return cv2.boundingRect(points)


def svg_document(width: int, height: int, element: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="black"/>'
        f'{element}'
        '</svg>'
    )


def render_element_mask(width: int, height: int, element: str) -> np.ndarray:
    svg = svg_document(width, height, element)
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=width, output_height=height)
    image = Image.open(io.BytesIO(png)).convert("L")
    return (np.array(image) > 127).astype(np.uint8) * 255


def render_element_alpha(width: int, height: int, element: str, scale: int) -> np.ndarray:
    scale = max(1, int(scale))
    svg = svg_document(width, height, element)
    png = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=width * scale,
        output_height=height * scale,
    )
    image = Image.open(io.BytesIO(png)).convert("L")
    if scale != 1:
        image = image.resize((width, height), Image.Resampling.LANCZOS)
    return np.array(image, dtype=np.float32) / 255.0


def score_soft_alpha(target_alpha: np.ndarray | None, candidate_alpha: np.ndarray) -> float:
    if target_alpha is None:
        return 1.0
    focus = (target_alpha > 0.01) | (candidate_alpha > 0.01)
    if not np.any(focus):
        return 1.0
    return float(np.mean(np.abs(target_alpha[focus] - candidate_alpha[focus])))

def score_mask(target: np.ndarray, candidate: np.ndarray) -> tuple[float, int, int, int]:
    target_bool = target > 0
    candidate_bool = candidate > 0
    intersection = int(np.count_nonzero(target_bool & candidate_bool))
    union = int(np.count_nonzero(target_bool | candidate_bool))
    diff = int(np.count_nonzero(target_bool ^ candidate_bool))
    target_pixels = int(np.count_nonzero(target_bool))
    candidate_pixels = int(np.count_nonzero(candidate_bool))
    iou = 0.0 if union == 0 else intersection / union
    return iou, diff, target_pixels, candidate_pixels


def rect_element(x: float, y: float, width: float, height: float, rx: float, color: str = "white") -> str:
    return (
        f'<rect x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" height="{height:.3f}" '
        f'rx="{rx:.3f}" ry="{rx:.3f}" fill="{html.escape(color)}"/>'
    )


def path_element(path_data: str, color: str = "white") -> str:
    return f'<path d="{html.escape(path_data)}" fill="{html.escape(color)}"/>'


def rounded_rect_mask(canvas_width: int, canvas_height: int, x: int, y: int, width: int, height: int, radius: float) -> np.ndarray:
    mask = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
    x0 = int(round(x))
    y0 = int(round(y))
    x1 = int(round(x + width))
    y1 = int(round(y + height))
    r = int(round(min(radius, width / 2.0, height / 2.0)))
    if width <= 0 or height <= 0:
        return mask
    if r <= 0:
        cv2.rectangle(mask, (x0, y0), (x1, y1), 255, thickness=-1)
        return mask

    cv2.rectangle(mask, (x0 + r, y0), (x1 - r, y1), 255, thickness=-1)
    cv2.rectangle(mask, (x0, y0 + r), (x1, y1 - r), 255, thickness=-1)
    cv2.circle(mask, (x0 + r, y0 + r), r, 255, thickness=-1)
    cv2.circle(mask, (x1 - r, y0 + r), r, 255, thickness=-1)
    cv2.circle(mask, (x1 - r, y1 - r), r, 255, thickness=-1)
    cv2.circle(mask, (x0 + r, y1 - r), r, 255, thickness=-1)
    return mask

def fit_rounded_rect(target: np.ndarray, width: int, height: int, args: argparse.Namespace) -> tuple[float, str, dict[str, Any], int, int, int]:
    x, y, w, h = mask_bbox(target)
    best: tuple[float, str, dict[str, Any], int, int, int] | None = None
    max_radius = min(args.max_radius, max(0.0, min(w, h) / 2.0))
    radius_values = np.arange(0.0, max_radius + 0.001, args.radius_step)
    for dx in range(-args.rect_adjust, args.rect_adjust + 1):
        for dy in range(-args.rect_adjust, args.rect_adjust + 1):
            for dw in range(-args.width_adjust, args.width_adjust + 1):
                for dh in range(-args.height_adjust, args.height_adjust + 1):
                    candidate_x = x + dx
                    candidate_y = y + dy
                    candidate_w = max(1, w + dw)
                    candidate_h = max(1, h + dh)
                    for radius in radius_values:
                        radius_clamped = min(float(radius), candidate_w / 2.0, candidate_h / 2.0)
                        element = rect_element(candidate_x, candidate_y, candidate_w, candidate_h, radius_clamped)
                        candidate_mask = rounded_rect_mask(width, height, candidate_x, candidate_y, candidate_w, candidate_h, radius_clamped)
                        iou, diff, target_pixels, candidate_pixels = score_mask(target, candidate_mask)
                        params = {
                            "x": candidate_x,
                            "y": candidate_y,
                            "width": candidate_w,
                            "height": candidate_h,
                            "rx": round(radius_clamped, 3),
                            "ry": round(radius_clamped, 3),
                        }
                        result = (iou, element, params, diff, target_pixels, candidate_pixels)
                        if best is None or iou > best[0] or (math.isclose(iou, best[0]) and diff < best[3]):
                            best = result
    assert best is not None
    return best


def contour_points(target: np.ndarray, epsilon_factor: float) -> np.ndarray:
    contours, _ = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return np.zeros((0, 2), dtype=np.float32)
    contour = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon_factor * perimeter, True)
    return approx.reshape((-1, 2)).astype(np.float32)


def rounded_polygon_path(points: np.ndarray, radius: float) -> str:
    if len(points) < 3:
        return ""
    if radius <= 0:
        chunks = [f"M {points[0][0]:.3f} {points[0][1]:.3f}"]
        for point in points[1:]:
            chunks.append(f"L {point[0]:.3f} {point[1]:.3f}")
        chunks.append("Z")
        return " ".join(chunks)

    in_points: list[np.ndarray] = []
    out_points: list[np.ndarray] = []
    count = len(points)
    for index in range(count):
        previous_point = points[(index - 1) % count]
        point = points[index]
        next_point = points[(index + 1) % count]
        previous_vector = previous_point - point
        next_vector = next_point - point
        previous_length = max(float(np.linalg.norm(previous_vector)), 1e-6)
        next_length = max(float(np.linalg.norm(next_vector)), 1e-6)
        distance = min(radius, previous_length * 0.48, next_length * 0.48)
        in_points.append(point + previous_vector / previous_length * distance)
        out_points.append(point + next_vector / next_length * distance)

    chunks = [f"M {out_points[0][0]:.3f} {out_points[0][1]:.3f}"]
    for index in range(1, count):
        point = points[index]
        in_point = in_points[index]
        out_point = out_points[index]
        chunks.append(f"L {in_point[0]:.3f} {in_point[1]:.3f}")
        control_1 = in_point + (point - in_point) * 0.55
        control_2 = out_point + (point - out_point) * 0.55
        chunks.append(f"C {control_1[0]:.3f} {control_1[1]:.3f} {control_2[0]:.3f} {control_2[1]:.3f} {out_point[0]:.3f} {out_point[1]:.3f}")
    chunks.append(f"L {in_points[0][0]:.3f} {in_points[0][1]:.3f}")
    control_1 = in_points[0] + (points[0] - in_points[0]) * 0.55
    control_2 = out_points[0] + (points[0] - out_points[0]) * 0.55
    chunks.append(f"C {control_1[0]:.3f} {control_1[1]:.3f} {control_2[0]:.3f} {control_2[1]:.3f} {out_points[0][0]:.3f} {out_points[0][1]:.3f}")
    chunks.append("Z")
    return " ".join(chunks)


def rounded_polygon_path_with_corner_radii(points: np.ndarray, radii: list[float]) -> str:
    if len(points) < 3:
        return ""

    in_points: list[np.ndarray] = []
    out_points: list[np.ndarray] = []
    count = len(points)
    for index in range(count):
        previous_point = points[(index - 1) % count]
        point = points[index]
        next_point = points[(index + 1) % count]
        previous_vector = previous_point - point
        next_vector = next_point - point
        previous_length = max(float(np.linalg.norm(previous_vector)), 1e-6)
        next_length = max(float(np.linalg.norm(next_vector)), 1e-6)
        radius = max(0.0, float(radii[index]))
        distance = min(radius, previous_length * 0.48, next_length * 0.48)
        in_points.append(point + previous_vector / previous_length * distance)
        out_points.append(point + next_vector / next_length * distance)

    chunks: list[str] = []
    first = out_points[0] if radii[0] > 0 else points[0]
    chunks.append(f"M {first[0]:.3f} {first[1]:.3f}")
    for index in range(1, count):
        point = points[index]
        if radii[index] <= 0:
            chunks.append(f"L {point[0]:.3f} {point[1]:.3f}")
            continue
        in_point = in_points[index]
        out_point = out_points[index]
        chunks.append(f"L {in_point[0]:.3f} {in_point[1]:.3f}")
        control_1 = in_point + (point - in_point) * 0.55
        control_2 = out_point + (point - out_point) * 0.55
        chunks.append(f"C {control_1[0]:.3f} {control_1[1]:.3f} {control_2[0]:.3f} {control_2[1]:.3f} {out_point[0]:.3f} {out_point[1]:.3f}")
    if radii[0] <= 0:
        chunks.append("Z")
        return " ".join(chunks)
    chunks.append(f"L {in_points[0][0]:.3f} {in_points[0][1]:.3f}")
    control_1 = in_points[0] + (points[0] - in_points[0]) * 0.55
    control_2 = out_points[0] + (points[0] - out_points[0]) * 0.55
    chunks.append(f"C {control_1[0]:.3f} {control_1[1]:.3f} {control_2[0]:.3f} {control_2[1]:.3f} {out_points[0][0]:.3f} {out_points[0][1]:.3f}")
    chunks.append("Z")
    return " ".join(chunks)


def score_polygon_path(
    target: np.ndarray,
    canvas_width: int,
    canvas_height: int,
    path_data: str,
    params: dict[str, Any],
) -> tuple[float, str, dict[str, Any], int, int, int]:
    element = path_element(path_data)
    candidate_mask = render_element_mask(canvas_width, canvas_height, element)
    iou, diff, target_pixels, candidate_pixels = score_mask(target, candidate_mask)
    return iou, element, params, diff, target_pixels, candidate_pixels


def fit_variable_corner_polygon(
    target: np.ndarray,
    width: int,
    height: int,
    args: argparse.Namespace,
    epsilon: float,
) -> tuple[float, str, dict[str, Any], int, int, int] | None:
    points = contour_points(target, epsilon)
    if len(points) < 3 or len(points) > 24:
        return None

    max_radius = min(float(args.max_radius), 10.0)
    radius_values = sorted({0.0, 1.0, 2.0, 3.0, float(args.preferred_radius), max_radius})
    radius_values = [value for value in radius_values if 0.0 <= value <= max_radius]
    radii = [float(args.preferred_radius)] * len(points)

    def evaluate(current_radii: list[float]) -> tuple[float, str, dict[str, Any], int, int, int]:
        path_data = rounded_polygon_path_with_corner_radii(points, current_radii)
        params = {
            "epsilon_factor": epsilon,
            "corner_radii": [round(value, 3) for value in current_radii],
            "vertices": int(len(points)),
            "path": path_data,
        }
        return score_polygon_path(target, width, height, path_data, params)

    best = evaluate(radii)
    for _ in range(2):
        changed = False
        for index in range(len(radii)):
            local_best = best
            local_radius = radii[index]
            for radius in radius_values:
                trial = radii.copy()
                trial[index] = radius
                candidate = evaluate(trial)
                if candidate[0] > local_best[0] or (math.isclose(candidate[0], local_best[0]) and candidate[3] < local_best[3]):
                    local_best = candidate
                    local_radius = radius
            if local_radius != radii[index]:
                radii[index] = local_radius
                best = local_best
                changed = True
        if not changed:
            break
    return best

def fit_rounded_polygon(target: np.ndarray, target_soft: np.ndarray | None, width: int, height: int, args: argparse.Namespace) -> tuple[float, str, dict[str, Any], int, int, int]:
    candidates: list[tuple[float, str, dict[str, Any], int, int, int]] = []
    epsilon_values = [0.004, 0.007, 0.01, 0.014, 0.02, 0.03, 0.045, 0.06]
    radius_values = np.arange(0.0, args.max_radius + 0.001, args.radius_step)
    for epsilon in epsilon_values:
        points = contour_points(target, epsilon)
        if len(points) < 3:
            continue
        for radius in radius_values:
            path_data = rounded_polygon_path(points, float(radius))
            if not path_data:
                continue
            element = path_element(path_data)
            candidate_mask = render_element_mask(width, height, element)
            iou, diff, target_pixels, candidate_pixels = score_mask(target, candidate_mask)
            params = {
                "epsilon_factor": epsilon,
                "radius": round(float(radius), 3),
                "vertices": int(len(points)),
                "path": path_data,
            }
            candidates.append((iou, element, params, diff, target_pixels, candidate_pixels))

    for epsilon in [0.004, 0.007]:
        variable_candidate = fit_variable_corner_polygon(target, width, height, args, epsilon)
        if variable_candidate is not None:
            candidates.append(variable_candidate)

    if not candidates:
        empty_element = path_element("")
        return 0.0, empty_element, {}, int(np.count_nonzero(target)), int(np.count_nonzero(target)), 0

    highest_iou = max(candidate[0] for candidate in candidates)
    eligible = [candidate for candidate in candidates if candidate[0] >= highest_iou - args.simplicity_iou_tolerance]

    def corner_smoothness(params: dict[str, Any]) -> float:
        preferred = max(float(args.preferred_radius), 1.0)
        if "corner_radii" in params:
            radii = [float(value) for value in params.get("corner_radii", [])]
        else:
            vertices = int(params.get("vertices", 0))
            radii = [float(params.get("radius", 0.0))] * vertices
        if not radii:
            return 0.0
        return sum(min(max(radius, 0.0), preferred) / preferred for radius in radii) / len(radii)

    def design_rank(candidate: tuple[float, str, dict[str, Any], int, int, int]) -> tuple[int, float, float, int]:
        iou, _, params, diff, _, _ = candidate
        vertices = int(params.get("vertices", 999))
        # Inside the IoU tolerance, prefer cleaner and visibly rounded design intent over pixel-hugging corners.
        return (vertices, -corner_smoothness(params), -iou, diff)

    return min(eligible, key=design_rank)

def fit_shape(
    json_path: Path,
    shape: dict[str, Any],
    width: int,
    height: int,
    image_rgb: np.ndarray | None,
    background: str,
    args: argparse.Namespace,
) -> FitResult:
    target = component_mask_for_shape(json_path, shape, width, height, args.min_component_area)
    color = str(shape.get("color", "#000000"))
    target_soft = soft_alpha_target(image_rgb, target, color, background)
    rect_fit = fit_rounded_rect(target, width, height, args)
    polygon_fit = fit_rounded_polygon(target, target_soft, width, height, args)
    best_kind = "rounded_rect"
    best_fit = rect_fit
    if polygon_fit[0] > rect_fit[0] + 0.002:
        best_kind = "rounded_polygon"
        best_fit = polygon_fit

    iou, element, params, diff, target_pixels, candidate_pixels = best_fit
    clean_element = element.replace('fill="white"', f'fill="{html.escape(color)}"')
    stroke = "#FF2E88" if best_kind == "rounded_polygon" else "#00A8FF"
    debug_element = clean_element.replace("/>", f' fill-opacity="0.72" stroke="{stroke}" stroke-width="1.5"/>')
    candidate_alpha = render_element_alpha(width, height, element, args.soft_edge_scale)
    soft_mae = score_soft_alpha(target_soft, candidate_alpha)
    return FitResult(
        shape_id=int(shape.get("id", 0)),
        layer=int(shape.get("layer", 1)),
        color=color,
        kind=str(shape.get("kind", "shape")),
        fit_kind=best_kind,
        score_iou=round(float(iou), 6),
        score_soft_mae=round(float(soft_mae), 6),
        diff_pixels=int(diff),
        target_pixels=int(target_pixels),
        candidate_pixels=int(candidate_pixels),
        svg_element=clean_element,
        debug_svg_element=debug_element,
        params=params,
    )

def output_svg(width: int, height: int, background: str, fits: list[FitResult], debug: bool) -> str:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <rect width="100%" height="100%" fill="{html.escape(background)}"/>',
        '  <g id="fitted-shapes">',
    ]
    for fit in sorted(fits, key=lambda item: (-item.layer, -item.target_pixels)):
        lines.append("    " + (fit.debug_svg_element if debug else fit.svg_element))
        if debug:
            x_value = int(fit.params.get("x", 4)) if fit.fit_kind == "rounded_rect" else 4
            y_value = int(fit.params.get("y", 12)) if fit.fit_kind == "rounded_rect" else 12 + fit.shape_id * 10
            label = f"#{fit.shape_id} L{fit.layer} {fit.fit_kind} IoU={fit.score_iou}"
            lines.append(
                f'    <text x="{x_value}" y="{y_value}" font-family="monospace" font-size="8" fill="#111" '
                f'stroke="#fff" stroke-width="0.8" paint-order="stroke">{html.escape(label)}</text>'
            )
    lines.extend(["  </g>", "</svg>", ""])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    json_path = resolve_path(args.detected_json)
    payload = load_json(json_path)
    shapes = list(payload.get("shapes", []))
    width, height = image_size(payload, shapes)
    out_dir = resolve_path(args.out_dir) if args.out_dir else json_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    background = str(payload.get("background_color", "#FFFFFF"))
    image_rgb = load_source_rgb(payload)
    fits = [fit_shape(json_path, shape, width, height, image_rgb, background, args) for shape in shapes]
    out_dir.joinpath("fitted_shapes.svg").write_text(output_svg(width, height, background, fits, debug=False), encoding="utf-8")
    out_dir.joinpath("fitted_shapes_debug.svg").write_text(output_svg(width, height, background, fits, debug=True), encoding="utf-8")
    report = {
        "source": str(json_path),
        "width": width,
        "height": height,
        "shape_count": len(fits),
        "fits": [asdict(fit) for fit in fits],
    }
    out_dir.joinpath("fitted_shapes_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())













