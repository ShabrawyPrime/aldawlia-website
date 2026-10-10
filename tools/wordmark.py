import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from textpath import Face, shape, fmt
import uharfbuzz as hb
FS="/home/claude/tools/node_modules/@fontsource"
SG=Face(f"{FS}/space-grotesk/files/space-grotesk-latin-700-normal.woff2")
MONO=Face(f"{FS}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2")
RDX=Face(f"{FS}/readex-pro/files/readex-pro-arabic-700-normal.woff2")
RDX6=Face(f"{FS}/readex-pro/files/readex-pro-arabic-500-normal.woff2")
OUT=sys.argv[1]; os.makedirs(OUT,exist_ok=True)

GRAD='<linearGradient id="{id}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#F6B61D"/></linearGradient>'
VGRAD='<linearGradient id="{id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#F6B61D"/></linearGradient>'
GRAD_RTL=VGRAD

def lockup_en(color="#EEF3FA", sub="#93A4BD", gid="agS"):
    # ALDAWLIA (cap height ~ 40) + bar + GROUP mono
    size=56
    d1,w1=shape(SG,"ALDAWLIA",size,tracking=0.02)
    cap=SG.cap*size/SG.upem
    sub_size=17
    d2,w2=shape(MONO,"GROUP",sub_size,tracking=0.28)
    gap=16; barw=4
    x2=w1+gap+barw+gap
    H=cap
    # vertical bar spans cap height; GROUP baseline aligned to bottom
    capm=MONO.cap*sub_size/MONO.upem
    W=x2+w2
    pad=2
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-cap-pad:.2f} {W+2*pad:.2f} {cap+2*pad:.2f}" role="img" aria-label="Aldawlia Group">'
         f'<defs>{VGRAD.format(id=gid)}</defs>'
         f'<path fill="{color}" d="{fmt(d1)}"/>'
         f'<rect x="{w1+gap:.2f}" y="{-cap:.2f}" width="{barw}" height="{cap:.2f}" fill="url(#{gid})"/>'
         f'<g transform="translate({x2:.2f},0)"><path fill="{sub}" d="{fmt(d2)}"/></g>'
         f'</svg>')
    return svg, (W+2*pad, cap+2*pad)

def lockup_ar(color="#EEF3FA", sub="#93A4BD", gid="agSa"):
    size=52
    d1,w1=shape(RDX,"الدولية",size)
    d2,w2=shape(RDX6,"مجموعة",size*0.5)
    # Arabic metrics: use ascender/descender of shaped text bbox approx
    asc=RDX.asc*size/RDX.upem*0.78; desc=-RDX.desc*size/RDX.upem*0.55
    gap=14; barw=4
    # RTL: [مجموعة] (right) | bar | [الدولية] (left)
    # place big name at x=0..w1, bar, then small at right
    xbar=w1+gap; xs=xbar+barw+gap
    W=xs+w2
    top=-asc; h=asc+desc
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 {top-2:.2f} {W+4:.2f} {h+4:.2f}" role="img" aria-label="مجموعة الدولية">'
         f'<defs>{GRAD_RTL.format(id=gid)}</defs>'
         f'<path fill="{color}" d="{fmt(d1)}"/>'
         f'<rect x="{xbar:.2f}" y="{-asc*0.92:.2f}" width="{barw}" height="{asc*0.92+desc*0.35:.2f}" fill="url(#{gid})"/>'
         f'<g transform="translate({xs:.2f},0)"><path fill="{sub}" d="{fmt(d2)}"/></g>'
         f'</svg>')
    return svg,(W+4,h+4)

def monogram():
    size=150
    dA,wA=shape(SG,"A",size)
    cap=SG.cap*size/SG.upem
    S=256
    x=(S-wA)/2; base=S/2+cap/2-14
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}">'
         f'<defs>{GRAD.format(id="mg")}</defs>'
         f'<rect width="{S}" height="{S}" rx="56" fill="#070B14"/>'
         f'<g transform="translate({x:.2f},{base:.2f})"><path fill="#EEF3FA" d="{fmt(dA)}"/></g>'
         f'<rect x="{x:.2f}" y="{base+18:.2f}" width="{wA:.2f}" height="12" rx="0" fill="url(#mg)"/>'
         f'</svg>')
    return svg

for name,(svg,dim) in {"group-en-light":lockup_en("#EEF3FA","#93A4BD","g1"),
                       "group-en-dark":lockup_en("#0B1B2E","#3B4D66","g2"),
                       "group-ar-light":lockup_ar("#EEF3FA","#93A4BD","g3"),
                       "group-ar-dark":lockup_ar("#0B1B2E","#3B4D66","g4")}.items():
    open(f"{OUT}/{name}.svg","w").write(svg); print(name, [round(v,1) for v in dim], len(svg))
open(f"{OUT}/monogram.svg","w").write(monogram())
