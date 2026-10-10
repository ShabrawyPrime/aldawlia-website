"""Prepare company logos: trim transparent margins, export colour + reversed (white) PNGs at 2x display height."""
import sys, os, json
from PIL import Image, ImageOps
SRC="/home/claude/work/src_img"
OUT=sys.argv[1]
os.makedirs(OUT,exist_ok=True)
LOGOS={
 "aldawlia":"aldawlia_logo.png",
 "jet-solar":"blob_ae2726c16e830e1e541301369c417cb6.png",
 "ets":"blob_6cd2cc7980939d1df9379f23fab523a5.png",
 "nova-freeze":"nova_logo.png",
 "neo-energy":"blob_1612f676708b9d6f9b889a8622ef014d.png",
 "ggg":"blob_96eb6d3f866cd6652db158ac886c33b1.png",
 "elaraby":"blob_f0df9df813ac6fe6cabcf5de229db80b.png",
}
meta={}
for key,f in LOGOS.items():
    im=Image.open(os.path.join(SRC,f)).convert("RGBA")
    # alpha-trim
    bbox=im.getchannel("A").point(lambda a:255 if a>8 else 0).getbbox()
    im=im.crop(bbox)
    # pad 2%
    pad=max(2,int(min(im.size)*0.02))
    canvas=Image.new("RGBA",(im.width+2*pad,im.height+2*pad),(0,0,0,0)); canvas.paste(im,(pad,pad)); im=canvas
    # colour version: max height 240px (2x of 120)
    H=240 if key!="aldawlia" else 360
    if im.height>H:
        im=im.resize((round(im.width*H/im.height),H),Image.LANCZOS)
    im.save(os.path.join(OUT,f"{key}.png"),optimize=True)
    # reversed: white with original alpha (keeps shape), for dark backgrounds
    a=im.getchannel("A")
    white=Image.new("RGBA",im.size,(255,255,255,0)); white.putalpha(a)
    w=Image.merge("RGBA",(Image.new("L",im.size,255),)*3+(a,))
    w.save(os.path.join(OUT,f"{key}-white.png"),optimize=True)
    # webp too
    im.save(os.path.join(OUT,f"{key}.webp"),quality=92,method=6)
    w.save(os.path.join(OUT,f"{key}-white.webp"),quality=92,method=6)
    meta[key]={"w":im.width,"h":im.height}
json.dump(meta,open(os.path.join(OUT,"logos.json"),"w"),indent=1)
print(meta)
