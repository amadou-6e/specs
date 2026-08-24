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
class ColorPickResult:
    text: str
    font_path: str
    font_size: int
    tracking: int
    crop: list[int]
    solid_fill_hex: str
    solid_fill_rgb: list[int]
    rendered_text_mean_hex: str
    rendered_text_mean_rgb: list[int]
    background_hex: str
    background_rgb: list[int]
    core_text_mean_hex: str
    core_text_mean_rgb: list[int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate a repeatable solid font fill color from a screenshot crop by "
            "rendering the text back into the crop and solving against the observed pixels."
        )
    )
    parser.add_argument("image", type=Path, help="Image to sample")
    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        metavar=("X1", "Y1", "X2", "Y2"),
        required=True,
        help="Crop bounds containing the text",
    )
    parser.add_argument("--text", required=True, help="Text string to render")
    parser.add_argument(
        "--font-query",
        required=True,
        help="Substring used to find a font file in repo fonts or C:\\Windows\\Fonts",
    )
    parser.add_argument("--font-size", type=int, required=True, help="Font size in px")
    parser.add_argument(
        "--tracking", type=int, default=0, help="Extra tracking to add between glyphs"
    )
    parser.add_argument(
        "--debug-prefix",
        type=Path,
        help="Optional path prefix for debug mask and crop images",
    )
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def to_hex(rgb: np.ndarray) -> str:
    return "#{:02X}{:02X}{:02X}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


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
    query = font_query.lower()
    filtered = [path for path in iter_font_paths() if query in path.name.lower()]
    if not filtered:
        raise FileNotFoundError(f"No font found for query: {font_query}")
    filtered.sort(key=lambda path: (len(path.name), str(path).lower()))
    return filtered[0]


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Image not found or unreadable: {path}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def crop_image(image: np.ndarray, crop: list[int]) -> np.ndarray:
    x1, y1, x2, y2 = crop
    return image[y1:y2, x1:x2]


def render_text_alpha(
    text: str,
    font_path: Path,
    font_size: int,
    tracking: int,
    target_shape: tuple[int, int],
) -> np.ndarray:
    target_height, target_width = target_shape
    canvas_width = target_width + 80
    canvas_height = target_height + 80
    canvas = Image.new("L", (canvas_width, canvas_height), 0)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(font_path), font_size)

    widths: list[int] = []
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        widths.append(bbox[2] - bbox[0])

    total_width = sum(widths) + max(len(text) - 1, 0) * tracking
    all_bbox = draw.textbbox((0, 0), text, font=font)
    total_height = all_bbox[3] - all_bbox[1]
    x = (canvas_width - total_width) // 2
    y = (canvas_height - total_height) // 2 - all_bbox[1]

    for index, char in enumerate(text):
        draw.text((x, y), char, fill=255, font=font)
        x += widths[index] + tracking

    alpha = np.array(canvas, dtype=np.float32) / 255.0
    rows, cols = np.where(alpha > 0)
    if len(rows) == 0 or len(cols) == 0:
        raise ValueError("Rendered text mask is empty")

    text_alpha = alpha[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]
    if text_alpha.shape[0] > target_height or text_alpha.shape[1] > target_width:
        raise ValueError("Rendered text exceeds the requested crop bounds")

    out = np.zeros((target_height, target_width), dtype=np.float32)
    offset_y = (target_height - text_alpha.shape[0]) // 2
    offset_x = (target_width - text_alpha.shape[1]) // 2
    out[
        offset_y : offset_y + text_alpha.shape[0],
        offset_x : offset_x + text_alpha.shape[1],
    ] = text_alpha
    return out


def sample_background(crop_rgb: np.ndarray, alpha_mask: np.ndarray) -> np.ndarray:
    binary = (alpha_mask > 0.2).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=2)
    outer = cv2.dilate(binary, kernel, iterations=5)
    ring = np.logical_and(outer == 1, dilated == 0)
    samples = crop_rgb[ring]
    if samples.size == 0:
        inverse = crop_rgb[binary == 0]
        if inverse.size == 0:
            return crop_rgb.reshape(-1, 3).mean(axis=0)
        return inverse.mean(axis=0)
    return samples.mean(axis=0)


def sample_core_text(crop_rgb: np.ndarray, alpha_mask: np.ndarray) -> np.ndarray:
    binary = (alpha_mask > 0.75).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    if eroded.sum() == 0:
        eroded = binary
    samples = crop_rgb[eroded == 1]
    if samples.size == 0:
        samples = crop_rgb[alpha_mask > 0.35]
    if samples.size == 0:
        samples = crop_rgb[alpha_mask > 0.05]
    return samples.mean(axis=0)


def solve_solid_fill(
    crop_rgb: np.ndarray, alpha_mask: np.ndarray, background_rgb: np.ndarray
) -> np.ndarray:
    active = alpha_mask > 0.05
    alpha = alpha_mask[active][:, None]
    observed = crop_rgb[active].astype(np.float32)
    background = background_rgb.astype(np.float32)[None, :]
    numerator = (alpha * (observed - (1.0 - alpha) * background)).sum(axis=0)
    denominator = np.maximum((alpha * alpha).sum(axis=0), 1e-6)
    color = numerator / denominator
    return np.clip(color, 0, 255)


def write_debug_images(
    prefix: Path, crop_rgb: np.ndarray, alpha_mask: np.ndarray, background_rgb: np.ndarray
) -> None:
    crop_path = Path(str(prefix) + "_crop.png")
    mask_path = Path(str(prefix) + "_mask.png")
    ring_path = Path(str(prefix) + "_ring.png")

    cv2.imwrite(str(crop_path), cv2.cvtColor(crop_rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(mask_path), (alpha_mask * 255).astype(np.uint8))

    binary = (alpha_mask > 0.2).astype(np.uint8)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=2)
    outer = cv2.dilate(binary, kernel, iterations=5)
    ring = np.logical_and(outer == 1, dilated == 0)
    ring_vis = crop_rgb.copy()
    ring_vis[ring] = background_rgb.astype(np.uint8)
    cv2.imwrite(str(ring_path), cv2.cvtColor(ring_vis, cv2.COLOR_RGB2BGR))


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    crop = list(args.crop)
    font_path = resolve_font_path(args.font_query)
    image_rgb = load_image(image_path)
    crop_rgb = crop_image(image_rgb, crop)
    alpha_mask = render_text_alpha(
        args.text,
        font_path,
        args.font_size,
        args.tracking,
        (crop_rgb.shape[0], crop_rgb.shape[1]),
    )

    background_rgb = sample_background(crop_rgb, alpha_mask)
    core_text_rgb = sample_core_text(crop_rgb, alpha_mask)
    solid_fill_rgb = solve_solid_fill(crop_rgb, alpha_mask, background_rgb)
    rendered_mean_rgb = crop_rgb[alpha_mask > 0.05].mean(axis=0)

    if args.debug_prefix:
        write_debug_images(resolve_path(args.debug_prefix), crop_rgb, alpha_mask, background_rgb)

    result = ColorPickResult(
        text=args.text,
        font_path=str(font_path),
        font_size=args.font_size,
        tracking=args.tracking,
        crop=crop,
        solid_fill_hex=to_hex(solid_fill_rgb),
        solid_fill_rgb=[int(round(channel)) for channel in solid_fill_rgb],
        rendered_text_mean_hex=to_hex(rendered_mean_rgb),
        rendered_text_mean_rgb=[int(round(channel)) for channel in rendered_mean_rgb],
        background_hex=to_hex(background_rgb),
        background_rgb=[int(round(channel)) for channel in background_rgb],
        core_text_mean_hex=to_hex(core_text_rgb),
        core_text_mean_rgb=[int(round(channel)) for channel in core_text_rgb],
    )
    print(json.dumps(asdict(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())