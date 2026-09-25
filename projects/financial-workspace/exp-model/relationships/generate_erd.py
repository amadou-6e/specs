"""Generate a one-page, routed crow's-foot ERD from graph.yaml."""
from __future__ import annotations
import heapq, html, json, math, re, tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
GRAPH=json.loads((HERE/"graph.yaml").read_text(encoding="utf-8"))
OUT=HERE/"layered-erd.drawio"
PREVIEW=Path(tempfile.gettempdir())/"financial-workspace-layered-erd-preview.html"
W,H=2500,1920
BW=250
STEP=20
NODES={
 "financial-institution":(570,235),"employer":(100,235),
 "recurring-expense":(1510,235),"recurring-income":(100,360),"procurement":(1980,235),"liability":(1040,235),
 "account":(570,490),"income-statement":(100,490),
 "commitment-term":(1510,490),"procurement-item":(1980,490),"liability-term":(1040,490),
 "transaction-statement":(570,745),"income-statement-item":(100,745),
 "payment-occurrence":(1510,745),"receipt":(1980,745),"balance-item":(1040,745),
 "transaction":(1090,1050),"cashflow-entry":(1090,1370),"cashflow-sheet":(1090,1650),
}
LANES=[
 ("Accounts and statements",535,140,360,770,"#EEF5FA"),
 ("Employment income",65,140,360,770,"#F5F1FA"),
 ("Recurring expenses",1475,140,360,770,"#F1F6EE"),
 ("Procurement and receipts",1945,140,360,770,"#FFF6EC"),
 ("Liabilities",1005,140,360,770,"#F8F0F1"),
 ("Booked movements",65,955,2300,320,"#EDF4F8"),
 ("Cashflow reporting",65,1295,2300,570,"#E9F4ED"),
]
SYM={"1":"ERmandOne","0..1":"ERzeroToOne","0..*":"ERzeroToMany","1..*":"ERoneToMany"}
OBJ={o["id"]:o for o in GRAPH["objects"]}
assert set(NODES)==set(OBJ)
def foreign_keys(n):
 text=(HERE.parent/"objects"/n/"schema.yaml").read_text(encoding="utf-8-sig")
 block=text.split("foreign_keys:",1)[1].split("\nfields:",1)[0] if "foreign_keys:" in text else ""
 return re.findall(r"^  ([A-Za-z_][A-Za-z_0-9]*):$",block,re.M)
FKS={n:foreign_keys(n) for n in NODES}
NODE_H={n:max(110,58+22*len(FKS[n])) for n in NODES}
CATEGORIES={
 "Party":("#D7E7FB",{"financial-institution","employer"}),
 "Account or obligation":("#F7DDD6",{"account","liability","recurring-expense","recurring-income"}),
 "Document":("#E8DFF8",{"transaction-statement","income-statement","receipt"}),
 "Activity":("#D7F0DF",{"transaction","payment-occurrence","procurement"}),
 "Detail or term":("#F7EDC9",{"balance-item","liability-term","commitment-term","procurement-item","income-statement-item"}),
 "Reporting":("#D9EAF2",{"cashflow-entry","cashflow-sheet"}),
}
NODE_COLOR={n:color for color,names in CATEGORIES.values() for n in names}
assert set(NODE_COLOR)==set(NODES)

def center(n):
 x,y=NODES[n];return x+BW/2,y+NODE_H[n]/2
def side(s,t):
 x,y=center(s);X,Y=center(t)
 dx,dy=X-x,Y-y
 if abs(dy)>abs(dx)*0.65:return "bottom" if dy>0 else "top"
 return "right" if dx>0 else "left"
rels=GRAPH["relationships"]
ports=defaultdict(list)
for i,r in enumerate(rels):
 ports[(r["source"],side(r["source"],r["target"]))].append((i,"source"))
 ports[(r["target"],side(r["target"],r["source"]))].append((i,"target"))
endpoint={}
for (n,s),items in ports.items():
 x,y=NODES[n]
 for rank,(i,end) in enumerate(items,1):
  q=rank/(len(items)+1)
  if s=="top":p=(x+q*BW,y);rel=(q,0);outer=(p[0],p[1]-40)
  elif s=="bottom":p=(x+q*BW,y+NODE_H[n]);rel=(q,1);outer=(p[0],p[1]+40)
  elif s=="left":p=(x,y+q*NODE_H[n]);rel=(0,q);outer=(p[0]-40,p[1])
  else:p=(x+BW,y+q*NODE_H[n]);rel=(1,q);outer=(p[0]+40,p[1])
  endpoint[(i,end)]=(p,outer,rel,s)
def grid(p):return (round(p[0]/STEP),round(p[1]/STEP))
blocked={(gx,gy) for gx in range(W//STEP) for gy in range(0,7)}
for n,(x,y) in NODES.items():
 for gx in range(math.floor((x-8)/STEP),math.ceil((x+BW+8)/STEP)+1):
  for gy in range(math.floor((y-8)/STEP),math.ceil((y+NODE_H[n]+8)/STEP)+1):
   blocked.add((gx,gy))
used=defaultdict(int)
used_axis=defaultdict(lambda: defaultdict(int))
def route(a,b):
 start,goal=grid(a),grid(b)
 frontier=[(0,0,start,None)]
 best={(start,None):0}
 prev={}
 final=None
 while frontier:
  _,cost,p,d=heapq.heappop(frontier)
  state=(p,d)
  if cost!=best.get(state):continue
  if p==goal:final=state;break
  for v in ((1,0),(-1,0),(0,1),(0,-1)):
   nxt=(p[0]+v[0],p[1]+v[1])
   if not 1<=nxt[0]<W//STEP-1 or not 1<=nxt[1]<H//STEP-1:continue
   if nxt in blocked and nxt not in (start,goal):continue
   axis='h' if v[0] else 'v'
   opposite='v' if axis=='h' else 'h'
   nc=cost+1+(0.9 if d and d!=v else 0)+2.5*used[nxt]+25*used_axis[nxt][opposite]
   ns=(nxt,v)
   if nc<best.get(ns,float("inf")):
    best[ns]=nc;prev[ns]=state
    heuristic=abs(nxt[0]-goal[0])+abs(nxt[1]-goal[1])
    heapq.heappush(frontier,(nc+heuristic,nc,nxt,v))
 if final is None:raise RuntimeError(f"No clear route {a} to {b}")
 cells=[]
 while final!=(start,None):
  cells.append(final[0]);final=prev[final]
 cells.append(start);cells.reverse()
 for c in cells:used[c]+=1
 for left,right in zip(cells,cells[1:]):
  axis='h' if left[1]==right[1] else 'v'
  used_axis[left][axis]+=1
  used_axis[right][axis]+=1
 pts=[(c[0]*STEP,c[1]*STEP) for c in cells]
 compact=[pts[0]]
 for k in range(1,len(pts)-1):
  a,b,c=pts[k-1],pts[k],pts[k+1]
  if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):compact.append(b)
 compact.append(pts[-1])
 return compact
mx=ET.Element("mxfile",{"host":"app.diagrams.net","type":"device","version":"24.7.17"})
diag=ET.SubElement(mx,"diagram",{"name":"Full ERD","id":"full-layered-erd"})
model=ET.SubElement(diag,"mxGraphModel",{"dx":str(W),"dy":str(H),"grid":"1","gridSize":"10","guides":"1","tooltips":"1","connect":"1","arrows":"1","fold":"1","page":"1","pageScale":"1","pageWidth":str(W),"pageHeight":str(H),"math":"0","shadow":"0"})
root=ET.SubElement(model,"root")
ET.SubElement(root,"mxCell",{"id":"0"});ET.SubElement(root,"mxCell",{"id":"1","parent":"0"})
def vertex(id,value,x,y,w,h,style):
 c=ET.SubElement(root,"mxCell",{"id":id,"value":value,"style":style,"vertex":"1","parent":"1"})
 ET.SubElement(c,"mxGeometry",{"x":str(x),"y":str(y),"width":str(w),"height":str(h),"as":"geometry"})
vertex("title","Financial workspace · Entity relationships",80,25,2400,65,"text;html=1;strokeColor=none;fillColor=none;fontSize=31;fontStyle=1;fontColor=#152B40;align=left;")
for i,(label,lx,ly,lw,lh,fill) in enumerate(LANES):
 vertex(f"lane-{i}",label,lx,ly,lw,lh,
        f"swimlane;horizontal=1;startSize=45;rounded=0;html=1;fillColor={fill};swimlaneFillColor={fill};strokeColor=#C7D3DE;strokeWidth=1.5;fontColor=#40576D;fontSize=17;fontStyle=1;align=left;spacingLeft=16;container=0;")
for i,(category,(color,_)) in enumerate(CATEGORIES.items()):
 vertex(f"legend-{i}",category,80+i*370,108,350,25,
        f"text;html=1;strokeColor=none;fillColor={color};fontColor=#243B52;fontSize=13;align=center;verticalAlign=middle;")
for n,(x,y) in NODES.items():
 name=n.replace("-"," ").title()
 fk_lines="".join(f"<br><font color='#475E72'>FK {key}</font>" for key in FKS[n])
 value=f"<b><font style='font-size:16px'>{name}</font></b><br><font color='#344E66'>PK {OBJ[n]['identity']}</font>{fk_lines}"
 fill=NODE_COLOR[n]
 vertex(n,value,x,y,BW,NODE_H[n],f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#294968;strokeWidth=2;fontColor=#17324B;fontSize=13;align=left;verticalAlign=top;spacingTop=10;spacingLeft=13;")
def strict_crossings(paths):
 def crosses(a,b,c,d):
  if a[0]==b[0] and c[1]==d[1]:
   return min(a[1],b[1])<c[1]<max(a[1],b[1]) and min(c[0],d[0])<a[0]<max(c[0],d[0])
  if a[1]==b[1] and c[0]==d[0]:
   return min(a[0],b[0])<c[0]<max(a[0],b[0]) and min(c[1],d[1])<a[1]<max(c[1],d[1])
  return False
 n=0
 for i,p in enumerate(paths):
  for q in paths[:i]:
   for a,b in zip(p,p[1:]):
    for c,d in zip(q,q[1:]):
     n+=crosses(a,b,c,d)
 return n
import random
indices=list(range(len(rels)))
def distance(i):
 a=endpoint[(i,"source")][1];b=endpoint[(i,"target")][1]
 return abs(a[0]-b[0])+abs(a[1]-b[1])
orders=[indices,list(reversed(indices)),sorted(indices,key=distance),sorted(indices,key=distance,reverse=True)]
for seed in range(12):
 order=indices[:];random.Random(seed).shuffle(order);orders.append(order)
best=None
for order in orders:
 used.clear();used_axis.clear()
 candidate={}
 for i in order:
  candidate[i]=route(endpoint[(i,"source")][1],endpoint[(i,"target")][1])
 preview=[[endpoint[(i,"source")][0],endpoint[(i,"source")][1]]+candidate[i]+[endpoint[(i,"target")][1],endpoint[(i,"target")][0]] for i in indices]
 score=strict_crossings(preview)
 if best is None or score<best[0]:best=(score,candidate)
paths=best[1]
preview_edges=[]
for i,r in enumerate(rels):
 sp,so,srel,ss=endpoint[(i,"source")]
 tp,to,trel,ts=endpoint[(i,"target")]
 path=paths[i]
 # Include short perpendicular stubs from each cardinality marker to the routed path.
 points=[so]+path+[to]
 points=list(dict.fromkeys(points))
 style=(f"edgeStyle=segmentEdgeStyle;rounded=0;html=1;strokeColor=#3D607E;strokeWidth=1.8;"
        f"startArrow={SYM[r['sources_per_target']]};endArrow={SYM[r['targets_per_source']]};"
        f"startSize=18;endSize=18;startFill=0;endFill=0;"
        f"exitX={srel[0]:.4f};exitY={srel[1]:.4f};entryX={trel[0]:.4f};entryY={trel[1]:.4f};")
 e=ET.SubElement(root,"mxCell",{"id":f"edge-{i}","value":"","style":style,"edge":"1","parent":"1","source":r["source"],"target":r["target"]})
 g=ET.SubElement(e,"mxGeometry",{"relative":"1","as":"geometry"})
 arr=ET.SubElement(g,"Array",{"as":"points"})
 for x,y in points:ET.SubElement(arr,"mxPoint",{"x":str(round(x,2)),"y":str(round(y,2))})
 preview_edges.append([sp]+points+[tp])
ET.ElementTree(mx).write(OUT,encoding="utf-8",xml_declaration=True)
ET.parse(OUT)
# Independently verify every routed segment stays outside every non-endpoint entity.
for i,path in enumerate(preview_edges):
 src,dst=rels[i]["source"],rels[i]["target"]
 for a,b in zip(path,path[1:]):
  for n,(x,y) in NODES.items():
   if n in (src,dst):continue
   if a[0]==b[0] and x<a[0]<x+BW and max(a[1],b[1])>y and min(a[1],b[1])<y+NODE_H[n]:
    raise AssertionError(f"{rels[i]['id']} crosses {n}")
   if a[1]==b[1] and y<a[1]<y+NODE_H[n] and max(a[0],b[0])>x and min(a[0],b[0])<x+BW:
    raise AssertionError(f"{rels[i]['id']} crosses {n}")
parts=[f'<html><body style="margin:0;background:#f7f9fb"><svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
parts += ['<text x="80" y="65" font-family="Arial" font-size="31" font-weight="bold" fill="#152B40">Financial workspace · Entity relationships</text>']
for label,lx,ly,lw,lh,fill in LANES:
 parts.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="{fill}" stroke="#C7D3DE" stroke-width="1.5"/>')
 parts.append(f'<text x="{lx+16}" y="{ly+30}" font-family="Arial" font-size="17" font-weight="bold" fill="#40576D">{html.escape(label)}</text>')
for i,(category,(color,_)) in enumerate(CATEGORIES.items()):
 lx=80+i*370
 parts.append(f'<rect x="{lx}" y="108" width="350" height="25" fill="{color}" stroke="none"/>')
 parts.append(f'<text x="{lx+175}" y="125" text-anchor="middle" font-family="Arial" font-size="13" fill="#243B52">{html.escape(category)}</text>')
for path in preview_edges:
 pts=" ".join(f"{x:.1f},{y:.1f}" for x,y in path)
 parts.append(f'<polyline points="{pts}" fill="none" stroke="#7390A8" stroke-width="1.6"/>')
for n,(x,y) in NODES.items():
 parts.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{NODE_H[n]}" fill="{NODE_COLOR[n]}" stroke="#294968" stroke-width="2"/>')
 parts.append(f'<text x="{x+13}" y="{y+28}" font-family="Arial" font-size="16" font-weight="bold" fill="#17324B">{html.escape(n.replace("-"," ").title())}</text>')
 parts.append(f'<text x="{x+13}" y="{y+50}" font-family="Arial" font-size="12" fill="#344E66">PK {html.escape(OBJ[n]["identity"])}</text>')
 for j,key in enumerate(FKS[n]):
  parts.append(f'<text x="{x+13}" y="{y+72+j*20}" font-family="Arial" font-size="12" fill="#475E72">FK {html.escape(key)}</text>')
parts.append("</svg></body></html>")
PREVIEW.write_text("".join(parts),encoding="utf-8")
print(f"{len(NODES)} entities, {len(rels)} relationships, one page; {best[0]} strict crossings; no connector crosses an unrelated entity.")



