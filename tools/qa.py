import sys, json
from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765"
PAGES = "index,story,group,aldawlia,jet-solar,ets,nova-freeze,neo-energy,ggg,solutions,projects,sustainability,contact,brand".split(",")
pages = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] != "all" else PAGES
langs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["en", "ar"]
vps = sys.argv[3].split(",") if len(sys.argv) > 3 else ["m", "d"]
VP = {"d": (1440, 900), "m": (390, 844), "s": (360, 740), "t": (820, 1180), "l": (1180, 820)}
JS = """async () => {
  const H = document.documentElement.scrollHeight;
  for (let y = 0; y < H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
  window.scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
  const vw = document.documentElement.clientWidth, out = [];
  const clipped = el => { for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) { const cs = getComputedStyle(a); if (/(hidden|clip|auto|scroll)/.test(cs.overflowX + cs.overflow)) { const r = a.getBoundingClientRect(); if (r.left >= -1 && r.right <= vw + 1) return true; } } return false; };
  for (const el of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden' || cs.position === 'fixed') continue;
    const r = el.getBoundingClientRect(); if (!r.width) continue;
    if ((r.right > vw + 1 || r.left < -1) && !clipped(el)) out.push((el.tagName + '.' + (el.className && el.className.baseVal === undefined ? el.className : '')).slice(0, 60) + ' [' + Math.round(r.left) + ',' + Math.round(r.right) + ']');
  }
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src'));
  // text overflow inside boxes (single-line nowrap clipped)
  const tight = [];
  for (const el of document.body.querySelectorAll('h1,h2,h3,h4,p,a,span,strong,dd,dt,li,button,label,small,b')) {
    if (el.children.length || el.closest('.vh')) continue; const cs = getComputedStyle(el); if (cs.display === 'none') continue;
    if (el.scrollWidth > el.clientWidth + 2 && cs.overflow !== 'visible' && el.clientWidth > 0) tight.push(el.tagName + ':' + el.textContent.trim().slice(0, 40));
  }
  return { sw: document.documentElement.scrollWidth, vw, h: document.documentElement.scrollHeight, out: out.slice(0, 12), n: out.length, broken, tight: tight.slice(0, 8) };
}"""
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in langs:
        for v in vps:
            w, h = VP[v]
            ctx = b.new_context(viewport={"width": w, "height": h}, reduced_motion="reduce")
            for pg_ in pages:
                pg = ctx.new_page(); errs = []; fails = []
                pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append(str(e)))
                pg.on("response", lambda r: fails.append(r.url) if r.status >= 400 else None)
                pg.goto(f"{BASE}/{lang}/{pg_}.html", wait_until="networkidle")
                r = pg.evaluate(JS)
                flag = r["sw"] > r["vw"] or r["n"] or r["broken"] or errs or fails or r["tight"]
                bad += bool(flag)
                print(f"{'!!' if flag else 'ok'} {lang}/{pg_}/{v} h={r['h']} sw={r['sw']}/{r['vw']}" + (f" over={r['n']} {r['out']}" if r['n'] else "") + (f" broken={r['broken']}" if r['broken'] else "") + (f" errs={errs[:3]}" if errs else "") + (f" 4xx={fails[:3]}" if fails else "") + (f" tight={r['tight']}" if r['tight'] else ""))
                pg.close()
            ctx.close()
    b.close()
print("flagged", bad)
