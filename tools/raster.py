"""Render the website icons and the Open Graph (link preview) cards.

Icons use the Aldawlia emblem (build/logos/aldawlia.png): the favicon shows the globe and snowflake on a white
tile (the name is unreadable at 16-32 px), the app icons show the whole emblem on white.
The link preview cards centre the emblem, so it stays in view when an app crops the card to a square.

    python3 tools/raster.py
"""
import os, io, base64, json, tempfile
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "build", "brand"); F = os.path.join(ROOT, "build", "fonts")
IMG = os.path.join(ROOT, "build", "img"); LOGOS = os.path.join(ROOT, "build", "logos")
PIPW = json.load(open(os.path.join(IMG, "images.json"), encoding="utf-8"))["piping"]["widths"][-1]
EMBLEM = Image.open(os.path.join(LOGOS, "aldawlia.png")).convert("RGBA")
SYMBOL = EMBLEM.crop((0, 0, EMBLEM.width, 262))          # globe, roofline and snowflake, without the name band


def tile(size, art, pad, radius):
    """art centred on a white square (radius as a fraction of the size), drawn at 4x and reduced."""
    S = size * 4
    c = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((0, 0, S - 1, S - 1), radius=int(S * radius), fill=(255, 255, 255, 255))
    box = S * (1 - 2 * pad)
    k = min(box / art.width, box / art.height)
    a = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    c.alpha_composite(a, ((S - a.width) // 2, (S - a.height) // 2))
    return c.resize((size, size), Image.LANCZOS)


# favicon (rounded white tile, symbol only) and app icons (square white, whole emblem; iOS and Android mask them)
tile(32, SYMBOL, 0.04, 0.18).save(os.path.join(B, "favicon-32.png"), optimize=True)
fav96 = tile(96, SYMBOL, 0.04, 0.18)
buf = io.BytesIO(); fav96.save(buf, "PNG", optimize=True)
open(os.path.join(B, "favicon.svg"), "w", encoding="utf-8").write(
    '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 96 96">'
    f'<image width="96" height="96" href="data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"/></svg>')
for size, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
    tile(size, EMBLEM, 0.08, 0).convert("RGB").save(os.path.join(B, name), optimize=True)

en = open(os.path.join(B, "aldawlia-en-light.svg"), encoding="utf-8").read()
ar = open(os.path.join(B, "aldawlia-ar-light.svg"), encoding="utf-8").read()
emb = "file://" + os.path.join(LOGOS, "aldawlia.png")


def og_html(lang):
    sub = ("Industrial refrigeration · Turnkey EPC · Solar energy · Since 1983" if lang == "en"
           else "التبريد الصناعي · مشروعات تسليم المفتاح · الطاقة الشمسية · منذ 1983")
    d = "rtl" if lang == "ar" else "ltr"
    return f"""<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Plex';font-weight:500;src:url(file://{F}/ibm-plex-sans-latin-500-normal.woff2)}}
@font-face{{font-family:'PlexAr';font-weight:500;src:url(file://{F}/ibm-plex-sans-arabic-arabic-500-normal.woff2)}}
html,body{{margin:0;width:1200px;height:630px;background:#070B14;overflow:hidden}}
.bg{{position:absolute;inset:0;background:url(file://{IMG}/piping-{PIPW}.webp) center/cover}}
.v{{position:absolute;inset:0;background:radial-gradient(60% 75% at 50% 45%,rgba(7,11,20,.80) 0%,rgba(7,11,20,.93) 70%)}}
.g{{position:absolute;inset:0;background-image:linear-gradient(to right,rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.05) 1px,transparent 1px);background-size:96px 96px}}
.c{{position:absolute;inset:0 0 8px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px}}
.t{{background:#FFFFFF;border-radius:24px;padding:18px 22px;box-shadow:0 18px 50px rgba(0,0,0,.45)}}
.t img{{display:block;width:300px;height:auto}}
.c svg{{height:{'44' if lang == 'en' else '52'}px;width:auto}}
p{{font:500 {'22px' if lang == 'en' else '24px'}/1.4 {'Plex' if lang == 'en' else 'PlexAr'},sans-serif;color:#93A4BD;margin:-8px 0 0}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient({'90deg' if lang == 'en' else '270deg'},#22D3EE,#F6B61D)}}
</style></head><body><div class="bg"></div><div class="v"></div><div class="g"></div>
<div class="c"><div class="t"><img src="{emb}" alt=""></div>{en if lang == 'en' else ar}<p>{sub}</p></div><div class="bar"></div></body></html>"""


with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in ["en", "ar"]:
        tmp = os.path.join(tempfile.gettempdir(), f"og-{lang}.html")
        open(tmp, "w", encoding="utf-8").write(og_html(lang))
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(f"file://{tmp}"); pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(B, f"og-{lang}.jpg"), type="jpeg", quality=88); pg.close()
    b.close()
print(sorted(os.listdir(B)))
