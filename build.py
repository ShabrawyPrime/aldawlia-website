#!/usr/bin/env python3
"""Aldawlia Group website generator.

    python3 build.py            -> docs/ (the website: external CSS/JS, self-hosted fonts; served by GitHub Pages)
                                   dist-artifact/ (single-folder preview: inline CSS/JS, Google Fonts; not committed)
Edit content in content/*.py, templates in templates/, styles in static/.
"""
import json, os, re, shutil, sys, glob
from jinja2 import Environment, FileSystemLoader, DebugUndefined
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from content.common import T, SITE, NAV, UI, COMPANIES, COMPANY, OFFICES, SOCIAL, KPIS, PAGES, ARABIC_COUNTRIES
from content.images import IMAGES
from content.home import HOME, SECTORS
from content.story import STORY
from content.group import GROUP, COUNTRIES, MARKETS, HUBS
from content.companies import COMPANY_PAGES, SERVICES
from content.projects import PROJECTS, PROJECT, REFERENCES, PROJECTS_PAGE, CATS
from content.solutions import SOLUTIONS, SUSTAIN, CONTACT
from content.brand import BRAND

BUILD = os.path.join(ROOT, "build")
FONTS = os.path.join(BUILD, "fonts")            # vendored woff2 files + unicode ranges (from @fontsource)
SRC = os.environ.get("AG_SRC_IMG", "/home/claude/work/src_img")   # original photos; only needed to regenerate the wall images
FORM_ENDPOINT = ""   # e.g. "https://formspree.io/f/xxxx" — when empty the form prepares an email instead

IMG = json.load(open(os.path.join(BUILD, "img", "images.json"), encoding="utf-8"))
LOGO = json.load(open(os.path.join(BUILD, "logos", "logos.json"), encoding="utf-8"))
IMGALT = {k: v[2] for k, v in IMAGES.items()}

EXTRA = {
    "MEGA_TEXT": T("Aldawlia and the companies built on its legacy, in cooling and in energy.", "الدولية والشركات التي قامت على إرثها، في التبريد وفي الطاقة."),
    "FOOT_TEXT": T("Industrial refrigeration since 1983, and a new generation of companies in solar energy and global supply.",
                   "تبريد صناعي منذ 1983، وجيل جديد من الشركات في الطاقة الشمسية والتوريد العالمي."),
    "TB": {"project": T("Project", "المشروع"), "date": T("Date", "التاريخ")},
    "POWERED": T("Powered by", "بقوة"),
    "EPCY": {"civil": T("Civil Department established", "تأسيس القسم المدني"), "epc": T("Turnkey EPC from empty land", "تسليم مفتاح من الأرض الفضاء")},
    "VMLAB": {"vision": T("Vision", "الرؤية"), "mission": T("Mission", "الرسالة")},
    "OFFICE2": {"label": T("Mansoura office", "مكتب المنصورة"), "address": OFFICES[1]["address"], "map": OFFICES[1]["map"]},
    "MARKETS_LABEL": T("Where we work", "أين نعمل"),
    "WALLALT": {
        "partners": T("Technology partner logos: Mayekawa MYCOM, ThermoKey, Baltimore Aircoil, Danfoss, SRMTec, Daikin, WITT, Lederle Hermetic, WIKA, thermofin, mind, GEA, Clauger, Johnson Controls and DECSA",
                      "شعارات شركاء التكنولوجيا: مايكاوا MYCOM وثيرموكي وبالتيمور إيركويل ودانفوس وSRMTec ودايكن وWITT وليدرلي هيرمتيك وWIKA وثيرموفين وmind وGEA وكلوجيه وجونسون كنترولز وDECSA"),
        "clients": T("Client logos including Nestlé, Mars, Americana, Gourmet, Domty, Juhayna, DHL, VACSERA, Orascom, Frozena, Halwani Bros, Ghataty Farms and Katilo",
                     "شعارات عملاء منهم نستله ومارس وأمريكانا وجورميه ودومتي وجهينة وDHL وفاكسيرا وأوراسكوم وفروزينا وحلواني إخوان ومزارع غطاطي وكاتيلو"),
    },
}
GROUP_PAGES = ["group", "aldawlia", "jet-solar", "ets", "nova-freeze", "neo-energy", "ggg"]

PAGE_DATA = {
    "index": HOME, "story": STORY, "group": GROUP, "solutions": SOLUTIONS, "projects": PROJECTS_PAGE,
    "sustainability": SUSTAIN, "contact": CONTACT, "brand": BRAND,
}
for k, v in COMPANY_PAGES.items():
    PAGE_DATA[k] = v

# ------------------------------------------------------------------ helpers
def tr(lang):
    def t(x):
        if isinstance(x, dict) and "en" in x and "ar" in x:
            return x[lang]
        if x is None:
            return ""
        return x
    return t

def url(lang, file):
    return f"{SITE['url']}/{lang}/" + ("" if file == "index.html" else file)

def read(p):
    return open(p, encoding="utf-8").read()

def svg_inline(path, uid):
    s = read(path)
    s = s.replace('id="g', f'id="{uid}g').replace('url(#g', f'url(#{uid}g')
    s = s.replace('id="mg"', f'id="{uid}mg"').replace('url(#mg)', f'url(#{uid}mg)')
    s = re.sub(r'<svg ', '<svg aria-hidden="true" focusable="false" ', s, count=1)
    return s

# ------------------------------------------------------------------ assets
def prep_assets(out, mode):
    A = os.path.join(out, "assets")
    for sub in ["img", "logos", "brand", "css", "js", "fonts"]:
        os.makedirs(os.path.join(A, sub), exist_ok=True)
    for f in glob.glob(os.path.join(BUILD, "img", "*.webp")):
        shutil.copy2(f, os.path.join(A, "img"))
    for f in glob.glob(os.path.join(BUILD, "logos", "*.*")):
        if not f.endswith(".json"):
            shutil.copy2(f, os.path.join(A, "logos"))
    for f in glob.glob(os.path.join(BUILD, "brand", "*.*")):
        shutil.copy2(f, os.path.join(A, "brand"))
    for f in glob.glob(os.path.join(BUILD, "walls", "*.webp")):
        shutil.copy2(f, os.path.join(A, "img"))
    css = read(os.path.join(ROOT, "static/css/site.css"))
    js = read(os.path.join(ROOT, "static/js/site.js"))
    if mode == "prod":
        css = fonts_css(A) + "\n" + css
        open(os.path.join(A, "css", "site.css"), "w", encoding="utf-8").write(css)
        open(os.path.join(A, "js", "site.js"), "w", encoding="utf-8").write(js)
    else:
        shutil.rmtree(os.path.join(A, "fonts"), ignore_errors=True)
        shutil.rmtree(os.path.join(A, "css"), ignore_errors=True)
        shutil.rmtree(os.path.join(A, "js"), ignore_errors=True)
    return css, js

FONT_SET = [
    ("space-grotesk", "Space Grotesk", "latin", [500, 600, 700]),
    ("ibm-plex-sans", "IBM Plex Sans", "latin", [400, 500, 600]),
    ("ibm-plex-mono", "IBM Plex Mono", "latin", [400, 500]),
    ("readex-pro", "Readex Pro", "arabic", [500, 600, 700]),
    ("ibm-plex-sans-arabic", "IBM Plex Sans Arabic", "arabic", [400, 500, 600, 700]),
]
GOOGLE_FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700"
                "&family=IBM+Plex+Sans:wght@400;500;600&family=Readex+Pro:wght@500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap")

_RANGES = json.load(open(os.path.join(FONTS, "ranges.json"), encoding="utf-8"))

def unicode_range(pkg, subset, w):
    return _RANGES.get(f"{pkg}-{subset}-{w}-normal.woff2", "U+0000-00FF")

def fonts_css(A):
    out = []
    for pkg, fam, subset, weights in FONT_SET:
        for w in weights:
            fn = f"{pkg}-{subset}-{w}-normal.woff2"
            shutil.copy2(os.path.join(FONTS, fn), os.path.join(A, "fonts", fn))
            ur = unicode_range(pkg, subset, w)
            out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(../fonts/{fn}) format('woff2');unicode-range:{ur}}}")
    return "\n".join(out)

def prep_walls():
    os.makedirs(os.path.join(BUILD, "walls"), exist_ok=True)
    walls = {"partners": "blob_1e788508e8a8fb269eba3a4142ba277a.jpg", "clients": "blob_afd16b2a1ed279125c054cbb22b4d8ec.jpg"}
    dims = {}
    for k, f in walls.items():
        out = os.path.join(BUILD, "walls", f"wall-{k}.webp")
        src = os.path.join(SRC, f)
        if os.path.exists(src):
            im = Image.open(src).convert("RGB")
            if im.width > 1800:
                im = im.resize((1800, round(im.height * 1800 / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=86, method=6)
        else:
            im = Image.open(out)          # source photos not on this machine: keep the processed wall
        dims[k] = {"w": im.width, "h": im.height}
    return dims

# ------------------------------------------------------------------ map
def map_svg(lang):
    meta = json.load(open(os.path.join(BUILD, "map-meta.json"), encoding="utf-8"))
    frag = read(os.path.join(BUILD, "map-paths.min.svgfrag"))
    t = tr(lang)
    W, H = meta["W"], meta["H"]
    hubs = []
    for h in HUBS:
        x, y = meta["hubs"][h["key"]]
        hubs.append(f'<g class="hub"><circle class="ring" cx="{x}" cy="{y}" r="5"/><circle class="core" cx="{x}" cy="{y}" r="3.2"/><title>{t(h["name"])} · {t(h["note"])}</title></g>')
    # Mauritius sits below the frame: draw a pointer at the bottom edge
    mu_x, mu_y = 905, H - 26
    mu = (f'<g><path d="M{mu_x} {mu_y-14} l0 -22" stroke="#2DC3DC" stroke-width="1" stroke-dasharray="2 3"/>'
          f'<circle class="mu-dot m-c is-on" data-cc="MU" cx="{mu_x}" cy="{mu_y}" r="6" tabindex="0" role="button" aria-label="{t(COUNTRIES["MU"])}"/>'
          f'<text x="{mu_x - 14 if lang == "en" else mu_x + 14}" y="{mu_y + 4}" text-anchor="end">{t(COUNTRIES["MU"])} ↓</text></g>')
    if lang == "ar":
        mu = mu.replace('text-anchor="end"', 'text-anchor="start"').replace(f'x="{mu_x + 14}"', f'x="{mu_x - 70}"')
    label = T("Map of the Middle East and Africa with the group's 17 active countries and its hubs", "خريطة الشرق الأوسط وإفريقيا تُظهر 17 دولة تعمل بها المجموعة ومراكزها")
    return (f'<svg viewBox="0 0 {W} {H}" role="group" aria-label="{t(label)}" preserveAspectRatio="xMidYMid meet">'
            f'{frag}{"".join(hubs)}{mu}</svg>')

def map_json(lang):
    t = tr(lang)
    by = {}
    for k, ccs in MARKETS.items():
        for cc in ccs:
            by.setdefault(cc, []).append(k)
    order = [c["key"] for c in COMPANIES]
    for cc in by:
        by[cc].sort(key=order.index)
    return json.dumps({
        "countries": {cc: t(n) for cc, n in COUNTRIES.items()},
        "companies": {c["key"]: {"name": t(c["short"]), "color": c["on_dark"]} for c in COMPANIES},
        "byCountry": by, "markets": MARKETS,
    }, ensure_ascii=False)

# ------------------------------------------------------------------ json-ld
def jsonld(lang, page):
    t = tr(lang)
    org = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": "Aldawlia Group", "alternateName": ["مجموعة الدولية", "Aldawlia for Cooling Corporation", "المؤسسة الدولية للتبريد"],
        "url": SITE["url"] + "/", "logo": SITE["url"] + "/assets/brand/icon-512.png",
        "foundingDate": "1986", "founder": {"@type": "Person", "name": "Nabil El Shabrawy"},
        "email": "info@aldawlia.org", "telephone": "+20 2 3836 7822",
        "address": {"@type": "PostalAddress", "streetAddress": "5 Solimar Buildings, Central Axis, Office 101", "addressLocality": "6th of October City", "addressRegion": "Giza", "addressCountry": "EG"},
        "sameAs": [s["url"] for s in SOCIAL],
        "subOrganization": [{"@type": "Organization", "name": c["short"]["en"] if c["key"] != "aldawlia" else c["name"]["en"], "url": c["url"]} for c in COMPANIES],
    }
    if page in COMPANY_PAGES:
        c = COMPANY[page]
        org = {"@context": "https://schema.org", "@type": "Organization", "name": c["name"]["en"], "alternateName": c["name"]["ar"],
               "url": c["url"], "email": c["email"], "telephone": c["phones"][0],
               "parentOrganization": {"@type": "Organization", "name": "Aldawlia Group", "url": SITE["url"] + "/"}}
    return json.dumps(org, ensure_ascii=False)

# ------------------------------------------------------------------ render
def render_site(out, mode, walls):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    css, js = prep_assets(out, mode)
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), undefined=DebugUndefined,
                      trim_blocks=False, lstrip_blocks=False, autoescape=False)
    lock = {
        "en_light": svg_inline(os.path.join(BUILD, "brand", "group-en-light.svg"), "a"),
        "en_dark": svg_inline(os.path.join(BUILD, "brand", "group-en-dark.svg"), "b"),
        "ar_light": svg_inline(os.path.join(BUILD, "brand", "group-ar-light.svg"), "c"),
        "ar_dark": svg_inline(os.path.join(BUILD, "brand", "group-ar-dark.svg"), "d"),
        "monogram": svg_inline(os.path.join(BUILD, "brand", "monogram.svg"), "e"),
    }
    project_cos = sorted({k for p in PROJECTS for k in p["cos"]})
    files = {p: ("index.html" if p == "index" else f"{p}.html") for p in PAGES}
    sheets = str(len(PAGES)).zfill(2)
    for lang in ["en", "ar"]:
        t = tr(lang)
        other = "ar" if lang == "en" else "en"
        os.makedirs(os.path.join(out, lang), exist_ok=True)
        if mode == "prod":
            head_assets = ('<link rel="preload" href="../assets/fonts/{f}" as="font" type="font/woff2" crossorigin>\n'
                           '<link rel="stylesheet" href="../assets/css/site.css">').format(
                f="space-grotesk-latin-700-normal.woff2" if lang == "en" else "readex-pro-arabic-700-normal.woff2")
            foot_assets = '<script src="../assets/js/site.js" defer></script>'
        else:
            head_assets = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
                           f'<link rel="stylesheet" href="{GOOGLE_FONTS}">\n<style>{css}</style>')
            foot_assets = f"<script>{js}</script>"
        market_names = {k: ("، " if lang == "ar" else ", ").join(t(COUNTRIES[cc]) for cc in v) for k, v in MARKETS.items()}
        route = {
            "needs": {k: co for k, _, co in CONTACT["needs"]},
            "companies": {c["key"]: {"name": t(c["short"]) if c["key"] != "aldawlia" else t(c["name"]), "email": c["email"],
                                     "logo": (f"../assets/logos/{c['logo']}.webp" if c["logo"] else "")} for c in COMPANIES},
            "labels": {"name": t(CONTACT["form"]["name"]), "company": t(CONTACT["form"]["company"]), "email": t(CONTACT["form"]["email"]),
                       "phone": t(CONTACT["form"]["phone"]), "country": t(CONTACT["form"]["country"]), "need": t(CONTACT["form"]["need"]),
                       "subject": t(CONTACT["form"]["subject"]), "sent": t(CONTACT["form"]["sent_title"])},
        }
        for i, page in enumerate(PAGES):
            tpl = "company.html" if page in COMPANY_PAGES else f"{page}.html"
            D = PAGE_DATA[page]
            ctx = dict(
                L=lang, DIR="rtl" if lang == "ar" else "ltr", OTHER=other, file=files[page], page=page, MODE=mode,
                SHEET=str(i + 1).zfill(2), SHEETS=sheets, A="../assets/", ROOT="../",
                t=t, URL=url, SITE=SITE, UI=UI, NAV=NAV, NAVD={n["key"]: n for n in NAV}, COMPANIES=COMPANIES, COMPANY=COMPANY,
                OFFICES=OFFICES, SOCIAL=SOCIAL, KPIS=KPIS, IMG=IMG, IMGALT=IMGALT, LOGO=LOGO, SECTORS=SECTORS, SERVICES=SERVICES,
                PROJECTS=PROJECTS, PROJECT=PROJECT, REFERENCES=REFERENCES, CATS=CATS, PROJECT_COS=project_cos,
                COUNTRIES=COUNTRIES, MARKETS=MARKETS, MARKET_NAMES=market_names, GROUP_PAGES=GROUP_PAGES,
                CTA=HOME["cta"], WALLS=walls, D=D, meta=D["meta"], CO=COMPANY.get(page),
                LOCKUP_LIGHT=lock[f"{lang}_light"], BRAND_SVGS=lock,
                HEAD_ASSETS=head_assets, FOOT_ASSETS=foot_assets, JSONLD=jsonld(lang, page),
                MAP_SVG=map_svg(lang) if page == "index" else "", MAP_JSON=map_json(lang) if page == "index" else "{}",
                ROUTE_JSON=json.dumps(route, ensure_ascii=False), FORM_ENDPOINT=FORM_ENDPOINT,
                **EXTRA,
            )
            html = env.get_template(tpl).render(**ctx)
            html = re.sub(r"\n\s*\n+", "\n", html)
            open(os.path.join(out, lang, files[page]), "w", encoding="utf-8").write(html)
    # gateway
    gate_fonts = "" if mode == "prod" else f'<link rel="stylesheet" href="{GOOGLE_FONTS}">'
    if mode == "prod":
        gate_fonts = ('<link rel="preload" href="assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
                      '<style>' + fonts_css_root() + '</style>')
    gctx = dict(ARTIFACT=(mode != "prod"), SITE=SITE, GATE_FONTS=gate_fonts,
                LOCKUP_EN=svg_inline(os.path.join(BUILD, "brand", "group-en-light.svg"), "x"),
                LOCKUP_AR=svg_inline(os.path.join(BUILD, "brand", "group-ar-light.svg"), "y"),
                ARAB_JSON=json.dumps(ARABIC_COUNTRIES), TZ_JSON=json.dumps(TZ_ARAB), AMBIG_JSON=json.dumps(TZ_AMBIG))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(env.get_template("gateway.html").render(**gctx))
    return files

def fonts_css_root():
    out = []
    for pkg, fam, subset, w in [("ibm-plex-sans", "IBM Plex Sans", "latin", 400), ("ibm-plex-sans", "IBM Plex Sans", "latin", 600), ("ibm-plex-sans-arabic", "IBM Plex Sans Arabic", "arabic", 400), ("ibm-plex-sans-arabic", "IBM Plex Sans Arabic", "arabic", 600)]:
        fn = f"{pkg}-{subset}-{w}-normal.woff2"
        ur = unicode_range(pkg, subset, w)
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(assets/fonts/{fn}) format('woff2');unicode-range:{ur}}}")
    return "".join(out)

# Time zones that belong to Arabic-speaking countries (IANA id -> ISO country)
TZ_ARAB = {
    "Africa/Cairo": "EG", "Egypt": "EG", "Asia/Riyadh": "SA", "Asia/Dubai": "AE", "Asia/Muscat": "OM", "Asia/Kuwait": "KW",
    "Asia/Qatar": "QA", "Asia/Bahrain": "BH", "Asia/Aden": "YE", "Asia/Baghdad": "IQ", "Asia/Damascus": "SY", "Asia/Amman": "JO",
    "Asia/Beirut": "LB", "Asia/Gaza": "PS", "Asia/Hebron": "PS", "Africa/Tripoli": "LY", "Libya": "LY", "Africa/Tunis": "TN",
    "Africa/Algiers": "DZ", "Africa/Casablanca": "MA", "Africa/El_Aaiun": "EH", "Africa/Khartoum": "SD", "Africa/Nouakchott": "MR",
    "Africa/Djibouti": "DJ", "Africa/Mogadishu": "SO", "Indian/Comoro": "KM", "Africa/Ndjamena": "TD",
}
# Zones shared with non-Arab countries (or reported by privacy modes): decided by the browser's locale region/language instead
TZ_AMBIG = ["Africa/Lagos", "Africa/Nairobi", "Africa/Abidjan", "Atlantic/Reykjavik", "Asia/Jerusalem", "Asia/Tel_Aviv",
            "UTC", "Etc/UTC", "Etc/GMT", "GMT", "Etc/Universal", "Universal", "Zulu", "Etc/Zulu"]

# ------------------------------------------------------------------ extras (prod)
def write_extras(out, files):
    S = SITE["url"]
    urls = []
    for p, f in files.items():
        for lang in ["en", "ar"]:
            loc = url(lang, f)
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, f)}"/>' for l in ["en", "ar"])
            urls.append(f"<url><loc>{loc}</loc>{alts}<xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{S}/\"/><lastmod>2026-10-11</lastmod></url>")
    open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(out, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {S}/sitemap.xml\n")
    open(os.path.join(out, "site.webmanifest"), "w", encoding="utf-8").write(json.dumps({
        "name": "Aldawlia Group", "short_name": "Aldawlia", "start_url": "/", "display": "standalone",
        "background_color": "#070B14", "theme_color": "#070B14",
        "icons": [{"src": "/assets/brand/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/brand/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    countries = ",".join(c.lower() for c in ARABIC_COUNTRIES)
    open(os.path.join(out, "_redirects"), "w", encoding="utf-8").write(
        "# Netlify: send the root to the right language by country. A saved choice (cookie ag_lang) is handled by the\n"
        "# edge function in netlify/edge-functions/lang.js; these rules are the fallback when edge functions are off.\n"
        f"/  /ar/  302  Country={countries}\n/  /en/  302\n")
    open(os.path.join(out, "404.html"), "w", encoding="utf-8").write(NOT_FOUND)
    open(os.path.join(out, ".nojekyll"), "w", encoding="utf-8").write("")
    shutil.copytree(os.path.join(ROOT, "deploy"), os.path.join(out, "deploy"), dirs_exist_ok=True)
    shutil.copy2(os.path.join(ROOT, "README.md"), os.path.join(out, "README.md"))

NOT_FOUND = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Aldawlia Group</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml" data-p="assets/brand/favicon.svg">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#070B14;color:#EEF3FA;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;text-align:center;padding:24px}
h1{font-size:clamp(2rem,6vw,3.4rem);margin:0 0 8px}p{color:#93A4BD;margin:0 0 24px}a{display:inline-block;margin:6px;padding:12px 20px;border:1px solid rgba(255,255,255,.25);border-radius:4px;color:#EEF3FA;text-decoration:none}a:hover{border-color:#22D3EE;color:#22D3EE}
.ar{direction:rtl;font-family:"IBM Plex Sans Arabic",Tahoma,sans-serif}</style></head>
<body><main><h1>404</h1><p>This page could not be found.</p><p class="ar">تعذّر العثور على هذه الصفحة.</p>
<a href="/en/" data-p="en/">Aldawlia Group</a><a class="ar" href="/ar/" data-p="ar/">مجموعة الدولية</a></main>
<script>(function(){var b="/";if(/\\.github\\.io$/.test(location.hostname)){var s=location.pathname.split("/")[1];if(s)b="/"+s+"/";}document.querySelectorAll("[data-p]").forEach(function(e){e.setAttribute("href",b+e.getAttribute("data-p"));});})();</script></body></html>
"""

def artifactize(out):
    """Root page of the artifact is wrapped by the host: it must not carry doctype/html/head/body."""
    p = os.path.join(out, "index.html")
    s = read(p)
    assert "<!doctype" not in s.lower(), "artifact gateway must be content-only"

if __name__ == "__main__":
    OUT = os.path.join(ROOT, os.environ.get("AG_OUT", "docs"))
    walls = prep_walls()
    files = render_site(OUT, "prod", walls)
    write_extras(OUT, files)
    render_site(os.path.join(ROOT, "dist-artifact"), "artifact", walls)
    artifactize(os.path.join(ROOT, "dist-artifact"))
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    m = sum(len(fs) for _, _, fs in os.walk(os.path.join(ROOT, "dist-artifact")))
    print(f"built {os.path.basename(OUT)}: {n} files · dist-artifact: {m} files")
