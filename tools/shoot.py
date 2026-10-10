import sys, os
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765"
OUT = "/home/claude/work/shots"
pages = sys.argv[1].split(",")
langs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["en"]
vps = sys.argv[3].split(",") if len(sys.argv) > 3 else ["d"]
VP = {"d": (1440, 900), "m": (390, 844), "t": (900, 1100)}
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in langs:
        for pg_ in pages:
            for v in vps:
                w, h = VP[v]
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, reduced_motion="reduce")
                pg = ctx.new_page()
                errs = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                url = f"{BASE}/{lang}/{pg_}.html" if pg_ != "gate" else f"{BASE}/index.html#{lang}"
                pg.goto(url, wait_until="networkidle")
                pg.wait_for_timeout(500)
                pg.evaluate("""async () => { const H = document.documentElement.scrollHeight; for (let y = 0; y < H; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); }""")
                pg.wait_for_timeout(700)
                sw = pg.evaluate("document.documentElement.scrollWidth"); 
                path = f"{OUT}/{lang}-{pg_}-{v}.png"
                pg.screenshot(path=path, full_page=True)
                hgt = pg.evaluate("document.documentElement.scrollHeight")
                print(f"{lang}/{pg_}/{v}: h={hgt} scrollW={sw} (vw={w}) errors={errs[:3]}")
                ctx.close()
    b.close()
