from pathlib import Path

from PIL import Image, ImageDraw

root = Path("scripts", "shape_detection_round_complex", "layered")
items = [
    ("reference", Path("components", "row_card", "round_complex.png")),
    ("overlay", root.joinpath("detected_shapes_overlay.png")),
    ("layer 1 raw", root.joinpath("layer_1_566129_raw_mask.png")),
    ("layer 1 repaired", root.joinpath("layer_1_566129_repaired_mask.png")),
    ("layer 2 raw", root.joinpath("layer_2_566129_raw_mask.png")),
    ("layer 2 repaired", root.joinpath("layer_2_566129_repaired_mask.png")),
]
thumbs = []
for label, path in items:
    image = Image.open(path).convert("RGB")
    canvas = Image.new("RGB", (340, 220), "white")
    image.thumbnail((320, 170), Image.Resampling.LANCZOS)
    x = (340 - image.width) // 2
    canvas.paste(image, (x, 34))
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 10), label, fill=(20, 20, 20))
    thumbs.append(canvas)

sheet = Image.new("RGB", (680, 660), (245, 242, 232))
for index, thumb in enumerate(thumbs):
    x = (index % 2) * 340
    y = (index // 2) * 220
    sheet.paste(thumb, (x, y))

out = root.joinpath("inspection_contact_sheet.png")
sheet.save(out)
print(out)
