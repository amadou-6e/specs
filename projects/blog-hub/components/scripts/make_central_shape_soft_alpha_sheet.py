from pathlib import Path
import io
import json

import cairosvg
import numpy as np
from PIL import Image, ImageDraw

from fit_detected_shapes import component_mask_for_shape, image_size, load_json, load_source_rgb, render_element_alpha, soft_alpha_target

root = Path("scripts", "shape_detection_round_complex", "layered")
json_path = root.joinpath("detected_shapes.json")
report_path = root.joinpath("fitted_shapes_report.json")
payload = load_json(json_path)
report = json.loads(report_path.read_text(encoding="utf-8"))
shapes = payload["shapes"]
width, height = image_size(payload, shapes)
image_rgb = load_source_rgb(payload)
background = str(payload.get("background_color", "#FFFFFF"))
shape = next(item for item in shapes if int(item["id"]) == 3)
fit = next(item for item in report["fits"] if int(item["shape_id"]) == 3)
target_mask = component_mask_for_shape(json_path, shape, width, height, 40)
target_alpha = soft_alpha_target(image_rgb, target_mask, str(shape["color"]), background)
if target_alpha is None:
    target_alpha = (target_mask > 0).astype(np.float32)
candidate_alpha = render_element_alpha(width, height, fit["svg_element"].replace(str(shape["color"]), "white"), 4)
abs_diff = np.abs(target_alpha - candidate_alpha)

panels = []
for label, array in [
    ("soft target", target_alpha),
    ("candidate alpha", candidate_alpha),
    ("absolute diff", abs_diff / max(float(abs_diff.max()), 1e-6)),
]:
    image = Image.fromarray(np.clip(array * 255.0, 0, 255).astype(np.uint8)).convert("RGB")
    canvas = Image.new("RGB", (340, 220), "white")
    image.thumbnail((322, 170), Image.Resampling.NEAREST)
    canvas.paste(image, ((340 - image.width) // 2, 34))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 10), label, fill=(20, 20, 20))
    panels.append(canvas)

sheet = Image.new("RGB", (1020, 220), (245, 242, 232))
for index, panel in enumerate(panels):
    sheet.paste(panel, (index * 340, 0))
out = root.joinpath("central_shape_soft_alpha_sheet.png")
sheet.save(out)
print(out)
