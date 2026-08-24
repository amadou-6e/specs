from pathlib import Path
import io
import json

import cairosvg
import numpy as np
from PIL import Image

from fit_detected_shapes import component_mask_for_shape, image_size, load_json

root = Path("scripts", "shape_detection_round_complex", "layered")
json_path = root.joinpath("detected_shapes.json")
report_path = root.joinpath("fitted_shapes_report.json")
payload = load_json(json_path)
report = json.loads(report_path.read_text(encoding="utf-8"))
shapes = payload["shapes"]
width, height = image_size(payload, shapes)
shape = next(item for item in shapes if int(item["id"]) == 3)
fit = next(item for item in report["fits"] if int(item["shape_id"]) == 3)
target = component_mask_for_shape(json_path, shape, width, height, 40) > 0
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><rect width="100%" height="100%" fill="black"/>{fit["svg_element"].replace("#566129", "white")}</svg>'
png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=width, output_height=height)
candidate = np.array(Image.open(io.BytesIO(png)).convert("L")) > 127
visual = np.zeros((height, width, 3), dtype=np.uint8)
visual[:, :] = np.array([235, 225, 205], dtype=np.uint8)
visual[target & candidate] = np.array([70, 180, 90], dtype=np.uint8)
visual[target & ~candidate] = np.array([240, 80, 80], dtype=np.uint8)
visual[~target & candidate] = np.array([70, 130, 240], dtype=np.uint8)
out = root.joinpath("central_shape_fit_diff.png")
Image.fromarray(visual).save(out)
print(out)
