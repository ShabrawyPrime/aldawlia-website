import re,sys,json
src=open('/home/claude/site/build/map-paths.svgfrag').read()
def compact(d):
    out=[]; 
    for sub in re.findall(r'M[^M]+',d):
        closed=sub.rstrip().endswith('Z')
        pts=[tuple(map(int,p.split(','))) for p in re.findall(r'-?\d+,-?\d+',sub)]
        # dedupe consecutive
        dd=[pts[0]]
        for p in pts[1:]:
            if p!=dd[-1]: dd.append(p)
        # drop collinear points
        res=[dd[0]]
        for i in range(1,len(dd)-1):
            a,b,c=res[-1],dd[i],dd[i+1]
            if (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])==0: continue
            res.append(b)
        if len(dd)>1: res.append(dd[-1])
        if len(res)<3 and closed: continue
        s=f"M{res[0][0]} {res[0][1]}"
        prev=res[0]; parts=[]
        for p in res[1:]:
            dx,dy=p[0]-prev[0],p[1]-prev[1]; prev=p
            parts.append(f"{dx} {dy}")
        s+="l"+" ".join(parts).replace(" -","-")
        s=s.replace(" -","-")
        if closed: s+="z"
        out.append(s)
    return "".join(out)
paths=re.findall(r'<path([^>]*) d="([^"]+)"/>',src)
res=[]
for attrs,d in paths:
    c=compact(d)
    if c: res.append(f'<path{attrs} d="{c}"/>')
open('/home/claude/site/build/map-paths.min.svgfrag','w').write("".join(res))
print(len(src),'->',len("".join(res)), len(res))
