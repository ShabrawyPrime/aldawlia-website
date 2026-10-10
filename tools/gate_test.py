from playwright.sync_api import sync_playwright
BASE = "http://127.0.0.1:8765"
cases = [
  ("Africa/Cairo", "en-US", None, "", "ar"),
  ("Europe/London", "en-GB", None, "", "en"),
  ("Asia/Dubai", "en-US", None, "", "ar"),
  ("Asia/Riyadh", "ar-SA", None, "", "ar"),
  ("America/New_York", "ar-EG", None, "", "en"),
  ("Africa/Casablanca", "fr-FR", None, "", "ar"),
  ("Asia/Kolkata", "en-IN", None, "", "en"),
  ("UTC", "ar-EG", None, "", "ar"),
  ("UTC", "en-US", None, "", "en"),
  ("Africa/Cairo", "en-US", "en", "", "en"),
  ("Europe/London", "en-GB", None, "#ar", "ar"),
  ("Africa/Cairo", "ar-EG", None, "?lang=en", "en"),
]
ok = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for tz, loc, saved, suffix, want in cases:
        ctx = b.new_context(timezone_id=tz, locale=loc)
        pg = ctx.new_page()
        if saved:
            pg.goto(f"{BASE}/robots.txt"); pg.evaluate(f"localStorage.setItem('ag:lang','{saved}')")
        pg.goto(f"{BASE}/index.html{suffix}")
        st = pg.locator("#st").inner_text()
        try:
            pg.wait_for_url(f"**/{want}/index.html", timeout=4000); got = want
        except Exception:
            got = pg.url
        res = got == want; ok += res
        print(("PASS" if res else "FAIL"), tz, loc, saved, suffix or "-", "->", got, "|", st)
        ctx.close()
    b.close()
print(ok, "/", len(cases))
