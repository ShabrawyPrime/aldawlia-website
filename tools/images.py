"""Build responsive WebP variants for every registered photo.

    python3 tools/images.py build/img            # new or missing photos only (keeps the rest)
    python3 tools/images.py build/img --all      # rebuild everything (needs every source photo)

Photos whose key is no longer in content/images.py are removed from the output folder.
"""
import sys, os, json, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from PIL import Image, ImageOps, ImageChops
from content.images import IMAGES

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.join(ROOT, "build", "img")
ALL = "--all" in sys.argv
os.makedirs(OUT, exist_ok=True)
HERO = {"piping", "machine_room", "frosty_solar", "frosty_roof", "compressors", "founder", "js_factory", "ggg_install", "epc1", "neo_products", "compressor_macro"}
WIDE = {"r3d_plant", "r3d_potato", "r3d_solar", "r3d_site", "r3d_dabaa", "r3d_frosty"}   # full-width 3D drawings with callouts
TRIM = {"js_bipv", "nova_compressor", "js_academy"}

meta_path = os.path.join(OUT, "images.json")
meta = {} if ALL or not os.path.exists(meta_path) else json.load(open(meta_path, encoding="utf-8"))

# drop photos that left the registry
for key in [k for k in meta if k not in IMAGES]:
    for f in glob.glob(os.path.join(OUT, f"{key}-*.webp")):
        os.remove(f)
    del meta[key]
    print("removed", key)

done = 0
for key, (src, focal, alt) in IMAGES.items():
    have = key in meta and all(os.path.exists(os.path.join(OUT, f"{key}-{w}.webp")) for w in meta[key]["widths"])
    if have:
        meta[key]["focal"] = focal          # focal points can change without reprocessing
        continue
    im = Image.open(src); im = ImageOps.exif_transpose(im).convert("RGB")
    if key in TRIM:
        # remove a flat white border left over from the brochure layout
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg).convert("L").point(lambda v: 255 if v > 18 else 0)
        bbox = diff.getbbox()
        if bbox: im = im.crop(bbox)
    w, h = im.size
    cand = [1100, 2200] if key in HERO else [960, 1600, 2400] if key in WIDE else [800, 1600]
    widths = sorted(set(min(x, w) for x in cand))
    out = []
    for tw in widths:
        th = round(h * tw / w)
        r = im.resize((tw, th), Image.LANCZOS) if tw != w else im
        fn = f"{key}-{tw}.webp"
        r.save(os.path.join(OUT, fn), "WEBP", quality=74 if tw >= 1600 else 78, method=6)
        out.append(tw)
    meta[key] = {"w": w, "h": h, "widths": out, "focal": focal}
    done += 1
    print("built", key, out)

json.dump(meta, open(meta_path, "w", encoding="utf-8"), indent=0)
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print(done, "built,", len(meta), "images,", round(tot / 1e6, 2), "MB")
