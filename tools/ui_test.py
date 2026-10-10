from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765"
res = []
def check(name, cond, extra=""):
    res.append(cond); print(("PASS" if cond else "FAIL"), name, extra)
with sync_playwright() as p:
    b = p.chromium.launch()
    # mobile drawer
    for lang in ["en", "ar"]:
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f"{BASE}/{lang}/index.html", wait_until="networkidle")
        pg.click("[data-burger]"); pg.wait_for_timeout(400)
        vis = pg.is_visible("#drawer"); exp = pg.get_attribute("[data-burger]", "aria-expanded")
        check(f"{lang} drawer opens", vis and exp == "true")
        links = pg.locator("#drawer a").count(); check(f"{lang} drawer links", links >= 12, str(links))
        pg.keyboard.press("Escape"); pg.wait_for_timeout(400)
        check(f"{lang} drawer closes on Esc", not pg.is_visible("#drawer"))
        check(f"{lang} no page errors", not errs, str(errs[:2]))
        ctx.close()
    # desktop mega + lang switch
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    pg.goto(f"{BASE}/en/story.html", wait_until="networkidle")
    pg.click(".mega-tg"); pg.wait_for_timeout(300)
    check("mega opens", pg.is_visible("#mega"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    check("mega closes on Esc", not pg.is_visible("#mega"))
    pg.click("header [data-setlang='ar']"); pg.wait_for_load_state("networkidle")
    check("lang switch keeps page", pg.url.endswith("/ar/story.html"), pg.url)
    check("lang saved", pg.evaluate("localStorage.getItem('ag:lang')") == "ar")
    pg.goto(f"{BASE}/index.html"); pg.wait_for_url("**/ar/index.html", timeout=3000)
    check("gateway honours saved ar", pg.url.endswith("/ar/index.html"))
    # projects filter
    pg.goto(f"{BASE}/en/projects.html", wait_until="networkidle")
    total = pg.locator(".pcard:visible").count()
    pg.click("[data-f='solar']")
    pg.wait_for_timeout(300)
    solar = pg.locator(".pcard:visible").count()
    check("projects filter", 0 < solar < total, f"{solar}/{total} hash={pg.evaluate('location.hash')}")
    # contact form
    pg.goto(f"{BASE}/en/contact.html", wait_until="networkidle")
    pg.click("form[data-form] button[type=submit]"); pg.wait_for_timeout(200)
    inval = pg.locator("form[data-form] [aria-invalid='true']").count()
    check("form blocks empty submit", inval >= 3 and not pg.is_visible("[data-ready]"), str(inval))
    pg.fill("#f-name", "Test Person"); pg.fill("#f-email", "test@example.com"); pg.fill("#f-company", "ACME Foods")
    opts = pg.eval_on_selector_all("#f-need option", "os => os.map(o => o.value).filter(Boolean)")
    pg.select_option("#f-need", opts[0]); pg.wait_for_timeout(200)
    route_vis = pg.is_visible("[data-route]"); mail = pg.inner_text("[data-route-mail]")
    check("routing shows company", route_vis and "@" in mail, mail)
    pg.fill("#f-msg", "Cold store for 5,000 t potatoes in Minya."); pg.check("#f-ok")
    pg.click("form[data-form] button[type=submit]"); pg.wait_for_timeout(300)
    ready = pg.is_visible("[data-ready]"); href = pg.get_attribute("[data-mailto]", "href") or ""
    check("ready panel + mailto", ready and href.startswith("mailto:") and mail.split("@")[1] in href, href[:120])
    # each need routes somewhere valid
    pg.click("[data-edit]") if pg.locator("[data-edit]").count() else None
    routes = {}
    for o in opts:
        pg.select_option("#f-need", o); pg.wait_for_timeout(60); routes[o] = pg.inner_text("[data-route-mail]")
    check("all needs route", all("@" in v for v in routes.values()), str(routes))
    ctx.close()
    b.close()
print(sum(res), "/", len(res))
