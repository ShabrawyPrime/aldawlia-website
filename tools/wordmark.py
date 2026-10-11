"""Signature lockups for Aldawlia for Cooling Corporation (outlined SVG, no font dependency).

EN: ALDAWLIA | FOR COOLING / CORPORATION   (Space Grotesk Bold, Spectrum bar, IBM Plex Mono descriptor)
AR: المؤسسة الدولية | للتبريد               (Readex Pro: small المؤسسة, big الدولية, bar, small للتبريد; read right to left)

    python3 tools/wordmark.py build/brand
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from textpath import Face, shape, fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "build", "fonts")
SG = Face(f"{F}/space-grotesk-latin-700-normal.woff2")
MONO = Face(f"{F}/ibm-plex-mono-latin-500-normal.woff2")
RDX = Face(f"{F}/readex-pro-arabic-700-normal.woff2")
RDX5 = Face(f"{F}/readex-pro-arabic-500-normal.woff2")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "build", "brand")
os.makedirs(OUT, exist_ok=True)

GRAD = '<linearGradient id="{id}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#F6B61D"/></linearGradient>'
VGRAD = '<linearGradient id="{id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#F6B61D"/></linearGradient>'


def lockup_en(color="#EEF3FA", sub="#93A4BD", gid="agS"):
    size = 56
    d1, w1 = shape(SG, "ALDAWLIA", size, tracking=0.02)
    cap = SG.cap * size / SG.upem
    ss = 15.5                                   # descriptor size: two lines span the cap height
    capm = MONO.cap * ss / MONO.upem
    da, wa = shape(MONO, "FOR COOLING", ss, tracking=0.16)
    db, wb = shape(MONO, "CORPORATION", ss, tracking=0.16)
    gap, barw = 16, 4
    x2 = w1 + gap + barw + gap
    W = x2 + max(wa, wb)
    pad = 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-cap - pad:.2f} {W + 2 * pad:.2f} {cap + 2 * pad:.2f}" role="img" aria-label="Aldawlia for Cooling Corporation">'
           f'<defs>{VGRAD.format(id=gid)}</defs>'
           f'<path fill="{color}" d="{fmt(d1)}"/>'
           f'<rect x="{w1 + gap:.2f}" y="{-cap:.2f}" width="{barw}" height="{cap:.2f}" fill="url(#{gid})"/>'
           f'<g transform="translate({x2:.2f},{-cap + capm:.2f})"><path fill="{sub}" d="{fmt(da)}"/></g>'
           f'<g transform="translate({x2:.2f},0)"><path fill="{sub}" d="{fmt(db)}"/></g>'
           f'</svg>')
    return svg, (W + 2 * pad, cap + 2 * pad)


def lockup_ar(color="#EEF3FA", sub="#93A4BD", gid="agSa"):
    size = 52
    small = size * 0.5
    d_big, w_big = shape(RDX, "الدولية", size)
    d_pre, w_pre = shape(RDX5, "المؤسسة", small)
    d_post, w_post = shape(RDX5, "للتبريد", small)
    asc = RDX.asc * size / RDX.upem * 0.78
    desc = -RDX.desc * size / RDX.upem * 0.55
    gap, barw, gap_pre = 14, 4, 10
    # left to right on the page: [للتبريد] gap bar gap [الدولية] gap_pre [المؤسسة]  -> reads المؤسسة الدولية | للتبريد
    x_bar = w_post + gap
    x_big = x_bar + barw + gap
    x_pre = x_big + w_big + gap_pre
    W = x_pre + w_pre
    top, h = -asc, asc + desc
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 {top - 2:.2f} {W + 4:.2f} {h + 4:.2f}" role="img" aria-label="المؤسسة الدولية للتبريد">'
           f'<defs>{VGRAD.format(id=gid)}</defs>'
           f'<path fill="{sub}" d="{fmt(d_post)}"/>'
           f'<rect x="{x_bar:.2f}" y="{-asc * 0.92:.2f}" width="{barw}" height="{asc * 0.92 + desc * 0.35:.2f}" fill="url(#{gid})"/>'
           f'<g transform="translate({x_big:.2f},0)"><path fill="{color}" d="{fmt(d_big)}"/></g>'
           f'<g transform="translate({x_pre:.2f},0)"><path fill="{sub}" d="{fmt(d_pre)}"/></g>'
           f'</svg>')
    return svg, (W + 4, h + 4)


def wordmark_en(color="#EEF3FA"):
    """ALDAWLIA alone: the compact signature for narrow headers."""
    size = 56
    d1, w1 = shape(SG, "ALDAWLIA", size, tracking=0.02)
    cap = SG.cap * size / SG.upem
    pad = 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-cap - pad:.2f} {w1 + 2 * pad:.2f} {cap + 2 * pad:.2f}" role="img" aria-label="Aldawlia">'
           f'<path fill="{color}" d="{fmt(d1)}"/></svg>')
    return svg, (w1 + 2 * pad, cap + 2 * pad)


def monogram():
    size = 150
    dA, wA = shape(SG, "A", size)
    cap = SG.cap * size / SG.upem
    S = 256
    x = (S - wA) / 2
    base = S / 2 + cap / 2 - 14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">'
            f'<defs>{GRAD.format(id="mg")}</defs>'
            f'<rect width="{S}" height="{S}" rx="56" fill="#070B14"/>'
            f'<g transform="translate({x:.2f},{base:.2f})"><path fill="#EEF3FA" d="{fmt(dA)}"/></g>'
            f'<rect x="{x:.2f}" y="{base + 18:.2f}" width="{wA:.2f}" height="12" rx="0" fill="url(#mg)"/>'
            f'</svg>')


if __name__ == "__main__":
    for name, (svg, dim) in {"aldawlia-en-light": lockup_en("#EEF3FA", "#93A4BD", "g1"),
                             "aldawlia-en-dark": lockup_en("#0B1B2E", "#3B4D66", "g2"),
                             "aldawlia-ar-light": lockup_ar("#EEF3FA", "#93A4BD", "g3"),
                             "aldawlia-ar-dark": lockup_ar("#0B1B2E", "#3B4D66", "g4"),
                             "aldawlia-en-compact-light": wordmark_en("#EEF3FA")}.items():
        open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(svg)
        print(name, [round(v, 1) for v in dim], len(svg))
    open(f"{OUT}/monogram.svg", "w", encoding="utf-8").write(monogram())
