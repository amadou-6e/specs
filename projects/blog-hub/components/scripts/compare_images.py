from __future__ import annotations

import argparse
import tempfile
from dataclasses import dataclass
from pathlib import Path

import cairosvg
import cv2
import numpy as np


@dataclass(slots=True)
class ComparisonResult:
    identical: bool
    width: int
    height: int
    total_pixels: int
    different_pixels: int
    difference_ratio: float
    total_delta: int
    max_delta: int
    diff_image: Path
    image_a: Path
    image_b: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two raster images and write a per-pixel diff image."
    )
    parser.add_argument("image_a", type=Path, help="First image path")
    parser.add_argument("image_b", type=Path, help="Second image path")
    parser.add_argument(
        "--diff-output",
        type=Path,
        default=Path("image_diff.png"),
        help="Where to write the diff PNG",
    )
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else Path.cwd().joinpath(path)


def load_image(path: Path) -> np.ndarray:
    if path.suffix.lower() == ".svg":
        return load_svg_image(path)

    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"Image not found or unreadable: {path}")
    return image


def load_svg_image(path: Path) -> np.ndarray:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        temp_png_path = Path(handle.name)

    try:
        cairosvg.svg2png(url=str(path), write_to=str(temp_png_path))
        image = cv2.imread(str(temp_png_path), cv2.IMREAD_UNCHANGED)
        if image is None:
            raise FileNotFoundError(f"SVG could not be rasterized: {path}")
        return image
    finally:
        if temp_png_path.exists():
            temp_png_path.unlink()


def to_bgra(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)
    if image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    if image.shape[2] == 4:
        return image
    raise ValueError(f"Unsupported channel count: {image.shape[2]}")


def compare_images(
    image_a_path: Path, image_b_path: Path, diff_output_path: Path
) -> ComparisonResult:
    image_a = to_bgra(load_image(image_a_path))
    image_b = to_bgra(load_image(image_b_path))

    if image_a.shape != image_b.shape:
        raise ValueError(
            "Images must have the same dimensions and channel layout. "
            f"Left={image_a.shape}, Right={image_b.shape}"
        )

    diff = cv2.absdiff(image_a, image_b)
    changed_mask = np.any(diff != 0, axis=2)

    different_pixels = int(np.count_nonzero(changed_mask))
    total_pixels = int(changed_mask.size)
    total_delta = int(diff.astype(np.uint64).sum())
    per_pixel_delta = diff.astype(np.uint16).sum(axis=2)
    max_delta = int(per_pixel_delta.max()) if per_pixel_delta.size else 0

    diff_for_write = diff.copy()
    diff_for_write[~changed_mask] = np.array([0, 0, 0, 0], dtype=np.uint8)
    diff_for_write[changed_mask, 3] = 255

    diff_output_path.parent.mkdir(parents=True, exist_ok=True)
    success = cv2.imwrite(str(diff_output_path), diff_for_write)
    if not success:
        raise RuntimeError(f"Failed to write diff image: {diff_output_path}")

    height, width = image_a.shape[:2]
    difference_ratio = 0.0 if total_pixels == 0 else different_pixels / total_pixels

    return ComparisonResult(
        identical=different_pixels == 0,
        width=width,
        height=height,
        total_pixels=total_pixels,
        different_pixels=different_pixels,
        difference_ratio=difference_ratio,
        total_delta=total_delta,
        max_delta=max_delta,
        diff_image=diff_output_path,
        image_a=image_a_path,
        image_b=image_b_path,
    )


def print_result(result: ComparisonResult) -> None:
    print(f"identical: {result.identical}")
    print(f"width: {result.width}")
    print(f"height: {result.height}")
    print(f"total_pixels: {result.total_pixels}")
    print(f"different_pixels: {result.different_pixels}")
    print(f"difference_ratio: {result.difference_ratio:.6f}")
    print(f"total_delta: {result.total_delta}")
    print(f"max_delta: {result.max_delta}")
    print(f"diff_image: {result.diff_image}")
    print(f"image_a: {result.image_a}")
    print(f"image_b: {result.image_b}")


def main() -> int:
    args = parse_args()
    image_a_path = resolve_path(args.image_a)
    image_b_path = resolve_path(args.image_b)
    diff_output_path = resolve_path(args.diff_output)

    result = compare_images(image_a_path, image_b_path, diff_output_path)
    print_result(result)
    return 0 if result.identical else 1


if __name__ == "__main__":
    raise SystemExit(main())

