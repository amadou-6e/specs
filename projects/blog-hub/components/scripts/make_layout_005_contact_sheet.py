from pathlib import Path
import io

import cairosvg
from PIL import Image, ImageDraw

items = [
    ("original", Path("layouts", "005.png")),
    ("large regions overlay", Path("scripts", "shape_detection_layout_005", "regions", "detected_regions_overlay.png")),
    ("large regions svg", Path("scripts", "shape_detection_layout_005", "regions", "detected_regions.svg")),
    ("fine color islands svg", Path("scripts", "shape_detection_layout_005", "dominant", "detected_shapes.svg")),
]


def load_image(path: Path) -> Image.Image:
    if path.suffix.lower() == ".svg":
        png = cairosvg.svg2png(url=str(path))
        return Image.open(io.BytesIO(png)).convert("RGB")
    return Image.open(path).convert("RGB")

thumbs = []
for label, path in items:
    image = load_image(path)
    canvas = Image.new("RGB", (390, 540), "white")
    image.thumbnail((360, 460), Image.Resampling.LANCZOS)
    canvas.paste(image, ((390 - image.width) // 2, 46))
    draw = ImageDraw.Draw(canvas)
    draw.text((14, 14), label, fill=(20, 20, 20))
    draw.text((14, 516), str(path), fill=(80, 80, 80))
    thumbs.append(canvas)

sheet = Image.new("RGB", (780, 1080), (245, 242, 232))
for index, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((index % 2) * 390, (index // 2) * 540))
out = Path("scripts", "shape_detection_layout_005", "inspection_contact_sheet.png")
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(out)
