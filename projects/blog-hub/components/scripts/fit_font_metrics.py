from __future__ import annotations

import argparse
import concurrent.futures
import heapq
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


WINDOWS_FONTS_DIR = Path("C:\\Windows\\Fonts")
REPO_FONT_DIR_NAMES = ("fonts", "assets/fonts")


@dataclass(slots=True)
class FitResult:
    score: float
    mse: float
    overlap: float
    font_path: str
    font_size: int
    tracking: int
    x_scale: float
    y_scale: float
    offset_x: int
    offset_y: int
    glyph_pixels: int


@dataclass(slots=True)
class SearchParams:
    size_min: int
    size_max: int
    size_step: int
    tracking_min: int
    tracking_max: int
    tracking_step: int
    x_scale_min: float
    x_scale_max: float
    x_scale_step: float
    y_scale_min: float
    y_scale_max: float
    y_scale_step: float
    fit_scale_to_target: bool
    scale_refine_min: float
    scale_refine_max: float
    scale_refine_step: float
    absolute_x_scale_min: float
    absolute_x_scale_max: float
    absolute_y_scale_min: float
    absolute_y_scale_max: float
    offset_x_min: int
    offset_x_max: int
    offset_x_step: int
    offset_y_min: int
    offset_y_max: int
    offset_y_step: int
    per_font_top_k: int
    min_score_to_keep: float
    early_stop_score: float | None
    density_ratio_min: float
    density_ratio_max: float


@dataclass(slots=True)
class TargetGeometry:
    width: int
    height: int
    glyph_pixels: int


@dataclass(slots=True)
class FontSearchResult:
    results: list[FitResult]
    skipped: bool
    rendered_variants: int
    scaled_variants: int
    scored_variants: int
    early_stopped: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fit local fonts to a screenshot crop and rank the best metrics."
    )
    parser.add_argument("image", type=Path, help="Image containing the text")
    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        metavar=("X1", "Y1", "X2", "Y2"),
        required=True,
        help="Crop bounds containing the text",
    )
    parser.add_argument("--text", required=True, help="Text to render into the crop")
    parser.add_argument("--text-rgb", nargs=3, type=float, default=[235.0, 223.0, 199.0], metavar=("R", "G", "B"))
    parser.add_argument("--background-rgb", nargs=3, type=float, default=[86.0, 97.0, 41.0], metavar=("R", "G", "B"))
    parser.add_argument("--mask-softness", type=float, default=80.0)
    parser.add_argument(
        "--font-queries",
        nargs="+",
        default=None,
        help="One or more substrings used to match local font files",
    )
    parser.add_argument("--all-fonts", action="store_true", help="Search every local font.")
    parser.add_argument(
        "--font-list-json",
        type=Path,
        default=None,
        help="Search only unique font_path entries from a previous matcher JSON file.",
    )
    parser.add_argument("--size-min", type=int, required=True)
    parser.add_argument("--size-max", type=int, required=True)
    parser.add_argument("--size-step", type=int, default=1)
    parser.add_argument("--tracking-min", type=int, default=0)
    parser.add_argument("--tracking-max", type=int, default=0)
    parser.add_argument("--tracking-step", type=int, default=1)
    parser.add_argument("--x-scale-min", type=float, default=1.0)
    parser.add_argument("--x-scale-max", type=float, default=1.0)
    parser.add_argument("--x-scale-step", type=float, default=1.0)
    parser.add_argument("--y-scale-min", type=float, default=1.0)
    parser.add_argument("--y-scale-max", type=float, default=1.0)
    parser.add_argument("--y-scale-step", type=float, default=1.0)
    parser.add_argument(
        "--fit-scale-to-target",
        action="store_true",
        help="Fit each rendered font's width/height to the target text bbox before local scale refinement.",
    )
    parser.add_argument("--scale-refine-min", type=float, default=1.0)
    parser.add_argument("--scale-refine-max", type=float, default=1.0)
    parser.add_argument("--scale-refine-step", type=float, default=1.0)
    parser.add_argument("--absolute-x-scale-min", type=float, default=0.2)
    parser.add_argument("--absolute-x-scale-max", type=float, default=5.0)
    parser.add_argument("--absolute-y-scale-min", type=float, default=0.2)
    parser.add_argument("--absolute-y-scale-max", type=float, default=5.0)
    parser.add_argument("--offset-x-min", type=int, default=-2)
    parser.add_argument("--offset-x-max", type=int, default=2)
    parser.add_argument("--offset-x-step", type=int, default=1)
    parser.add_argument("--offset-y-min", type=int, default=-2)
    parser.add_argument("--offset-y-max", type=int, default=2)
    parser.add_argument("--offset-y-step", type=int, default=1)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--per-font-top-k", type=int, default=2)
    parser.add_argument("--min-score-to-keep", type=float, default=-1.0)
    parser.add_argument(
        "--early-stop-score",
        type=float,
        default=None,
        help="Stop searching a font once any candidate reaches this score.",
    )
    parser.add_argument(
        "--density-ratio-min",
        type=float,
        default=0.0,
        help="Skip scaled masks with too few foreground pixels relative to target.",
    )
    parser.add_argument(
        "--density-ratio-max",
        type=float,
        default=999.0,
        help="Skip scaled masks with too many foreground pixels relative to target.",
    )
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--progress-every", type=int, default=100)
    parser.add_argument("--out-json", type=Path, default=None)
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def int_range(start: int, stop: int, step: int) -> range:
    if step <= 0:
        raise ValueError("Integer range step must be greater than zero")
    return range(start, stop + 1, step)


def float_range(start: float, stop: float, step: float) -> list[float]:
    if step <= 0:
        raise ValueError("Scale step must be greater than zero")
    values: list[float] = []
    current = start
    epsilon = step / 2.0
    while current <= stop + epsilon:
        values.append(round(current, 4))
        current += step
    return values


def iter_font_paths() -> list[Path]:
    search_roots = [WINDOWS_FONTS_DIR]
    for dir_name in REPO_FONT_DIR_NAMES:
        search_roots.append(Path.cwd().joinpath(*dir_name.split("/")))
    all_fonts: list[Path] = []
    for root in search_roots:
        if not root.exists():
            continue
        for extension in ("*.ttf", "*.otf", "*.ttc"):
            all_fonts.extend(root.rglob(extension))
    return sorted(set(all_fonts), key=lambda path: str(path).lower())


def read_font_paths_from_json(path: Path) -> list[Path]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    paths: list[Path] = []
    seen: set[str] = set()
    for result in payload.get("results", []):
        font_path = result.get("font_path")
        if not font_path or font_path in seen:
            continue
        seen.add(font_path)
        paths.append(Path(font_path))
    if not paths:
        raise ValueError(f"No result font_path entries found in {path}")
    return paths


def resolve_font_paths(queries: list[str] | None, all_fonts: bool, font_list_json: Path | None) -> list[Path]:
    if font_list_json is not None:
        return read_font_paths_from_json(resolve_path(font_list_json))

    available_fonts = iter_font_paths()
    if all_fonts:
        return available_fonts
    if not queries:
        raise ValueError("Use --font-queries, --all-fonts, or --font-list-json")

    font_paths: list[Path] = []
    seen: set[Path] = set()
    for query in queries:
        lowered = query.lower()
        matches = [path for path in available_fonts if lowered in path.name.lower()]
        for path in matches:
            if path not in seen:
                seen.add(path)
                font_paths.append(path)
    if not font_paths:
        raise FileNotFoundError(f"No fonts found for queries: {queries}")
    return sorted(font_paths, key=lambda path: path.name.lower())


def load_crop(image_path: Path, crop: list[int]) -> np.ndarray:
    image = Image.open(image_path).convert("RGB")
    x1, y1, x2, y2 = crop
    return np.array(image.crop((x1, y1, x2, y2)), dtype=np.float32)


def build_target_mask(
    crop_rgb: np.ndarray,
    text_rgb: list[float],
    background_rgb: list[float],
    softness: float,
) -> np.ndarray:
    text_color = np.array(text_rgb, dtype=np.float32)
    background_color = np.array(background_rgb, dtype=np.float32)
    dist_text = np.linalg.norm(crop_rgb - text_color, axis=2)
    dist_background = np.linalg.norm(crop_rgb - background_color, axis=2)
    return np.clip((dist_background - dist_text + softness) / (softness * 2.0), 0.0, 1.0)


def get_target_geometry(target: np.ndarray) -> TargetGeometry:
    target_bin = target > 0.4
    rows, cols = np.where(target_bin)
    if rows.size == 0 or cols.size == 0:
        raise ValueError("Target mask has no text-like pixels")
    return TargetGeometry(
        width=int(cols.max() - cols.min() + 1),
        height=int(rows.max() - rows.min() + 1),
        glyph_pixels=int(target_bin.sum()),
    )


def render_tight_text_mask(
    text: str,
    font_path: Path,
    font_size: int,
    tracking: int,
) -> np.ndarray | None:
    pad = max(20, font_size)
    canvas_width = 2000
    canvas_height = max(200, font_size * 5)
    try:
        font = ImageFont.truetype(str(font_path), font_size)
    except OSError:
        return None

    canvas = Image.new("L", (canvas_width, canvas_height), 0)
    draw = ImageDraw.Draw(canvas)

    widths: list[int] = []
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        widths.append(bbox[2] - bbox[0])

    total_width = sum(widths) + max(len(text) - 1, 0) * tracking
    bbox_total = draw.textbbox((0, 0), text, font=font)
    total_height = bbox_total[3] - bbox_total[1]
    if total_width + pad * 2 > canvas_width:
        canvas_width = int(total_width + pad * 2)
        canvas = Image.new("L", (canvas_width, canvas_height), 0)
        draw = ImageDraw.Draw(canvas)

    x = pad
    y = (canvas_height - total_height) // 2 - bbox_total[1]
    for index, char in enumerate(text):
        draw.text((x, y), char, fill=255, font=font)
        x += widths[index] + tracking

    alpha = np.array(canvas, dtype=np.float32) / 255.0
    rows, cols = np.where(alpha > 0)
    if rows.size == 0 or cols.size == 0:
        return None
    return alpha[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]


def scale_mask(tight_mask: np.ndarray, x_scale: float, y_scale: float) -> np.ndarray:
    scaled_width = max(1, int(round(tight_mask.shape[1] * x_scale)))
    scaled_height = max(1, int(round(tight_mask.shape[0] * y_scale)))
    return cv2.resize(tight_mask, (scaled_width, scaled_height), interpolation=cv2.INTER_LINEAR)


def place_mask(
    scaled_mask: np.ndarray,
    target_shape: tuple[int, int],
    offset_x: int,
    offset_y: int,
) -> np.ndarray | None:
    target_height, target_width = target_shape
    scaled_height, scaled_width = scaled_mask.shape
    out = np.zeros((target_height, target_width), dtype=np.float32)
    left = (target_width - scaled_width) // 2 + offset_x
    top = (target_height - scaled_height) // 2 + offset_y
    right = left + scaled_width
    bottom = top + scaled_height

    dst_left = max(0, left)
    dst_top = max(0, top)
    dst_right = min(target_width, right)
    dst_bottom = min(target_height, bottom)
    if dst_left >= dst_right or dst_top >= dst_bottom:
        return None

    src_left = dst_left - left
    src_top = dst_top - top
    src_right = src_left + (dst_right - dst_left)
    src_bottom = src_top + (dst_bottom - dst_top)
    out[dst_top:dst_bottom, dst_left:dst_right] = scaled_mask[src_top:src_bottom, src_left:src_right]
    return out


def score_mask(candidate: np.ndarray, target: np.ndarray) -> tuple[float, float, float]:
    mse = float(((candidate - target) ** 2).mean())
    candidate_bin = candidate > 0.4
    target_bin = target > 0.4
    intersection = float(np.logical_and(candidate_bin, target_bin).sum())
    union = float(np.logical_or(candidate_bin, target_bin).sum())
    overlap = 0.0 if union == 0 else intersection / union
    score = overlap - mse
    return score, mse, overlap


def candidate_scales(
    params: SearchParams,
    tight_mask: np.ndarray,
    target_geometry: TargetGeometry,
) -> tuple[list[float], list[float]]:
    if not params.fit_scale_to_target:
        return (
            float_range(params.x_scale_min, params.x_scale_max, params.x_scale_step),
            float_range(params.y_scale_min, params.y_scale_max, params.y_scale_step),
        )

    base_x = target_geometry.width / tight_mask.shape[1]
    base_y = target_geometry.height / tight_mask.shape[0]
    refinements = float_range(params.scale_refine_min, params.scale_refine_max, params.scale_refine_step)
    x_scales = sorted(
        {
            round(base_x * refinement, 4)
            for refinement in refinements
            if params.absolute_x_scale_min <= base_x * refinement <= params.absolute_x_scale_max
        }
    )
    y_scales = sorted(
        {
            round(base_y * refinement, 4)
            for refinement in refinements
            if params.absolute_y_scale_min <= base_y * refinement <= params.absolute_y_scale_max
        }
    )
    return x_scales, y_scales


def push_top_result(heap: list[tuple[float, int, FitResult]], counter: int, result: FitResult, top_k: int) -> None:
    item = (result.score, counter, result)
    if len(heap) < top_k:
        heapq.heappush(heap, item)
        return
    if result.score > heap[0][0]:
        heapq.heapreplace(heap, item)


def search_font(
    font_path_text: str,
    text: str,
    target: np.ndarray,
    target_geometry: TargetGeometry,
    params: SearchParams,
) -> FontSearchResult:
    font_path = Path(font_path_text)
    target_shape = (target.shape[0], target.shape[1])
    heap: list[tuple[float, int, FitResult]] = []
    counter = 0
    rendered_variants = 0
    scaled_variants = 0
    scored_variants = 0
    early_stopped = False

    for font_size in int_range(params.size_min, params.size_max, params.size_step):
        for tracking in int_range(params.tracking_min, params.tracking_max, params.tracking_step):
            tight_mask = render_tight_text_mask(text, font_path, font_size, tracking)
            if tight_mask is None:
                continue
            rendered_variants += 1
            x_scales, y_scales = candidate_scales(params, tight_mask, target_geometry)
            if not x_scales or not y_scales:
                continue
            for x_scale in x_scales:
                for y_scale in y_scales:
                    scaled_mask = scale_mask(tight_mask, x_scale, y_scale)
                    scaled_variants += 1
                    density_ratio = float((scaled_mask > 0.4).sum()) / max(target_geometry.glyph_pixels, 1)
                    if density_ratio < params.density_ratio_min or density_ratio > params.density_ratio_max:
                        continue
                    for offset_x in int_range(params.offset_x_min, params.offset_x_max, params.offset_x_step):
                        for offset_y in int_range(params.offset_y_min, params.offset_y_max, params.offset_y_step):
                            candidate = place_mask(scaled_mask, target_shape, offset_x, offset_y)
                            if candidate is None:
                                continue
                            scored_variants += 1
                            score, mse, overlap = score_mask(candidate, target)
                            if score < params.min_score_to_keep:
                                continue
                            result = FitResult(
                                score=round(score, 6),
                                mse=round(mse, 6),
                                overlap=round(overlap, 6),
                                font_path=font_path_text,
                                font_size=font_size,
                                tracking=tracking,
                                x_scale=round(x_scale, 4),
                                y_scale=round(y_scale, 4),
                                offset_x=offset_x,
                                offset_y=offset_y,
                                glyph_pixels=int((candidate > 0.4).sum()),
                            )
                            push_top_result(heap, counter, result, params.per_font_top_k)
                            counter += 1
                            if params.early_stop_score is not None and score >= params.early_stop_score:
                                early_stopped = True
                                results = [item[2] for item in sorted(heap, key=lambda item: item[0], reverse=True)]
                                return FontSearchResult(
                                    results=results,
                                    skipped=rendered_variants == 0,
                                    rendered_variants=rendered_variants,
                                    scaled_variants=scaled_variants,
                                    scored_variants=scored_variants,
                                    early_stopped=early_stopped,
                                )

    results = [item[2] for item in sorted(heap, key=lambda item: item[0], reverse=True)]
    return FontSearchResult(
        results=results,
        skipped=rendered_variants == 0,
        rendered_variants=rendered_variants,
        scaled_variants=scaled_variants,
        scored_variants=scored_variants,
        early_stopped=early_stopped,
    )


def make_search_params(args: argparse.Namespace) -> SearchParams:
    return SearchParams(
        size_min=args.size_min,
        size_max=args.size_max,
        size_step=args.size_step,
        tracking_min=args.tracking_min,
        tracking_max=args.tracking_max,
        tracking_step=args.tracking_step,
        x_scale_min=args.x_scale_min,
        x_scale_max=args.x_scale_max,
        x_scale_step=args.x_scale_step,
        y_scale_min=args.y_scale_min,
        y_scale_max=args.y_scale_max,
        y_scale_step=args.y_scale_step,
        fit_scale_to_target=args.fit_scale_to_target,
        scale_refine_min=args.scale_refine_min,
        scale_refine_max=args.scale_refine_max,
        scale_refine_step=args.scale_refine_step,
        absolute_x_scale_min=args.absolute_x_scale_min,
        absolute_x_scale_max=args.absolute_x_scale_max,
        absolute_y_scale_min=args.absolute_y_scale_min,
        absolute_y_scale_max=args.absolute_y_scale_max,
        offset_x_min=args.offset_x_min,
        offset_x_max=args.offset_x_max,
        offset_x_step=args.offset_x_step,
        offset_y_min=args.offset_y_min,
        offset_y_max=args.offset_y_max,
        offset_y_step=args.offset_y_step,
        per_font_top_k=args.per_font_top_k,
        min_score_to_keep=args.min_score_to_keep,
        early_stop_score=args.early_stop_score,
        density_ratio_min=args.density_ratio_min,
        density_ratio_max=args.density_ratio_max,
    )


def run_search(
    font_paths: list[Path],
    text: str,
    target: np.ndarray,
    target_geometry: TargetGeometry,
    params: SearchParams,
    workers: int,
    progress_every: int,
    top_k: int,
) -> tuple[list[FitResult], int, int, int, int, int]:
    global_heap: list[tuple[float, int, FitResult]] = []
    counter = 0
    skipped_fonts = 0
    rendered_variants = 0
    scaled_variants = 0
    scored_variants = 0
    early_stopped_fonts = 0

    if workers <= 1:
        for index, font_path in enumerate(font_paths, start=1):
            result = search_font(str(font_path), text, target, target_geometry, params)
            skipped_fonts += int(result.skipped)
            rendered_variants += result.rendered_variants
            scaled_variants += result.scaled_variants
            scored_variants += result.scored_variants
            early_stopped_fonts += int(result.early_stopped)
            for fit in result.results:
                push_top_result(global_heap, counter, fit, top_k)
                counter += 1
            if progress_every > 0 and index % progress_every == 0:
                print(f"searched {index}/{len(font_paths)} fonts", file=sys.stderr, flush=True)
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(search_font, str(font_path), text, target, target_geometry, params)
                for font_path in font_paths
            ]
            for index, future in enumerate(concurrent.futures.as_completed(futures), start=1):
                result = future.result()
                skipped_fonts += int(result.skipped)
                rendered_variants += result.rendered_variants
                scaled_variants += result.scaled_variants
                scored_variants += result.scored_variants
                early_stopped_fonts += int(result.early_stopped)
                for fit in result.results:
                    push_top_result(global_heap, counter, fit, top_k)
                    counter += 1
                if progress_every > 0 and index % progress_every == 0:
                    print(f"searched {index}/{len(font_paths)} fonts", file=sys.stderr, flush=True)

    results = [item[2] for item in sorted(global_heap, key=lambda item: item[0], reverse=True)]
    return results, skipped_fonts, rendered_variants, scaled_variants, scored_variants, early_stopped_fonts


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    crop = list(args.crop)
    crop_rgb = load_crop(image_path, crop)
    target = build_target_mask(crop_rgb, args.text_rgb, args.background_rgb, args.mask_softness)
    target_geometry = get_target_geometry(target)
    fonts = resolve_font_paths(args.font_queries, args.all_fonts, args.font_list_json)
    params = make_search_params(args)

    results, skipped_fonts, rendered_variants, scaled_variants, scored_variants, early_stopped_fonts = run_search(
        font_paths=fonts,
        text=args.text,
        target=target,
        target_geometry=target_geometry,
        params=params,
        workers=args.workers,
        progress_every=args.progress_every,
        top_k=args.top_k,
    )

    payload = {
        "image": str(image_path),
        "crop": crop,
        "text": args.text,
        "font_count": len(fonts),
        "skipped_fonts": skipped_fonts,
        "rendered_variants": rendered_variants,
        "scaled_variants": scaled_variants,
        "scored_variants": scored_variants,
        "early_stopped_fonts": early_stopped_fonts,
        "target_geometry": asdict(target_geometry),
        "workers": args.workers,
        "results": [asdict(item) for item in results],
    }

    output = json.dumps(payload, indent=2)
    if args.out_json is not None:
        out_json = resolve_path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(output, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
