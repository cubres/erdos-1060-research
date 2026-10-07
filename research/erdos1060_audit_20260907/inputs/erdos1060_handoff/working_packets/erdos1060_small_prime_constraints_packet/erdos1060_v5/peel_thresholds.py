"""Reproduce threshold experiments using cached local factorizations.
Standard library only. Run verify_v5.py to certify the relevant arithmetic.
Finite prime-factor ranges do not establish unbounded-prime injectivity.
"""
from pathlib import Path
import json,time
from collections import defaultdict
BASE=Path(__file__).resolve().parent
fs=json.load(open(BASE/'factor_cache.json'))
cols=[]
for p in sorted({int(s.split(':')[0]) for s in fs if s.endswith(':1') and int(s.split(':')[0])<=100000}):
 f1={int(q):v for q,v in fs[f'{p}:1'].items()};f2={int(q):v for q,v in fs[f'{p}:2'].items()}
 cols += [(p,1,0,f1),(p,2,0,f2),(p,2,1,{q:f2.get(q,0)-f1.get(q,0) for q in f1.keys()|f2.keys() if f2.get(q,0)!=f1.get(q,0)})]
def peel(cc):
 rr=[]
 while cc:
  owners=defaultdict(set)
  for p,a,b,d in cc:
   for q in d:owners[q].add(p)
  single={q for q,v in owners.items() if len(v)==1}
  new=[c for c in cc if single.isdisjoint(c[3])]
  if len(new)==len(cc):break
  rr.append(len(cc)-len(new));cc=new
 return cc,rr
out=[]
for lower in [3,5,7,11,17,31,51,101,151,201,251,301,401,501,701,1001,2001,5001]:
 c=[c for c in cols if c[0]>=lower];remaining,rounds=peel(c)
 res={'lower':lower,'upper':100000,'start':len(c),'remaining':len(remaining),'remaining_primes':len({c[0] for c in remaining}),'rounds':rounds}
 out.append(res);print(res,flush=True)
(BASE/'peel_thresholds_recomputed.json').write_text(json.dumps(out,indent=2)+'\n')
