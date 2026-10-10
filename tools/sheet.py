import sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
src = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 4; H = int(sys.argv[3]) if len(sys.argv) > 3 else 1800; sc = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7
im = Image.open(src).convert("RGB"); w, h = im.size; gap = 16
segs = [im.crop((0, y, w, min(h, y + H))) for y in range(0, h, H)]
outs = []
for i in range(0, len(segs), cols):
    grp = segs[i:i + cols]
    sheet = Image.new("RGB", (cols * w + (cols - 1) * gap, H), (200, 40, 120))
    for j, sgm in enumerate(grp): sheet.paste(sgm, (j * (w + gap), 0))
    sheet = sheet.resize((int(sheet.width * sc), int(sheet.height * sc)), Image.LANCZOS)
    p = src.replace(".png", f"_s{i // cols}.jpg"); sheet.save(p, quality=80); outs.append(p)
print(" ".join(outs))
