"""Exploratory cubefree collision search; requires NumPy and SciPy.
Usage: python search_general.py MIN_PRIME MAX_PRIME SEED SECONDS
Run verify_v5.py first to check the cached local factorizations.
A failed search, or a zero random-objective optimum, is not a proof of
nonexistence. Returned witnesses are checked with exact integer products.
"""
import json,math,time,sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
HERE = Path(__file__).resolve().parent
if len(sys.argv) != 5:
 raise SystemExit("Usage: python search_general.py MIN_PRIME MAX_PRIME SEED SECONDS")
lo=int(sys.argv[1]);hi=int(sys.argv[2]);seed=int(sys.argv[3]);limit=float(sys.argv[4])
if not (3 <= lo <= hi <= 100000 and limit > 0):
 raise SystemExit("Require 3 <= MIN_PRIME <= MAX_PRIME <= 100000, and SECONDS > 0.")
F=json.loads((HERE/'factor_cache.json').read_text())
ps=sorted({int(k.split(':')[0]) for k in F if k.endswith(':1') and lo<=int(k.split(':')[0])<=hi})
cols=[]
for p in ps:
 d1={int(q):v for q,v in F[f'{p}:1'].items()};d2={int(q):v for q,v in F[f'{p}:2'].items()}
 cols += [(p,1,0,d1),(p,2,0,d2),(p,2,1,{q:d2.get(q,0)-d1.get(q,0) for q in d1.keys()|d2.keys() if d2.get(q,0)!=d1.get(q,0)})]
while cols:
 own=defaultdict(set)
 for p,a,b,d in cols:
  for q in d:own[q].add(p)
 forced={q for q,v in own.items() if len(v)==1}
 kept=[c for c in cols if forced.isdisjoint(c[3])]
 if len(kept)==len(cols):break
 cols=kept
G=defaultdict(list)
for c in cols:G[c[0]].append(c)
cols=[c for ls in G.values() for c in ls if len(ls)==1 or c[2]==0]
qs=sorted({q for p,a,b,d in cols for q in d});qi={q:i for i,q in enumerate(qs)}
rows=[];cis=[];vs=[];groups=defaultdict(list)
for j,(p,a,b,d) in enumerate(cols):
 groups[p].append(j)
 for q,v in d.items():rows.append(qi[q]);cis.append(j);vs.append(v)
lb=[0.]*len(qs);ub=lb.copy()
for p,js in groups.items():
 if len(js)==2:
  row=len(lb);lb.append(-1);ub.append(1)
  for j in js:rows.append(row);cis.append(j);vs.append(1)
print('model',lo,hi,len(cols),len(groups),flush=True)
if not cols:sys.exit(0)
A=coo_matrix((vs,(rows,cis)),shape=(len(lb),len(cols))).tocsc();c=np.random.default_rng(seed).choice([-1.,1.],len(cols))
t=time.monotonic();res=milp(c,integrality=np.ones(len(cols)),bounds=Bounds(-1.,1.),constraints=LinearConstraint(A,lb,ub),options={'presolve':False,'time_limit':limit,'threads':1})
out={'lo':lo,'hi':hi,'seed':seed,'status':int(res.status),'message':res.message,'time':time.monotonic()-t,'witness':None}
if res.x is not None:
 x=np.rint(res.x).astype(int);terms=[]
 for p,js in groups.items():
  if len(js)==1:
   j=js[0];_,a,b,_=cols[j]
   if x[j]:terms.append((p,a,b) if x[j]==1 else (p,b,a))
  else:
   d={cols[j][1]:int(x[j]) for j in js}
   if any(d.values()):terms.append((p,next((e for e,v in d.items() if v==1),0),next((e for e,v in d.items() if v==-1),0)))
 if terms:
  a=math.prod(p**e for p,e,f in terms);b=math.prod(p**f for p,e,f in terms)
  ha=math.prod(p**e*sum(p**i for i in range(e+1)) for p,e,f in terms);hb=math.prod(p**f*sum(p**i for i in range(f+1)) for p,e,f in terms)
  assert ha==hb and a!=b
  out['witness']={'terms':terms,'a':str(a),'b':str(b),'target':str(ha),'support':len(terms),'roughness_ratio':min(p for p,e,f in terms)/math.log(ha)}
print(json.dumps(out,indent=2),flush=True)
(HERE/f'search_run_{lo}_{hi}_{seed}.json').write_text(json.dumps(out,indent=2)+'\n')
