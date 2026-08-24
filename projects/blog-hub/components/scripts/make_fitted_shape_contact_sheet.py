from pathlib import Path
import io

import cairosvg
from PIL import Image, ImageDraw

root = Path("scripts", "shape_detection_round_complex", "layered")
items = [
    ("reference png", Path("components", "row_card", "round_complex.png")),
    ("current reconstruction", Path("components", "row_card", "round_complex.svg")),
    ("detected polygon svg", root.joinpath("detected_shapes.svg")),
    ("fitted debug svg", root.joinpath("fitted_shapes_debug.svg")),
    ("fitted clean svg", root.joinpath("fitted_shapes.svg")),
]


def load_visual(path: Path) -> Image.Image:
    if path.suffix.lower() == ".svg":
        png_bytes = cairosvg.svg2png(url=str(path))
        return Image.open(io.BytesIO(png_bytes)).convert("RGB")
    return Image.open(path).convert("RGB")

thumbs = []
for label, path in items:
    image = load_visual(path)
    canvas = Image.new("RGB", (360, 230), "white")
    image.thumbnail((330, 175), Image.Resampling.LANCZOS)
    x = (360 - image.width) // 2
    y = 38 + (175 - image.height) // 2
    canvas.paste(image, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 10), label, fill=(20, 20, 20))
    draw.text((12, 214), str(path), fill=(80, 80, 80))
    thumbs.append(canvas)

cols = 2
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 360, rows * 230), (245, 242, 232))
for index, thumb in enumerate(thumbs):
    x = (index % cols) * 360
    y = (index // cols) * 230
    sheet.paste(thumb, (x, y))

out = root.joinpath("fitted_shape_contact_sheet.png")
sheet.save(out)
print(out)
