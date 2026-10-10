import sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
src = sys.argv[1]; ch = int(sys.argv[2]) if len(sys.argv) > 2 else 1800; scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6
im = Image.open(src); w, h = im.size
outs = []
for i, y in enumerate(range(0, h, ch)):
    c = im.crop((0, y, w, min(h, y + ch)))
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    p = src.replace(".png", f"_{i}.jpg"); c.convert("RGB").save(p, quality=82); outs.append(p)
print("\n".join(outs))
