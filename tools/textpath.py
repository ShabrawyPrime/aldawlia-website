"""Shape text with HarfBuzz and emit SVG path data (font-independent wordmarks)."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import io

class Face:
    def __init__(self, path):
        self.path=path
        self.tt=TTFont(path)
        buf=io.BytesIO(); self.tt.flavor=None; self.tt.save(buf); data=buf.getvalue()
        self.tt=TTFont(io.BytesIO(data))
        self.hbface=hb.Face(data); self.font=hb.Font(self.hbface)
        self.upem=self.tt["head"].unitsPerEm
        self.gs=self.tt.getGlyphSet()
        self.order=self.tt.getGlyphOrder()
        os2=self.tt["OS/2"]; self.cap=getattr(os2,"sCapHeight",0) or int(self.upem*0.7)
        self.asc=self.tt["hhea"].ascent; self.desc=self.tt["hhea"].descent

def shape(face, text, size, tracking=0.0, direction=None, features=None):
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    if direction: buf.direction=direction
    hb.shape(face.font, buf, features or {"kern":True,"liga":True})
    scale=size/face.upem
    x=0.0; parts=[]
    infos=buf.glyph_infos; poss=buf.glyph_positions
    n=len(infos)
    for i,(info,pos) in enumerate(zip(infos,poss)):
        gname=face.order[info.codepoint]
        pen=SVGPathPen(face.gs)
        tp=TransformPen(pen,(scale,0,0,-scale,x+pos.x_offset*scale,-pos.y_offset*scale))
        face.gs[gname].draw(tp)
        d=pen.getCommands()
        if d: parts.append(d)
        x+=pos.x_advance*scale
        if i<n-1: x+=tracking*size
    return " ".join(parts), x

def fmt(d, nd=2):
    import re
    return re.sub(r"-?\d+\.\d+", lambda m: f"{float(m.group()):.{nd}f}".rstrip("0").rstrip("."), d)
