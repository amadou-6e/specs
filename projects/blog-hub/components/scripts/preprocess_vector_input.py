from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw


@dataclass(slots=True)
class TextRegion:
    id: int
    text: str
    confidence: float
    polygon: list[list[int]]
    x: int
    y: int
    width: int
    height: int


@dataclass(slots=True)
class ImageRegion:
    id: int
    source: str
    label: str
    confidence: float
    x: int
    y: int
    width: int
    height: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract/remove text and embedded image regions before vectorization.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--skip-ocr", action="store_true")
    parser.add_argument("--ocr-min-score", type=float, default=0.35)
    parser.add_argument("--text-pad", type=int, default=3)
    parser.add_argument("--image-pad", type=int, default=4)
    parser.add_argument("--image-detector", choices=["heuristic", "doclayout-yolo", "pp-doclayout", "grounding-dino", "owlv2", "none"], default="heuristic")
    parser.add_argument("--image-min-area", type=int, default=3500)
    parser.add_argument("--image-min-width", type=int, default=35)
    parser.add_argument("--image-min-height", type=int, default=35)
    parser.add_argument("--texture-threshold", type=float, default=0.46)
    parser.add_argument("--doclayout-conf", type=float, default=0.2)
    parser.add_argument("--doclayout-imgsz", type=int, default=1024)
    parser.add_argument("--pp-doclayout-model", default="PP-DocLayoutV2")
    parser.add_argument("--owlv2-threshold", type=float, default=0.16)
    parser.add_argument("--grounding-dino-box-threshold", type=float, default=0.25)
    parser.add_argument("--grounding-dino-text-threshold", type=float, default=0.20)
    parser.add_argument("--device", default="cuda:0")
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return Path.cwd().joinpath(path)


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def clamp_box(box: tuple[int, int, int, int], width: int, height: int, pad: int = 0) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    return (
        max(0, int(math.floor(x0 - pad))),
        max(0, int(math.floor(y0 - pad))),
        min(width, int(math.ceil(x1 + pad))),
        min(height, int(math.ceil(y1 + pad))),
    )


def polygon_to_box(polygon: list[list[int]]) -> tuple[int, int, int, int]:
    points = np.array(polygon, dtype=np.int32)
    x, y, width, height = cv2.boundingRect(points)
    return int(x), int(y), int(x + width), int(y + height)


def to_jsonable_polygons(value: Any) -> list[list[list[int]]]:
    if value is None:
        return []
    arr = np.array(value)
    if arr.ndim == 2 and arr.shape[1] == 2:
        arr = arr.reshape((1, arr.shape[0], 2))
    if arr.ndim != 3 or arr.shape[2] != 2:
        return []
    polygons: list[list[list[int]]] = []
    for polygon in arr:
        polygons.append([[int(round(float(x))), int(round(float(y)))] for x, y in polygon])
    return polygons


def page_get(page: Any, key: str) -> Any:
    if isinstance(page, dict):
        return page.get(key)
    if hasattr(page, "get"):
        try:
            return page.get(key)
        except Exception:
            pass
    return getattr(page, key, None)


def extract_text_regions_with_paddleocr(image_path: Path, min_score: float) -> list[TextRegion]:
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        device="cpu",
        enable_mkldnn=False,
    )
    if hasattr(ocr, "predict"):
        pages = ocr.predict(str(image_path))
    else:
        pages = ocr.ocr(str(image_path), cls=False)

    regions: list[TextRegion] = []
    next_id = 1
    for page in pages or []:
        polygons = to_jsonable_polygons(page_get(page, "rec_polys") or page_get(page, "dt_polys") or page_get(page, "boxes"))
        texts = page_get(page, "rec_texts") or page_get(page, "texts") or []
        scores = page_get(page, "rec_scores") or page_get(page, "scores") or []
        if not polygons and isinstance(page, list):
            for item in page:
                if not isinstance(item, (list, tuple)) or len(item) < 2:
                    continue
                polygon = [[int(round(float(x))), int(round(float(y)))] for x, y in item[0]]
                text = str(item[1][0]) if isinstance(item[1], (list, tuple)) and item[1] else ""
                score = float(item[1][1]) if isinstance(item[1], (list, tuple)) and len(item[1]) > 1 else 1.0
                if score < min_score:
                    continue
                x0, y0, x1, y1 = polygon_to_box(polygon)
                regions.append(TextRegion(next_id, text, score, polygon, x0, y0, x1 - x0, y1 - y0))
                next_id += 1
            continue
        for index, polygon in enumerate(polygons):
            text = str(texts[index]) if index < len(texts) else ""
            score = float(scores[index]) if index < len(scores) else 1.0
            if score < min_score:
                continue
            x0, y0, x1, y1 = polygon_to_box(polygon)
            regions.append(TextRegion(next_id, text, score, polygon, x0, y0, x1 - x0, y1 - y0))
            next_id += 1
    return regions


def local_entropy(gray: np.ndarray) -> np.ndarray:
    quantized = (gray // 16).astype(np.uint8)
    entropy = np.zeros(gray.shape, dtype=np.float32)
    padded = cv2.copyMakeBorder(quantized, 4, 4, 4, 4, cv2.BORDER_REFLECT)
    for y in range(gray.shape[0]):
        for x in range(gray.shape[1]):
            patch = padded[y : y + 9, x : x + 9]
            hist = np.bincount(patch.reshape(-1), minlength=16).astype(np.float32)
            prob = hist / max(float(np.sum(hist)), 1.0)
            keep = prob > 0
            entropy[y, x] = float(-np.sum(prob[keep] * np.log2(prob[keep]))) / 4.0
    return entropy


def detect_image_regions_heuristic(image_rgb: np.ndarray, text_mask: np.ndarray, args: argparse.Namespace) -> list[ImageRegion]:
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    entropy = local_entropy(gray)
    edges = cv2.Canny(gray, 50, 140)
    edge_density = cv2.blur((edges > 0).astype(np.float32), (15, 15))
    lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)
    lab_std = np.mean([cv2.blur((lab[:, :, c].astype(np.float32) ** 2), (11, 11)) - cv2.blur(lab[:, :, c].astype(np.float32), (11, 11)) ** 2 for c in range(3)], axis=0)
    lab_std = np.sqrt(np.maximum(lab_std, 0.0)) / 64.0
    score = np.clip(entropy * 0.58 + edge_density * 0.35 + lab_std * 0.25, 0.0, 1.0)
    mask = (score >= args.texture_threshold).astype(np.uint8) * 255
    mask[text_mask > 0] = 0
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel, iterations=1)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions: list[ImageRegion] = []
    height, width = gray.shape[:2]
    for contour in contours:
        area = int(cv2.contourArea(contour))
        if area < args.image_min_area:
            continue
        x, y, box_width, box_height = cv2.boundingRect(contour)
        if box_width < args.image_min_width or box_height < args.image_min_height:
            continue
        x0, y0, x1, y1 = clamp_box((x, y, x + box_width, y + box_height), width, height, args.image_pad)
        crop_score = float(np.mean(score[y0:y1, x0:x1])) if x1 > x0 and y1 > y0 else 0.0
        regions.append(ImageRegion(0, "heuristic_texture", "embedded_image_candidate", round(crop_score, 4), x0, y0, x1 - x0, y1 - y0))
    regions.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions


def detect_image_regions_doclayout(image_path: Path, args: argparse.Namespace) -> list[ImageRegion]:
    from doclayout_yolo import YOLOv10
    from huggingface_hub import hf_hub_download

    model_path = hf_hub_download(
        repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
        filename="doclayout_yolo_docstructbench_imgsz1024.pt",
    )
    model = YOLOv10(model_path)
    result = model.predict(str(image_path), imgsz=args.doclayout_imgsz, conf=args.doclayout_conf, device=args.device)[0]
    names = getattr(result, "names", {})
    regions: list[ImageRegion] = []
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return regions
    xyxy = boxes.xyxy.cpu().numpy()
    confidences = boxes.conf.cpu().numpy()
    classes = boxes.cls.cpu().numpy().astype(int)
    image_like_labels = {"figure", "picture", "image", "photo", "illustration", "figure_caption"}
    for index, box in enumerate(xyxy):
        label = str(names.get(int(classes[index]), classes[index])).lower()
        if label not in image_like_labels and not any(token in label for token in image_like_labels):
            continue
        x0, y0, x1, y1 = [int(round(float(value))) for value in box]
        regions.append(ImageRegion(0, "doclayout-yolo", label, round(float(confidences[index]), 4), x0, y0, x1 - x0, y1 - y0))
    regions.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions




def detect_image_regions_pp_doclayout(image_path: Path, args: argparse.Namespace) -> list[ImageRegion]:
    from paddlex import create_predictor
    from paddlex.inference import PaddlePredictorOption

    pp_option = PaddlePredictorOption(device_type="cpu", run_mode="paddle", enable_new_ir=False)
    predictor = create_predictor(model_name=args.pp_doclayout_model, pp_option=pp_option)
    results = list(predictor.predict(str(image_path)))
    if not results:
        return []
    regions: list[ImageRegion] = []
    for box in results[0].get("boxes", []):
        label = str(box.get("label", "")).lower()
        if "image" not in label and "figure" not in label and "vision" not in label:
            continue
        x0, y0, x1, y1 = [int(round(float(value))) for value in box.get("coordinate", [])]
        if x1 <= x0 or y1 <= y0:
            continue
        regions.append(
            ImageRegion(
                id=0,
                source=f"pp-doclayout:{args.pp_doclayout_model}",
                label=label,
                confidence=round(float(box.get("score", 0.0)), 4),
                x=x0,
                y=y0,
                width=x1 - x0,
                height=y1 - y0,
            )
        )
    regions.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions

def detect_image_regions_grounding_dino(image_path: Path, args: argparse.Namespace) -> list[ImageRegion]:
    import torch
    from PIL import Image
    from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

    device = args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu"
    model_id = "IDEA-Research/grounding-dino-base"
    processor = AutoProcessor.from_pretrained(model_id)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id).to(device)
    image = Image.open(image_path).convert("RGB")
    text = "a photograph. a product photo. an embedded image. a picture. a raster image."
    inputs = processor(images=image, text=text, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        box_threshold=args.grounding_dino_box_threshold,
        text_threshold=args.grounding_dino_text_threshold,
        target_sizes=[image.size[::-1]],
    )[0]
    regions: list[ImageRegion] = []
    boxes = results.get("boxes", [])
    scores = results.get("scores", [])
    labels = results.get("labels", [])
    for index, box in enumerate(boxes):
        score = float(scores[index].item()) if hasattr(scores[index], "item") else float(scores[index])
        label = str(labels[index]) if index < len(labels) else "grounded_image"
        x0, y0, x1, y1 = [int(round(float(value))) for value in box.tolist()]
        regions.append(ImageRegion(0, "grounding-dino", label, round(score, 4), x0, y0, x1 - x0, y1 - y0))
    regions.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions

def detect_image_regions_owlv2(image_path: Path, args: argparse.Namespace) -> list[ImageRegion]:
    import torch
    from transformers import Owlv2ForObjectDetection, Owlv2Processor

    device = args.device if torch.cuda.is_available() and args.device.startswith("cuda") else "cpu"
    model_id = "google/owlv2-base-patch16-ensemble"
    processor = Owlv2Processor.from_pretrained(model_id)
    model = Owlv2ForObjectDetection.from_pretrained(model_id).to(device)
    image = Image.open(image_path).convert("RGB")
    prompts = [["a photo", "an image", "a picture", "an illustration", "a screenshot panel"]]
    inputs = processor(text=prompts, images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]], device=device)
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=args.owlv2_threshold)[0]
    regions: list[ImageRegion] = []
    for index, box in enumerate(results["boxes"]):
        label_index = int(results["labels"][index].item())
        label = prompts[0][label_index]
        score = float(results["scores"][index].item())
        x0, y0, x1, y1 = [int(round(float(value))) for value in box.tolist()]
        regions.append(ImageRegion(0, "owlv2", label, round(score, 4), x0, y0, x1 - x0, y1 - y0))
    regions.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(regions, start=1):
        region.id = index
    return regions



def region_box(region: ImageRegion) -> tuple[int, int, int, int]:
    return region.x, region.y, region.x + region.width, region.y + region.height


def box_area(box: tuple[int, int, int, int]) -> int:
    x0, y0, x1, y1 = box
    return max(0, x1 - x0) * max(0, y1 - y0)


def box_intersection(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    x0 = max(a[0], b[0])
    y0 = max(a[1], b[1])
    x1 = min(a[2], b[2])
    y1 = min(a[3], b[3])
    return max(0, x1 - x0) * max(0, y1 - y0)


def merge_image_regions(regions: list[ImageRegion], containment: float = 0.86, iou_threshold: float = 0.65) -> list[ImageRegion]:
    kept: list[ImageRegion] = []
    for candidate in sorted(regions, key=lambda item: (item.confidence, item.width * item.height), reverse=True):
        candidate_box = region_box(candidate)
        candidate_area = max(box_area(candidate_box), 1)
        duplicate = False
        for kept_region in list(kept):
            kept_box = region_box(kept_region)
            kept_area = max(box_area(kept_box), 1)
            intersection = box_intersection(candidate_box, kept_box)
            union = candidate_area + kept_area - intersection
            iou = intersection / max(union, 1)
            candidate_inside_kept = intersection / candidate_area
            kept_inside_candidate = intersection / kept_area
            if iou >= iou_threshold:
                duplicate = True
                break
            if candidate_inside_kept >= containment and candidate.confidence <= kept_region.confidence:
                duplicate = True
                break
            if kept_inside_candidate >= containment and candidate.confidence <= kept_region.confidence:
                duplicate = True
                break
            if kept_inside_candidate >= containment and candidate.confidence > kept_region.confidence:
                kept.remove(kept_region)
        if not duplicate:
            kept.append(candidate)
    kept.sort(key=lambda item: (item.y, item.x))
    for index, region in enumerate(kept, start=1):
        region.id = index
    return kept


def refine_learned_regions_with_texture(
    image_rgb: np.ndarray,
    text_mask: np.ndarray,
    learned_regions: list[ImageRegion],
    args: argparse.Namespace,
) -> list[ImageRegion]:
    if not learned_regions:
        return learned_regions
    texture_regions = detect_image_regions_heuristic(image_rgb, text_mask, args)
    if not texture_regions:
        return learned_regions

    refined: list[ImageRegion] = []
    for learned in learned_regions:
        learned_box = region_box(learned)
        learned_area = max(box_area(learned_box), 1)
        contained_textures: list[ImageRegion] = []
        for texture in texture_regions:
            texture_box = region_box(texture)
            texture_area = max(box_area(texture_box), 1)
            intersection = box_intersection(learned_box, texture_box)
            texture_inside_learned = intersection / texture_area
            learned_covered = intersection / learned_area
            if texture_inside_learned >= 0.65 and learned_covered >= 0.025:
                contained_textures.append(texture)

        if not contained_textures:
            refined.append(learned)
            continue

        texture_area_total = sum(max(item.width * item.height, 1) for item in contained_textures)
        is_oversized_section = learned_area / max(texture_area_total, 1) >= 2.4
        if is_oversized_section:
            for texture in contained_textures:
                refined.append(
                    ImageRegion(
                        id=0,
                        source=f"{learned.source}+texture_refined",
                        label=f"{learned.label}:texture_subregion",
                        confidence=round(max(learned.confidence, texture.confidence), 4),
                        x=texture.x,
                        y=texture.y,
                        width=texture.width,
                        height=texture.height,
                    )
                )
        else:
            refined.append(learned)

    return refined

def draw_masks(shape: tuple[int, int], text_regions: list[TextRegion], image_regions: list[ImageRegion], text_pad: int, image_pad: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    height, width = shape
    text_mask = np.zeros((height, width), dtype=np.uint8)
    image_mask = np.zeros((height, width), dtype=np.uint8)
    for region in text_regions:
        polygon = np.array(region.polygon, dtype=np.int32)
        cv2.fillPoly(text_mask, [polygon], 255)
    if text_pad > 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (text_pad * 2 + 1, text_pad * 2 + 1))
        text_mask = cv2.dilate(text_mask, kernel, iterations=1)
    for region in image_regions:
        x0, y0, x1, y1 = clamp_box((region.x, region.y, region.x + region.width, region.y + region.height), width, height, image_pad)
        image_mask[y0:y1, x0:x1] = 255
    combined = cv2.bitwise_or(text_mask, image_mask)
    return text_mask, image_mask, combined


def estimate_fill_color(image_rgb: np.ndarray, mask: np.ndarray) -> tuple[int, int, int]:
    height, width = mask.shape[:2]
    border = np.zeros((height, width), dtype=np.uint8)
    border[0, :] = 255
    border[-1, :] = 255
    border[:, 0] = 255
    border[:, -1] = 255
    candidates = image_rgb[(mask == 0) & (border > 0)]
    if len(candidates) == 0:
        candidates = image_rgb[mask == 0]
    if len(candidates) == 0:
        return (255, 255, 255)
    median = np.median(candidates, axis=0)
    return tuple(int(round(float(value))) for value in median)


def fill_masked_background(image_rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    output = image_rgb.copy()
    fill = estimate_fill_color(image_rgb, mask)
    output[mask > 0] = fill
    return output


def inpaint_mask(image_rgb: np.ndarray, mask: np.ndarray) -> np.ndarray:
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    inpainted = cv2.inpaint(image_bgr, mask, 3, cv2.INPAINT_TELEA)
    return cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)


def save_region_crops(image_rgb: np.ndarray, out_dir: Path, text_regions: list[TextRegion], image_regions: list[ImageRegion]) -> None:
    text_dir = out_dir.joinpath("text_crops")
    image_dir = out_dir.joinpath("image_crops")
    text_dir.mkdir(exist_ok=True)
    image_dir.mkdir(exist_ok=True)
    height, width = image_rgb.shape[:2]
    pil_image = Image.fromarray(image_rgb)
    for region in text_regions:
        x0, y0, x1, y1 = clamp_box((region.x, region.y, region.x + region.width, region.y + region.height), width, height, 2)
        pil_image.crop((x0, y0, x1, y1)).save(text_dir.joinpath(f"text_{region.id:03d}.png"))
    for region in image_regions:
        x0, y0, x1, y1 = clamp_box((region.x, region.y, region.x + region.width, region.y + region.height), width, height, 2)
        pil_image.crop((x0, y0, x1, y1)).save(image_dir.joinpath(f"image_{region.id:03d}.png"))


def write_overlay(path: Path, image_rgb: np.ndarray, text_regions: list[TextRegion], image_regions: list[ImageRegion]) -> None:
    image = Image.fromarray(image_rgb).convert("RGB")
    draw = ImageDraw.Draw(image)
    for region in image_regions:
        box = (region.x, region.y, region.x + region.width, region.y + region.height)
        draw.rectangle(box, outline=(0, 168, 255), width=4)
        draw.text((region.x + 4, region.y + 4), f"image #{region.id} {region.label} {region.confidence:.2f}", fill=(0, 168, 255))
    for region in text_regions:
        polygon = [tuple(point) for point in region.polygon]
        draw.line(polygon + [polygon[0]], fill=(255, 46, 136), width=2)
        draw.text((region.x + 2, region.y + 2), f"text #{region.id}", fill=(255, 46, 136))
    image.save(path)


def main() -> int:
    args = parse_args()
    image_path = resolve_path(args.image)
    out_dir = resolve_path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    image_rgb = load_rgb(image_path)
    height, width = image_rgb.shape[:2]

    text_regions: list[TextRegion] = []
    ocr_error = None
    if not args.skip_ocr:
        try:
            text_regions = extract_text_regions_with_paddleocr(image_path, args.ocr_min_score)
        except Exception as exc:
            ocr_error = repr(exc)

    preliminary_text_mask, _, _ = draw_masks((height, width), text_regions, [], args.text_pad, args.image_pad)
    image_regions: list[ImageRegion] = []
    image_detector_error = None
    try:
        if args.image_detector == "heuristic":
            image_regions = detect_image_regions_heuristic(image_rgb, preliminary_text_mask, args)
        elif args.image_detector == "doclayout-yolo":
            image_regions = detect_image_regions_doclayout(image_path, args)
            image_regions = refine_learned_regions_with_texture(image_rgb, preliminary_text_mask, image_regions, args)
        elif args.image_detector == "pp-doclayout":
            image_regions = detect_image_regions_pp_doclayout(image_path, args)
            image_regions = refine_learned_regions_with_texture(image_rgb, preliminary_text_mask, image_regions, args)
        elif args.image_detector == "grounding-dino":
            image_regions = detect_image_regions_grounding_dino(image_path, args)
            image_regions = refine_learned_regions_with_texture(image_rgb, preliminary_text_mask, image_regions, args)
        elif args.image_detector == "owlv2":
            image_regions = detect_image_regions_owlv2(image_path, args)
            image_regions = refine_learned_regions_with_texture(image_rgb, preliminary_text_mask, image_regions, args)
    except Exception as exc:
        image_detector_error = repr(exc)

    image_regions = [region for region in image_regions if region.width >= args.image_min_width and region.height >= args.image_min_height and region.width * region.height >= args.image_min_area]
    image_regions = merge_image_regions(image_regions)
    text_mask, image_mask, combined_mask = draw_masks((height, width), text_regions, image_regions, args.text_pad, args.image_pad)
    masked_background = fill_masked_background(image_rgb, combined_mask)
    inpainted = inpaint_mask(image_rgb, combined_mask)

    Image.fromarray(text_mask).save(out_dir.joinpath("text_mask.png"))
    Image.fromarray(image_mask).save(out_dir.joinpath("image_mask.png"))
    Image.fromarray(combined_mask).save(out_dir.joinpath("combined_mask.png"))
    Image.fromarray(masked_background).save(out_dir.joinpath("masked_background.png"))
    Image.fromarray(inpainted).save(out_dir.joinpath("inpainted.png"))
    write_overlay(out_dir.joinpath("detected_regions_overlay.png"), image_rgb, text_regions, image_regions)
    save_region_crops(image_rgb, out_dir, text_regions, image_regions)

    payload = {
        "image": str(image_path),
        "width": width,
        "height": height,
        "ocr_error": ocr_error,
        "image_detector": args.image_detector,
        "image_detector_error": image_detector_error,
        "text_region_count": len(text_regions),
        "image_region_count": len(image_regions),
        "text_regions": [asdict(region) for region in text_regions],
        "image_regions": [asdict(region) for region in image_regions],
        "outputs": {
            "text_mask": str(out_dir.joinpath("text_mask.png")),
            "image_mask": str(out_dir.joinpath("image_mask.png")),
            "combined_mask": str(out_dir.joinpath("combined_mask.png")),
            "masked_background": str(out_dir.joinpath("masked_background.png")),
            "inpainted": str(out_dir.joinpath("inpainted.png")),
            "overlay": str(out_dir.joinpath("detected_regions_overlay.png")),
        },
    }
    out_dir.joinpath("preprocess_regions.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())