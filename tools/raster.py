"""Render favicons and Open Graph cards from the brand SVGs (Playwright)."""
import os, sys, shutil, json
from playwright.sync_api import sync_playwright
B = "/home/claude/site/build/brand"; FS = "/home/claude/tools/node_modules/@fontsource"
IMG = "/home/claude/site/build/img"
PIPW = json.load(open(IMG + "/images.json"))["piping"]["widths"][-1]
shutil.copy2(f"{B}/monogram.svg", f"{B}/favicon.svg")
mono = open(f"{B}/monogram.svg").read()
en = open(f"{B}/group-en-light.svg").read(); ar = open(f"{B}/group-ar-light.svg").read()
def og_html(lang):
    tag = "We build the infrastructure of the future." if lang == "en" else "نبني البنية التحتية للمستقبل."
    sub = "Industrial refrigeration · Turnkey EPC · Solar energy · Since 1983" if lang == "en" else "التبريد الصناعي · مشروعات تسليم المفتاح · الطاقة الشمسية · منذ 1983"
    d = "rtl" if lang == "ar" else "ltr"
    fam = "'Readex Pro'" if lang == "ar" else "'Space Grotesk'"
    return f"""<!doctype html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8"><style>
@font-face{{font-family:'Space Grotesk';font-weight:700;src:url(file://{FS}/space-grotesk/files/space-grotesk-latin-700-normal.woff2)}}
@font-face{{font-family:'Readex Pro';font-weight:700;src:url(file://{FS}/readex-pro/files/readex-pro-arabic-700-normal.woff2)}}
@font-face{{font-family:'Plex';font-weight:500;src:url(file://{FS}/ibm-plex-sans/files/ibm-plex-sans-latin-500-normal.woff2)}}
@font-face{{font-family:'PlexAr';font-weight:500;src:url(file://{FS}/ibm-plex-sans-arabic/files/ibm-plex-sans-arabic-arabic-500-normal.woff2)}}
html,body{{margin:0;width:1200px;height:630px;background:#070B14;overflow:hidden}}
.bg{{position:absolute;inset:0;background:url(file://{IMG}/piping-{PIPW}.webp) center/cover}}
.v{{position:absolute;inset:0;background:linear-gradient({'90deg' if lang=='en' else '270deg'},rgba(7,11,20,.97) 0%,rgba(7,11,20,.86) 48%,rgba(7,11,20,.35) 100%)}}
.g{{position:absolute;inset:0;background-image:linear-gradient(to right,rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(255,255,255,.05) 1px,transparent 1px);background-size:96px 96px}}
.c{{position:absolute;inset:72px;display:flex;flex-direction:column;justify-content:space-between}}
.c svg{{height:{'40' if lang=='en' else '50'}px;width:auto;align-self:flex-start}}
h1{{font:700 {'76px/1.0' if lang=='en' else '66px/1.3'} {fam},sans-serif;letter-spacing:{'-2.5px' if lang=='en' else '0'};color:#EEF3FA;margin:0;max-width:820px}}
p{{font:500 {'22px' if lang=='en' else '24px'}/1.4 {'Plex' if lang=='en' else 'PlexAr'},sans-serif;color:#93A4BD;margin:18px 0 0}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:8px;background:linear-gradient({'90deg' if lang=='en' else '270deg'},#22D3EE,#F6B61D)}}
</style></head><body><div class="bg"></div><div class="v"></div><div class="g"></div>
<div class="c">{en if lang=='en' else ar}<div><h1>{tag}</h1><p>{sub}</p></div></div><div class="bar"></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        pg = b.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
        pg.set_content(f'<html><body style="margin:0;background:transparent">{mono.replace("<svg ", f"<svg width=\"{size}\" height=\"{size}\" ",1)}</body></html>')
        pg.screenshot(path=f"{B}/{name}", omit_background=True); pg.close()
    for lang in ["en", "ar"]:
        open(f"/tmp/og-{lang}.html", "w").write(og_html(lang))
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(f"file:///tmp/og-{lang}.html"); pg.wait_for_timeout(400)
        pg.screenshot(path=f"{B}/og-{lang}.jpg", type="jpeg", quality=86); pg.close()
    b.close()
print(sorted(os.listdir(B)))
