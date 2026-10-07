#!/usr/bin/env python3
"""Find an h-collision avoiding a prescribed set of input base primes."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix, vstack

SEARCH_DIR=Path("/Users/cubres/Documents/ChatGPT/Research/ksigma_rough_collision_search_2026-09-05")
sys.path.insert(0,str(SEARCH_DIR))
from search import make_columns,relation_core,verify

HERE=Path(__file__).parent
sys.path.insert(0,str(HERE))
from relation_decompose import atoms,differing_columns


def build(columns):
    n=len(columns); bases=sorted({p for p,e,f in columns});rows=sorted({q for p,e,f in columns for q in f});ri={q:i for i,q in enumerate(rows)}
    rr=[];cc=[];data=[]
    for j,(p,e,f) in enumerate(columns):
        for q,a in f.items():
            i=ri[q];rr.extend((i,i));cc.extend((j,n+j));data.extend((a,-a))
    mats=[coo_matrix((data,(rr,cc)),shape=(len(rows),2*n)).tocsc()];lo=[0.]*len(rows);hi=[0.]*len(rows)
    by=defaultdict(list)
    for j,(p,e,f) in enumerate(columns):by[p].append(j)
    rr=[];cc=[];data=[];row=0
    for p in bases:
        for off in (0,n):
            for j in by[p]:rr.append(row);cc.append(off+j);data.append(1)
            lo.append(0.);hi.append(1.);row+=1
    for j in range(n):
        rr.extend((row,row));cc.extend((j,n+j));data.extend((1,1));lo.append(0.);hi.append(1.);row+=1
    for j in range(2*n):rr.append(row);cc.append(j);data.append(1)
    lo.append(1.);hi.append(float(2*n));row+=1
    mats.append(coo_matrix((data,(rr,cc)),shape=(row,2*n)).tocsc())
    return vstack(mats,format='csc'),np.array(lo),np.array(hi)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--upper',type=int,default=3000);ap.add_argument('--max-exponent',type=int,default=8);ap.add_argument('--seconds',type=float,default=300);ap.add_argument('--forbid',default='2,3,5,7,13,31,127');ap.add_argument('--output',type=Path,default=HERE/'third_disjoint_atom.json');ap.add_argument('--seeded',action='store_true');ap.add_argument('--seed-bases',type=int,default=30);ap.add_argument('--feasibility',action='store_true');args=ap.parse_args()
    forbidden={int(x) for x in args.forbid.split(',') if x}
    original,_=make_columns(2,args.upper,args.max_exponent)
    filtered=[c for c in original if c[0] not in forbidden]
    occurrences=defaultdict(set)
    for j,(_,_,f) in enumerate(filtered):
        for q in f:occurrences[q].add(j)
    columns=relation_core(filtered,occurrences);n=len(columns)
    print(f'upper={args.upper} e={args.max_exponent} original={len(original)} filtered={len(filtered)} core={n} bases={len(set(p for p,e,f in columns))} forbidden={sorted(forbidden)}',flush=True)
    A,lo,hi=build(columns)
    # The two sides have the same v2 by valuation balance.  Minimize twice
    # that common exponent, with a tiny block-count tie-breaker.
    objective=np.zeros(2*n)
    for j,(_,_,f) in enumerate(columns):
        objective[j]=objective[n+j]=1000*f.get(2,0)+1
    if args.feasibility: objective[:]=0
    seeds=[None]
    if args.seeded:
        selected_bases=sorted({p for p,e,f in columns})[:args.seed_bases]
        seeds=[j for j,(p,e,f) in enumerate(columns) if p in selected_bases]
    result=None
    for position,seed in enumerate(seeds,1):
        lower_bounds=np.zeros(2*n);upper_bounds=np.ones(2*n)
        if seed is not None:lower_bounds[seed]=upper_bounds[seed]=1
        result=milp(objective,integrality=np.ones(2*n),bounds=Bounds(lower_bounds,upper_bounds),constraints=LinearConstraint(A,lo,hi),options={'time_limit':args.seconds,'presolve':True,'mip_rel_gap':0.0})
        if position%10==0 or result.x is not None:print(f'seed {position}/{len(seeds)} {None if seed is None else columns[seed][:2]}: {result.message}',flush=True)
        if result.x is not None:break
    if result is None:
        print('NO_SOLVER_RESULT',flush=True);return 1
    if result.x is None:
        print(f'NO_HIT status={int(result.status)} message={result.message}',flush=True);return 1
    left=[(columns[j][0],columns[j][1]) for j in range(n) if result.x[j]>.5]
    right=[(columns[j][0],columns[j][1]) for j in range(n) if result.x[n+j]>.5]
    cert=verify(left,right,1)
    pieces=atoms(differing_columns(dict(left),dict(right)))
    candidates=[]
    for piece in pieces:
        L=[(p,e) for side,p,e in piece if side=='L'];R=[(p,e) for side,p,e in piece if side=='R']
        C=verify(L,R,1);C['target_v2']=C['common_h_factorization'].get('2',0);C['target_max_valuation']=max(C['common_h_factorization'].values());C['input_support']=sorted({p for p,e in L+R});candidates.append(C)
    cert={'forbidden_bases':sorted(forbidden),'milp_relation':cert,'atoms':candidates,'search':{'upper':args.upper,'max_exponent':args.max_exponent,'core_columns':n,'status':int(result.status),'message':result.message,'seed':None if seeds==[None] else list(columns[seed][:2])}}
    args.output.write_text(json.dumps(cert,indent=2)+'\n');print(json.dumps(cert,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
