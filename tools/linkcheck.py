import os, re, sys, glob
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
root = sys.argv[1] if len(sys.argv) > 1 else "dist"
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs = []; s.ids = set()
    def handle_starttag(s, t, a):
        d = dict(a)
        if "id" in d: s.ids.add(d["id"])
        for k in ("href", "src", "poster", "data-src"):
            if d.get(k): s.refs.append((t, k, d[k]))
        for k in ("srcset", "imagesrcset"):
            if d.get(k):
                for part in d[k].split(","):
                    u = part.strip().split(" ")[0]
                    if u: s.refs.append((t, k, u))
    handle_startendtag = handle_starttag
pages = {}
for f in glob.glob(f"{root}/**/*.html", recursive=True):
    p = P(); p.feed(open(f, encoding="utf-8").read()); pages[os.path.normpath(f)] = p
bad = []; ext = set(); n = 0
for f, p in pages.items():
    for t, k, u in p.refs:
        if u.startswith(("mailto:", "tel:", "data:", "javascript:")): continue
        if u.startswith(("http://", "https://", "//")): ext.add(u); continue
        n += 1
        pr = urlparse(u); path = unquote(pr.path)
        if not path:
            if pr.fragment and pr.fragment not in p.ids and t == "a": bad.append((f, u, "missing #id"))
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(f), path))
        if path.endswith("/"): target = os.path.join(target, "index.html")
        if not os.path.exists(target): bad.append((f, u, "missing file")); continue
        if pr.fragment and target.endswith(".html") and t == "a":
            tp = pages.get(os.path.normpath(target))
            if tp and pr.fragment not in tp.ids and pr.fragment not in ("ar", "en"): bad.append((f, u, "missing #id in target"))
print(f"{len(pages)} pages · {n} internal refs · {len(bad)} broken · {len(ext)} external")
for b in bad[:40]: print("  ", b)
if "-x" in sys.argv:
    for e in sorted(ext): print("  ext", e)
