"""Flag crossings between explicit orthogonal Draw.io waypoint segments.

A conservative preflight: endpoint connectors and Draw.io auto-routing are omitted.
"""
import argparse
import itertools
import xml.etree.ElementTree as ET

def props(cell):
    return dict(x.split("=", 1) for x in cell.get("style", "").split(";") if "=" in x)

def rect(cell):
    g = cell.find("mxGeometry")
    if g is None: return None
    try: return tuple(float(g.get(k)) for k in ("x", "y", "width", "height"))
    except (TypeError, ValueError): return None

def port(r, s, prefix):
    x, y, w, h = r
    return x + w * float(s.get(prefix + "X", .5)), y + h * float(s.get(prefix + "Y", .5))

def segments(points):
    return [(a,b) for a,b in zip(points, points[1:]) if a != b and (a[0] == b[0] or a[1] == b[1])]

def cross(a,b):
    (p,q),(r,s)=a,b
    if p[0] == q[0] and r[1] == s[1]: return cross(b,a)
    if p[1] != q[1] or r[0] != s[0]: return None
    x,y=r[0],p[1]
    return (x,y) if min(p[0],q[0]) < x < max(p[0],q[0]) and min(r[1],s[1]) < y < max(r[1],s[1]) else None

def audit(path):
    cells={c.get("id"):c for c in ET.parse(path).getroot().iter("mxCell")}
    cards={k:rect(c) for k,c in cells.items() if c.get("vertex") == "1" and "PK " in c.get("value","") and rect(c)}
    routes={}; warnings=[]
    for key,c in cells.items():
        if c.get("edge") != "1": continue
        source,target=c.get("source"),c.get("target")
        if source not in cards or target not in cards:
            warnings.append(key + ": missing endpoint geometry"); continue
        s=props(c); g=c.find("mxGeometry")
        via=[] if g is None else [(float(p.get("x")),float(p.get("y"))) for p in g.findall("./Array[@as='points']/mxPoint")]
        points=[port(cards[source],s,"exit"),*via,port(cards[target],s,"entry")]
        if any(a[0]!=b[0] and a[1]!=b[1] for a,b in zip(points,points[1:])):
            warnings.append(key + ": saved points include a diagonal; render may differ")
        routes[key]=segments(via)
    found=[]
    for (a,sa),(b,sb) in itertools.combinations(routes.items(),2):
        for first in sa:
            for second in sb:
                p=cross(first,second)
                if p: found.append((a,b,p))
    return found,warnings

if __name__ == "__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("diagram")
    args=ap.parse_args()
    crossings,warnings=audit(args.diagram)
    for a,b,(x,y) in crossings: print(f"CROSS {a} x {b} at ({x:g}, {y:g})")
    for warning in warnings: print("LIMITATION",warning)
    print(f"{len(crossings)} candidate crossing(s); {len(warnings)} route limitation(s)")

