from __future__ import annotations

import argparse
import html
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw


@dataclass(slots=True)
class FlatRegion:
    id: int
    color: str
    x: int
    y: int
    width: int
    height: int
    area_pixels: int
    bbox_area: int
    extent: float
    mean_lab_std: float
    mean_edge_density: float
    mean_entropy: float
    superpixel_count: int
    confidence: float
    vertices: int
    solidity: float
    boundary_complexity: float
    is_text_like: bool
    region_class: str
    svg_path: str


@dataclass(slots=True)
class SuperpixelStats:
    label: int
    area: int
    mean_rgb: tuple[float, float, float]
    rgb_std: float
    lab_std: float
    edge_density: float
    entropy: float
    is_background: bool
    is_flat: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect unicolored/flat vector-like regions separately from textured image regions.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--region-size", type=int, default=14)
    parser.add_argument("--ruler", type=float, default=12.0)
    parser.add_argument("--min-region-area", type=int, default=1200)
    parser.add_argument("--min-superpixel-area", type=int, default=20)
    parser.add_argument("--max-lab-std", type=float, default=9.0)
    parser.add_argument("--max-rgb-std", type=float, default=13.0)
    parser.add_argument("--max-edge-density", type=float, default=0.12)
    parser.add_argument("--max-entropy", type=float, default=2.2)
    parser.add_argument("--background-distance", type=float, default=18.0)
    parser.add_argument("--color-bin-size", type=int, default=16)
    parser.add_argument("--close-kernel", type=int, default=3)
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def rgb_to_hex(rgb: tuple[float, float, float] | np.ndarray) -> str:
    values = [int(round(float(value))) for value in rgb]
    values = [max(0, min(255, value)) for value in values]
    return f"#{values[0]:02X}{values[1]:02X}{values[2]:02X}"


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def estimate_background(image_rgb: np.ndarray) -> np.ndarray:
    border = np.concatenate(
        [image_rgb[0, :, :], image_rgb[-1, :, :], image_rgb[:, 0, :], image_rgb[:, -1, :]],
        axis=0,
    )
    quantized = ((border.astype(np.uint16) // 8) * 8).astype(np.uint32)
    packed = quantized[:, 0] * 65536 + quantized[:, 1] * 256 + quantized[:, 2]
    values, counts = np.unique(packed, return_counts=True)
    value = int(values[int(np.argmax(counts))])
    return np.array([(value // 65536) + 4, ((value // 256) % 256) + 4, (value % 256) + 4], dtype=np.float32)


def slic_labels(image_rgb: np.ndarray, region_size: int, ruler: float) -> np.ndarray:
    if not hasattr(cv2, "ximgproc"):
        raise RuntimeError("OpenCV ximgproc is required for SLIC superpixels in this environment.")
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    slic = cv2.ximgproc.createSuperpixelSLIC(image_bgr, algorithm=cv2.ximgproc.SLICO, region_size=region_size, ruler=float(ruler))
    slic.iterate(10)
    slic.enforceLabelConnectivity(min_element_size=20)
    return slic.getLabels().astype(np.int32)


def local_entropy(gray: np.ndarray) -> np.ndarray:
    entropy = np.zeros(gray.shape, dtype=np.float32)
    padded = cv2.copyMakeBorder(gray, 2, 2, 2, 2, cv2.BORDER_REFLECT)
    for y in range(gray.shape[0]):
        for x in range(gray.shape[1]):
            patch = padded[y : y + 5, x : x + 5]
            hist = np.bincount((patch // 16).reshape(-1), minlength=16).astype(np.float32)
            prob = hist / max(float(np.sum(hist)), 1.0)
            nonzero = prob > 0
            entropy[y, x] = float(-np.sum(prob[nonzero] * np.log2(prob[nonzero])))
    return entropy


def compute_superpixel_stats(image_rgb: np.ndarray, labels: np.ndarray, args: argparse.Namespace) -> tuple[list[SuperpixelStats], np.ndarray, np.ndarray]:
    background = estimate_background(image_rgb)
    image_lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 120) > 0
    entropy_image = local_entropy(gray)

    stats: list[SuperpixelStats] = []
    for label in range(int(labels.max()) + 1):
        mask = labels == label
        area = int(np.count_nonzero(mask))
        if area == 0:
            continue
        rgb_values = image_rgb[mask].astype(np.float32)
        lab_values = image_lab[mask].astype(np.float32)
        mean_rgb = tuple(float(value) for value in np.mean(rgb_values, axis=0))
        rgb_std = float(np.mean(np.std(rgb_values, axis=0)))
        lab_std = float(np.mean(np.std(lab_values, axis=0)))
        edge_density = float(np.count_nonzero(edges[mask]) / area)
        entropy = float(np.mean(entropy_image[mask]))
        bg_distance = float(np.linalg.norm(np.array(mean_rgb, dtype=np.float32) - background))
        is_background = bg_distance <= args.background_distance
        is_flat = (
            area >= args.min_superpixel_area
            and not is_background
            and lab_std <= args.max_lab_std
            and rgb_std <= args.max_rgb_std
            and edge_density <= args.max_edge_density
            and entropy <= args.max_entropy
        )
        stats.append(
            SuperpixelStats(
                label=label,
                area=area,
                mean_rgb=mean_rgb,
                rgb_std=round(rgb_std, 4),
                lab_std=round(lab_std, 4),
                edge_density=round(edge_density, 4),
                entropy=round(entropy, 4),
                is_background=is_background,
                is_flat=is_flat,
            )
        )
    return stats, edges.astype(np.uint8) * 255, entropy_image


def color_bin(rgb: tuple[float, float, float], bin_size: int) -> tuple[int, int, int]:
    return tuple(int(round(float(value) / bin_size) * bin_size) for value in rgb)


def contour_to_svg_path(contour: np.ndarray) -> str:
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


def is_text_like_region(width: int, height: int, area_pixels: int, vertices: int, boundary_complexity: float) -> bool:
    aspect = width / max(float(height), 1.0)
    compact_glyph_run = height <= 44 and width >= 30 and aspect >= 2.2 and vertices >= 10
    tiny_many_edges = height <= 32 and area_pixels <= 2500 and vertices >= 12
    small_irregular_mark = height <= 60 and width <= 140 and area_pixels <= 2500 and boundary_complexity >= 2.0 and vertices >= 16
    return compact_glyph_run or tiny_many_edges or small_irregular_mark

def extract_flat_regions(image_rgb: np.ndarray, labels: np.ndarray, stats: list[SuperpixelStats], args: argparse.Namespace) -> tuple[list[FlatRegion], np.ndarray]:
    stat_by_label = {stat.label: stat for stat in stats}
    flat_mask = np.zeros(labels.shape, dtype=np.uint8)
    bin_mask_by_color: dict[tuple[int, int, int], np.ndarray] = {}
    for stat in stats:
        if not stat.is_flat:
            continue
        mask = labels == stat.label
        flat_mask[mask] = 255
        key = color_bin(stat.mean_rgb, args.color_bin_size)
        if key not in bin_mask_by_color:
            bin_mask_by_color[key] = np.zeros(labels.shape, dtype=np.uint8)
        bin_mask_by_color[key][mask] = 255

    if args.close_kernel > 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (args.close_kernel, args.close_kernel))
        for key in list(bin_mask_by_color.keys()):
            bin_mask_by_color[key] = cv2.morphologyEx(bin_mask_by_color[key], cv2.MORPH_CLOSE, kernel, iterations=1)

    regions: list[FlatRegion] = []
    next_id = 1
    for key, mask in bin_mask_by_color.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            area = int(cv2.contourArea(contour))
            if area < args.min_region_area:
                continue
            x, y, width, height = cv2.boundingRect(contour)
            component_mask = np.zeros(mask.shape, dtype=np.uint8)
            cv2.drawContours(component_mask, [contour], -1, 255, thickness=-1)
            component_pixels = int(np.count_nonzero(component_mask))
            component_labels = np.unique(labels[component_mask > 0])
            component_stats = [stat_by_label[int(label)] for label in component_labels if int(label) in stat_by_label and stat_by_label[int(label)].is_flat]
            if not component_stats:
                continue
            mean_rgb = np.mean([stat.mean_rgb for stat in component_stats], axis=0)
            mean_lab_std = float(np.mean([stat.lab_std for stat in component_stats]))
            mean_edge_density = float(np.mean([stat.edge_density for stat in component_stats]))
            mean_entropy = float(np.mean([stat.entropy for stat in component_stats]))
            bbox_area = max(width * height, 1)
            extent = component_pixels / bbox_area
            perimeter = max(float(cv2.arcLength(contour, True)), 1.0)
            contour_area = max(float(cv2.contourArea(contour)), 1.0)
            approx = cv2.approxPolyDP(contour, 0.006 * perimeter, True)
            vertices = int(len(approx))
            hull = cv2.convexHull(contour)
            hull_area = max(float(cv2.contourArea(hull)), 1.0)
            solidity = float(contour_area / hull_area)
            boundary_complexity = float((perimeter * perimeter) / (4.0 * math.pi * contour_area))
            text_like = is_text_like_region(width, height, component_pixels, vertices, boundary_complexity)
            if text_like:
                region_class = "text_fragment"
            elif extent >= 0.55 and solidity >= 0.78 and vertices <= 22 and boundary_complexity <= 6.0:
                region_class = "simple_flat"
            else:
                region_class = "flat_fragment"
            confidence = min(1.0, 0.25 + (1.0 - min(mean_lab_std / max(args.max_lab_std, 1e-6), 1.0)) * 0.2 + (1.0 - min(mean_entropy / max(args.max_entropy, 1e-6), 1.0)) * 0.15 + extent * 0.2 + solidity * 0.15 + min(component_pixels / 50000.0, 1.0) * 0.1)
            regions.append(
                FlatRegion(
                    id=next_id,
                    color=rgb_to_hex(mean_rgb),
                    x=int(x),
                    y=int(y),
                    width=int(width),
                    height=int(height),
                    area_pixels=component_pixels,
                    bbox_area=bbox_area,
                    extent=round(float(extent), 4),
                    mean_lab_std=round(mean_lab_std, 4),
                    mean_edge_density=round(mean_edge_density, 4),
                    mean_entropy=round(mean_entropy, 4),
                    superpixel_count=len(component_stats),
                    confidence=round(float(confidence), 4),
                    vertices=vertices,
                    solidity=round(float(solidity), 4),
                    boundary_complexity=round(boundary_complexity, 4),
                    is_text_like=text_like,
                    region_class=region_class,
                    svg_path=contour_to_svg_path(contour),
                )
            )
            next_id += 1
    regions.sort(key=lambda item: (item.y, item.x, -item.area_pixels))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions, flat_mask


def region_debug_color(region_class: str) -> tuple[str, tuple[int, int, int]]:
    if region_class == "simple_flat":
        return "#1FBF75", (31, 191, 117)
    if region_class == "text_fragment":
        return "#2F80ED", (47, 128, 237)
    return "#FF2E88", (255, 46, 136)


def write_svg(path: Path, width: int, height: int, background_color: str, regions: list[FlatRegion]) -> None:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'  <rect width="100%" height="100%" fill="{html.escape(background_color)}"/>',
        '  <g id="flat-regions" stroke-width="2" stroke-linejoin="round">',
    ]
    for region in regions:
        debug_color, _ = region_debug_color(region.region_class)
        lines.append(f'    <path id="flat-region-{region.id}" d="{html.escape(region.svg_path)}" fill="{html.escape(region.color)}" fill-opacity="0.72" stroke="{debug_color}"/>')
        lines.append(f'    <text x="{region.x + 4}" y="{region.y + 14}" font-family="monospace" font-size="10" fill="{debug_color}" stroke="#fff" stroke-width="1" paint-order="stroke">#{region.id} {region.region_class} {region.confidence}</text>')
    lines.extend(['  </g>', '</svg>', ''])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_overlay(path: Path, image_rgb: np.ndarray, regions: list[FlatRegion]) -> None:
    image = Image.fromarray(image_rgb).convert("RGB")
    draw = ImageDraw.Draw(image)
    for region in regions:
        _, debug_rgb = region_debug_color(region.region_class)
        draw.rectangle((region.x, region.y, region.x + region.width, region.y + region.height), outline=debug_rgb, width=3)
        draw.text((region.x + 4, region.y + 4), f"#{region.id} {region.region_class} {region.confidence}", fill=debug_rgb)
    image.save(path)


def write_superpixel_overlay(path: Path, image_rgb: np.ndarray, labels: np.ndarray, stats: list[SuperpixelStats]) -> None:
    flat_labels = {stat.label for stat in stats if stat.is_flat}
    background_labels = {stat.label for stat in stats if stat.is_background}
    overlay = image_rgb.copy().astype(np.float32)
    flat_mask = np.isin(labels, list(flat_labels))
    background_mask = np.isin(labels, list(background_labels))
    textured_mask = ~(flat_mask | background_mask)
    overlay[flat_mask] = overlay[flat_mask] * 0.45 + np.array([0, 220, 110], dtype=np.float32) * 0.55
    overlay[textured_mask] = overlay[textured_mask] * 0.5 + np.array([240, 80, 80], dtype=np.float32) * 0.5
    overlay[background_mask] = overlay[background_mask] * 0.85
    boundaries = np.zeros(labels.shape, dtype=np.uint8)
    boundaries[:, 1:] |= labels[:, 1:] != labels[:, :-1]
    boundaries[1:, :] |= labels[1:, :] != labels[:-1, :]
    overlay[boundaries > 0] = np.array([255, 255, 255], dtype=np.float32)
    Image.fromarray(np.clip(overlay, 0, 255).astype(np.uint8)).save(path)


def write_contact_sheet(path: Path, original_path: Path, flat_svg_path: Path, overlay_path: Path, superpixel_overlay_path: Path) -> None:
    import cairosvg
    import io

    items = [
        ("original", original_path),
        ("superpixels: green flat / red textured", superpixel_overlay_path),
        ("flat regions overlay", overlay_path),
        ("flat regions svg", flat_svg_path),
    ]
    thumbs = []
    for label, item_path in items:
        if item_path.suffix.lower() == ".svg":
            png = cairosvg.svg2png(url=str(item_path))
            image = Image.open(io.BytesIO(png)).convert("RGB")
        else:
            image = Image.open(item_path).convert("RGB")
        canvas = Image.new("RGB", (390, 540), "white")
        image.thumbnail((360, 460), Image.Resampling.LANCZOS)
        canvas.paste(image, ((390 - image.width) // 2, 46))
        draw = ImageDraw.Draw(canvas)
        draw.text((14, 14), label, fill=(20, 20, 20))
        thumbs.append(canvas)
    sheet = Image.new("RGB", (780, 1080), (245, 242, 232))
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % 2) * 390, (index // 2) * 540))
    sheet.save(path)


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    out_dir = resolve_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    image_rgb = load_rgb(image_path)
    labels = slic_labels(image_rgb, args.region_size, args.ruler)
    stats, edges, entropy_image = compute_superpixel_stats(image_rgb, labels, args)
    regions, flat_mask = extract_flat_regions(image_rgb, labels, stats, args)
    background = rgb_to_hex(estimate_background(image_rgb))
    height, width = image_rgb.shape[:2]

    flat_svg_path = out_dir.joinpath("flat_regions.svg")
    simple_svg_path = out_dir.joinpath("simple_flat_regions.svg")
    text_svg_path = out_dir.joinpath("text_fragments.svg")
    overlay_path = out_dir.joinpath("flat_regions_overlay.png")
    simple_overlay_path = out_dir.joinpath("simple_flat_regions_overlay.png")
    text_overlay_path = out_dir.joinpath("text_fragments_overlay.png")
    superpixel_overlay_path = out_dir.joinpath("superpixel_classification_overlay.png")
    simple_regions = [region for region in regions if region.region_class == "simple_flat"]
    text_regions = [region for region in regions if region.region_class == "text_fragment"]
    write_svg(flat_svg_path, width, height, background, regions)
    write_svg(simple_svg_path, width, height, background, simple_regions)
    write_svg(text_svg_path, width, height, background, text_regions)
    write_overlay(overlay_path, image_rgb, regions)
    write_overlay(simple_overlay_path, image_rgb, simple_regions)
    write_overlay(text_overlay_path, image_rgb, text_regions)
    write_superpixel_overlay(superpixel_overlay_path, image_rgb, labels, stats)
    Image.fromarray(flat_mask).save(out_dir.joinpath("flat_mask.png"))
    Image.fromarray(edges).save(out_dir.joinpath("edge_mask.png"))
    Image.fromarray(np.clip(entropy_image / max(float(entropy_image.max()), 1e-6) * 255, 0, 255).astype(np.uint8)).save(out_dir.joinpath("entropy_map.png"))
    write_contact_sheet(out_dir.joinpath("inspection_contact_sheet.png"), image_path, flat_svg_path, overlay_path, superpixel_overlay_path)

    payload = {
        "image": str(image_path),
        "background_color": background,
        "region_count": len(regions),
        "simple_region_count": len(simple_regions),
        "text_fragment_count": len(text_regions),
        "class_counts": {
            "simple_flat": len(simple_regions),
            "text_fragment": len(text_regions),
            "flat_fragment": sum(1 for region in regions if region.region_class == "flat_fragment"),
        },
        "superpixel_count": len(stats),
        "flat_superpixel_count": int(sum(1 for stat in stats if stat.is_flat)),
        "regions": [asdict(region) for region in regions],
        "thresholds": {
            "max_lab_std": args.max_lab_std,
            "max_rgb_std": args.max_rgb_std,
            "max_edge_density": args.max_edge_density,
            "max_entropy": args.max_entropy,
            "background_distance": args.background_distance,
        },
        "notes": [
            "Green superpixels in the overlay are classified as flat/unicolored; red superpixels are textured/image-like.",
            "Flat regions are merged only when neighboring flat superpixels fall into the same quantized color bin.",
        ],
    }
    out_dir.joinpath("flat_regions.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())






