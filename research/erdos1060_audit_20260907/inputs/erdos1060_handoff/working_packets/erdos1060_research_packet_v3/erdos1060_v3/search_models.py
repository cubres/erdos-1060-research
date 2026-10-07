"""Exact valuation-model preparation and numerical MILP witness discovery.
A solver infeasibility/optimality status is not an exact proof certificate.
"""
from __future__ import annotations
import argparse, json, math, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
from sympy import primerange, factorint


def h(p,e): return p**e * ((p**(e+1)-1)//(p-1))

def build(B,lo,exponents,excluded=()):
    ps=[int(p) for p in primerange(lo,B+1) if p not in excluded]
    cachepath=Path(__file__).parent/'factor_cache.json'
    cache=json.loads(cachepath.read_text()) if cachepath.exists() else {}
    fac={}
    for p in ps:
        for e in exponents:
            key=f'{p}:{e}'
            if key not in cache:
                cache[key]={str(q):int(v) for q,v in factorint(h(p,e)).items()}
            fac[p,e]={int(q):v for q,v in cache[key].items()}
    cachepath.write_text(json.dumps(cache))
    # Unordered exponent pairs have both possible orientations in the MILP.
    columns=[]
    for p in ps:
        for a in exponents:
            for b in exponents:
                if a<=b: continue
                fa,fb=fac[p,a],fac[p,b]
                v={q:fa.get(q,0)-fb.get(q,0) for q in fa.keys()|fb.keys()}
                columns.append((p,a,b,{q:d for q,d in v.items() if d}))
    initial=len(columns); rounds=[]
    # A valuation row involving only one input prime cannot be canceled:
    # each collision chooses at most one exponent pair at that prime.
    while columns:
        rows={}
        for p,a,b,v in columns:
            for q in v:rows.setdefault(q,set()).add(p)
        singleton={q for q,p in rows.items() if len(p)==1}
        new=[c for c in columns if not(singleton&c[3].keys())]
        if len(new)==len(columns):break
        rounds.append(len(columns)-len(new));columns=new
    return columns,{'input_primes':len(ps),'initial_pairs':initial,'surviving_pairs':len(columns),'surviving_primes':len(set(c[0] for c in columns)),'peel_rounds':rounds}

def solve(B,lo,exponents,seconds,excluded=(),seed=0):
    start=time.monotonic();cols,stats=build(B,lo,exponents,excluded)
    out={'B':B,'min_prime':lo,'exponents':exponents,'excluded':list(excluded),'statistics':stats}
    if not cols:
        return dict(out,exact_peeling_no_collision=True,elapsed=time.monotonic()-start)
    ps=sorted({c[0] for c in cols}); qs=sorted({q for c in cols for q in c[3]})
    pi={p:i for i,p in enumerate(ps)};qi={q:i for i,q in enumerate(qs)}
    rr=[];cc=[];dd=[];variables=[];cost=[]
    rng=np.random.default_rng(seed)
    for p,a,b,v in cols:
        for sign in (1,-1):
            j=len(variables);variables.append((p,a,b) if sign==1 else (p,b,a))
            for q,d in v.items():rr.append(qi[q]);cc.append(j);dd.append(sign*d)
            rr.extend((len(qs)+pi[p],len(qs)+len(ps)))
            cc.extend((j,j));dd.extend((1,1))
            cost.append((a+b)*math.log(p)*(1+.001*rng.random()))
    mat=coo_matrix((dd,(rr,cc)),shape=(len(qs)+len(ps)+1,len(variables))).tocsc()
    lb=np.r_[np.zeros(len(qs)),np.zeros(len(ps)),1]
    ub=np.r_[np.zeros(len(qs)),np.ones(len(ps)),np.inf]
    res=milp(np.array(cost),integrality=np.ones(len(variables)),bounds=Bounds(0,1),constraints=LinearConstraint(mat,lb,ub),options={'time_limit':seconds,'mip_rel_gap':0.05})
    out.update(status=int(res.status),message=str(res.message),elapsed=time.monotonic()-start)
    if res.x is not None:
        chosen=[v for v,x in zip(variables,res.x) if x>.5]
        a=math.prod(p**e for p,e,f in chosen);b=math.prod(p**f for p,e,f in chosen)
        ha=math.prod(h(p,e) for p,e,f in chosen);hb=math.prod(h(p,f) for p,e,f in chosen)
        valid=len({p for p,e,f in chosen})==len(chosen) and a!=b and ha==hb
        out.update(chosen=chosen,a=str(a),b=str(b),target=str(ha),verified=valid)
        if valid:
            out.update(minimum_actual_prime=min(p for p,e,f in chosen),roughness_ratio=min(p for p,e,f in chosen)/math.log(ha),support_size=len(chosen))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--B',type=int,default=10000);ap.add_argument('--lo',type=int,default=3);ap.add_argument('--exponents',default='0,1,2');ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--out',required=True);ap.add_argument('--exclude',default='');ap.add_argument('--seed',type=int,default=0)
    args=ap.parse_args()
    out=solve(args.B,args.lo,sorted(set(map(int,args.exponents.split(',')))),args.seconds,tuple(int(s) for s in args.exclude.split(',') if s),args.seed)
    Path(args.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
