from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


WINDOWS_FONTS_DIR = Path("C:\\Windows\\Fonts")
REPO_FONT_DIR_NAMES = ("fonts", "assets/fonts")


@dataclass(slots=True)
class CandidateSpec:
    label: str
    font_path: str
    size_min: int
    size_max: int
    tracking_min: int
    tracking_max: int
    x_scale_min: float
    x_scale_max: float
    x_scale_step: float
    y_scale_min: float
    y_scale_max: float
    y_scale_step: float
    offset_x_min: int
    offset_x_max: int
    offset_y_min: int
    offset_y_max: int


@dataclass(slots=True)
class CandidateScore:
    label: str
    font_path: str
    font_size: int
    tracking: int
    x_scale: float
    y_scale: float
    offset_x: int
    offset_y: int
    mse: float
    overlap: float
    score: float
    glyph_pixels: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare two candidate fonts against a screenshot crop after fitting each one "
            "independently over size, spacing, x/y scale, and offsets."
        )
    )
    parser.add_argument("image", type=Path, help="Image containing the text crop")
    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        metavar=("X1", "Y1", "X2", "Y2"),
        required=True,
        help="Crop bounds containing the text",
    )
    parser.add_argument("--text", required=True, help="Text to render")
    parser.add_argument("--out-dir", type=Path, required=True, help="Debug output folder")

    add_candidate_args(parser, "font-a")
    add_candidate_args(parser, "font-b")
    return parser.parse_args()


def add_candidate_args(parser: argparse.ArgumentParser, prefix: str) -> None:
    parser.add_argument(f"--{prefix}-query", required=True)
    parser.add_argument(f"--{prefix}-size-min", type=int, required=True)
    parser.add_argument(f"--{prefix}-size-max", type=int, required=True)
    parser.add_argument(f"--{prefix}-tracking-min", type=int, default=0)
    parser.add_argument(f"--{prefix}-tracking-max", type=int, default=0)
    parser.add_argument(f"--{prefix}-x-scale-min", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-x-scale-max", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-x-scale-step", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-y-scale-min", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-y-scale-max", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-y-scale-step", type=float, default=1.0)
    parser.add_argument(f"--{prefix}-offset-x-min", type=int, default=-2)
    parser.add_argument(f"--{prefix}-offset-x-max", type=int, default=2)
    parser.add_argument(f"--{prefix}-offset-y-min", type=int, default=-2)
    parser.add_argument(f"--{prefix}-offset-y-max", type=int, default=2)
    default_label = prefix.replace("-", "_")
    parser.add_argument(f"--{prefix}-label", default=default_label)


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


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
    return all_fonts


def resolve_font_path(font_query: str) -> Path:
    lowered = font_query.lower()
    matches = [path for path in iter_font_paths() if lowered in path.name.lower()]
    if not matches:
        raise FileNotFoundError(f"No font found for query: {font_query}")
    matches.sort(key=lambda path: (len(path.name), str(path).lower()))
    return matches[0]


def load_crop(image_path: Path, crop: list[int]) -> np.ndarray:
    image = Image.open(image_path).convert("RGB")
    x1, y1, x2, y2 = crop
    return np.array(image.crop((x1, y1, x2, y2)), dtype=np.float32)


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


def build_target_mask(crop_rgb: np.ndarray) -> np.ndarray:
    bg = np.array([235.0, 223.0, 199.0], dtype=np.float32)
    fg = np.array([86.0, 97.0, 41.0], dtype=np.float32)
    dist_bg = np.linalg.norm(crop_rgb - bg, axis=2)
    dist_fg = np.linalg.norm(crop_rgb - fg, axis=2)
    return np.clip((dist_fg - dist_bg + 80.0) / 160.0, 0.0, 1.0)


def render_tight_text_mask(
    text: str,
    font_path: Path,
    font_size: int,
    tracking: int,
) -> np.ndarray | None:
    pad = max(20, font_size)
    canvas_width = 2000
    canvas_height = max(200, font_size * 5)
    canvas = Image.new("L", (canvas_width, canvas_height), 0)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(font_path), font_size)

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


def place_scaled_mask(
    tight_mask: np.ndarray,
    target_shape: tuple[int, int],
    x_scale: float,
    y_scale: float,
    offset_x: int,
    offset_y: int,
) -> np.ndarray | None:
    target_height, target_width = target_shape
    scaled_width = max(1, int(round(tight_mask.shape[1] * x_scale)))
    scaled_height = max(1, int(round(tight_mask.shape[0] * y_scale)))
    scaled = cv2.resize(tight_mask, (scaled_width, scaled_height), interpolation=cv2.INTER_LINEAR)

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
    out[dst_top:dst_bottom, dst_left:dst_right] = scaled[src_top:src_bottom, src_left:src_right]
    return out


def score_mask(candidate: np.ndarray, target: np.ndarray) -> tuple[float, float, float]:
    mse = float(((candidate - target) ** 2).mean())
    candidate_bin = candidate > 0.4
    target_bin = target > 0.4
    intersection = float(np.logical_and(candidate_bin, target_bin).sum())
    union = float(np.logical_or(candidate_bin, target_bin).sum())
    overlap = 0.0 if union == 0 else intersection / union
    score = overlap - mse
    return mse, overlap, score


def save_mask(path: Path, mask: np.ndarray) -> None:
    cv2.imwrite(str(path), (np.clip(mask, 0.0, 1.0) * 255).astype(np.uint8))


def save_overlay(path: Path, crop_rgb: np.ndarray, candidate: np.ndarray, target: np.ndarray) -> None:
    overlay = crop_rgb.astype(np.uint8).copy()
    candidate_bin = candidate > 0.4
    target_bin = target > 0.4
    true_positive = np.logical_and(candidate_bin, target_bin)
    false_positive = np.logical_and(candidate_bin, np.logical_not(target_bin))
    false_negative = np.logical_and(np.logical_not(candidate_bin), target_bin)

    overlay[true_positive] = np.array([80, 220, 120], dtype=np.uint8)
    overlay[false_positive] = np.array([220, 90, 90], dtype=np.uint8)
    overlay[false_negative] = np.array([90, 130, 255], dtype=np.uint8)
    cv2.imwrite(str(path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))


def fit_candidate(
    crop_rgb: np.ndarray,
    target: np.ndarray,
    text: str,
    spec: CandidateSpec,
) -> tuple[CandidateScore, np.ndarray]:
    best_result: CandidateScore | None = None
    best_mask: np.ndarray | None = None
    x_scales = float_range(spec.x_scale_min, spec.x_scale_max, spec.x_scale_step)
    y_scales = float_range(spec.y_scale_min, spec.y_scale_max, spec.y_scale_step)

    for font_size in range(spec.size_min, spec.size_max + 1):
        for tracking in range(spec.tracking_min, spec.tracking_max + 1):
            tight_mask = render_tight_text_mask(text, Path(spec.font_path), font_size, tracking)
            if tight_mask is None:
                continue
            for x_scale in x_scales:
                for y_scale in y_scales:
                    for offset_x in range(spec.offset_x_min, spec.offset_x_max + 1):
                        for offset_y in range(spec.offset_y_min, spec.offset_y_max + 1):
                            mask = place_scaled_mask(
                                tight_mask,
                                (crop_rgb.shape[0], crop_rgb.shape[1]),
                                x_scale,
                                y_scale,
                                offset_x,
                                offset_y,
                            )
                            if mask is None:
                                continue
                            mse, overlap, score = score_mask(mask, target)
                            result = CandidateScore(
                                label=spec.label,
                                font_path=spec.font_path,
                                font_size=font_size,
                                tracking=tracking,
                                x_scale=round(x_scale, 4),
                                y_scale=round(y_scale, 4),
                                offset_x=offset_x,
                                offset_y=offset_y,
                                mse=round(mse, 6),
                                overlap=round(overlap, 6),
                                score=round(score, 6),
                                glyph_pixels=int((mask > 0.4).sum()),
                            )
                            if best_result is None or result.score > best_result.score:
                                best_result = result
                                best_mask = mask

    if best_result is None or best_mask is None:
        raise RuntimeError(f"Could not fit candidate: {spec.label}")
    return best_result, best_mask


def build_spec(args: argparse.Namespace, prefix: str, font_path: Path) -> CandidateSpec:
    prefix_attr = prefix.replace("-", "_")
    return CandidateSpec(
        label=getattr(args, f"{prefix_attr}_label"),
        font_path=str(font_path),
        size_min=getattr(args, f"{prefix_attr}_size_min"),
        size_max=getattr(args, f"{prefix_attr}_size_max"),
        tracking_min=getattr(args, f"{prefix_attr}_tracking_min"),
        tracking_max=getattr(args, f"{prefix_attr}_tracking_max"),
        x_scale_min=getattr(args, f"{prefix_attr}_x_scale_min"),
        x_scale_max=getattr(args, f"{prefix_attr}_x_scale_max"),
        x_scale_step=getattr(args, f"{prefix_attr}_x_scale_step"),
        y_scale_min=getattr(args, f"{prefix_attr}_y_scale_min"),
        y_scale_max=getattr(args, f"{prefix_attr}_y_scale_max"),
        y_scale_step=getattr(args, f"{prefix_attr}_y_scale_step"),
        offset_x_min=getattr(args, f"{prefix_attr}_offset_x_min"),
        offset_x_max=getattr(args, f"{prefix_attr}_offset_x_max"),
        offset_y_min=getattr(args, f"{prefix_attr}_offset_y_min"),
        offset_y_max=getattr(args, f"{prefix_attr}_offset_y_max"),
    )


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    out_dir = resolve_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    crop = list(args.crop)
    crop_rgb = load_crop(image_path, crop)
    target = build_target_mask(crop_rgb)

    font_a = resolve_font_path(args.font_a_query)
    font_b = resolve_font_path(args.font_b_query)
    spec_a = build_spec(args, "font-a", font_a)
    spec_b = build_spec(args, "font-b", font_b)

    result_a, mask_a = fit_candidate(crop_rgb, target, args.text, spec_a)
    result_b, mask_b = fit_candidate(crop_rgb, target, args.text, spec_b)

    save_mask(out_dir.joinpath("target_mask.png"), target)
    cv2.imwrite(
        str(out_dir.joinpath("crop.png")),
        cv2.cvtColor(crop_rgb.astype(np.uint8), cv2.COLOR_RGB2BGR),
    )
    save_mask(out_dir.joinpath(f"{result_a.label}_mask.png"), mask_a)
    save_mask(out_dir.joinpath(f"{result_b.label}_mask.png"), mask_b)
    save_overlay(out_dir.joinpath(f"{result_a.label}_overlay.png"), crop_rgb, mask_a, target)
    save_overlay(out_dir.joinpath(f"{result_b.label}_overlay.png"), crop_rgb, mask_b, target)

    payload = {
        "image": str(image_path),
        "crop": crop,
        "text": args.text,
        "candidate_a": asdict(result_a),
        "candidate_b": asdict(result_b),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
