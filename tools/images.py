"""Build responsive WebP variants for every registered photo."""
import sys, os, json
sys.path.insert(0, "/home/claude/site")
from PIL import Image, ImageOps
from content.images import IMAGES
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
WIDTHS = [480, 960, 1600, 2200]
HERO = {"piping", "machine_room", "frosty_solar", "frosty_roof", "compressors", "founder", "js_factory", "ggg_install", "epc1", "neo_products", "compressor_macro"}
TRIM = {"js_bipv", "nova_compressor", "js_academy"}
meta = {}
for key, (src, focal, alt) in IMAGES.items():
    im = Image.open(src); im = ImageOps.exif_transpose(im).convert("RGB")
    if key in TRIM:
        # remove a flat white border left over from the brochure layout
        from PIL import ImageChops
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0)
        bbox = diff.getbbox()
        if bbox: im = im.crop(bbox)
    w, h = im.size
    cand = [1100, 2200] if key in HERO else [800, 1600]
    widths = sorted(set(min(x, w) for x in cand))
    out = []
    for tw in widths:
        th = round(h * tw / w)
        r = im.resize((tw, th), Image.LANCZOS) if tw != w else im
        fn = f"{key}-{tw}.webp"
        r.save(os.path.join(OUT, fn), "WEBP", quality=74 if tw >= 1600 else 78, method=6)
        out.append(tw)
    meta[key] = {"w": w, "h": h, "widths": out, "focal": focal}
json.dump(meta, open(os.path.join(OUT, "images.json"), "w"), indent=0)
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print(len(meta), "images,", round(tot/1e6, 2), "MB")
