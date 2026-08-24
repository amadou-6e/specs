from pathlib import Path
import io

import cairosvg
from PIL import Image, ImageDraw

root = Path("scripts", "shape_detection_layout_005", "flat_regions")
items = [
    ("original", Path("layouts", "005.png")),
    ("superpixels: green flat / red textured", root.joinpath("superpixel_classification_overlay.png")),
    ("all flat fragments", root.joinpath("flat_regions_overlay.png")),
    ("simple flat only", root.joinpath("simple_flat_regions_overlay.png")),
    ("all flat svg", root.joinpath("flat_regions.svg")),
    ("simple flat svg", root.joinpath("simple_flat_regions.svg")),
    ("text fragments overlay", root.joinpath("text_fragments_overlay.png")),
    ("text fragments svg", root.joinpath("text_fragments.svg")),
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

sheet = Image.new("RGB", (780, 2160), (245, 242, 232))
for index, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((index % 2) * 390, (index // 2) * 540))
out = root.joinpath("inspection_contact_sheet.png")
sheet.save(out)
print(out)

