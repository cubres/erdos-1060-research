"""Exact bounded-exponent inverse search given a certified target factorization.
Pure standard-library Python. No floating point is used in the search.
"""
from __future__ import annotations
from functools import lru_cache
from math import prod, isqrt
import json, argparse, time

def prime(n: int) -> bool:
    if n < 2:return False
    return all(n%d for d in range(2,isqrt(n)+1))

def inverse(factors: dict[int,int], E: int) -> tuple[list[int],dict]:
    if E<1 or any(not prime(p) or a<1 for p,a in factors.items()):
        raise ValueError('Invalid exponent bound or target factorization')
    qs=sorted(factors); N=prod(p**a for p,a in factors.items())
    variables=[]
    for p in reversed(qs):
        options=[]
        for e in range(min(E,factors[p])+1):
            block=p**e*((p**(e+1)-1)//(p-1))
            if N%block:continue
            rest=block; v=[]
            for q in qs:
                a=0
                while rest%q==0: rest//=q;a+=1
                v.append(a)
            if rest!=1:raise AssertionError('Incomplete target factorization')
            options.append((p**e,tuple(v)))
        if len(options)>1:variables.append((p,options))
    r=len(qs);m=len(variables)
    mx=[[0]*r for _ in range(m+1)]
    for i in range(m-1,-1,-1):
        for j in range(r):mx[i][j]=mx[i+1][j]+max(v[j] for _,v in variables[i][1])
    nodes=0
    @lru_cache(None)
    def visit(i: int, rem: tuple[int,...]) -> tuple[int,...]:
        nonlocal nodes
        nodes+=1
        if any(rem[j]>mx[i][j] for j in range(r)):return ()
        if i==m:return (1,) if all(x==0 for x in rem) else ()
        out=[]
        for power,v in variables[i][1]:
            if any(v[j]>rem[j] for j in range(r)):continue
            nr=tuple(rem[j]-v[j] for j in range(r))
            out.extend(power*k for k in visit(i+1,nr))
        return tuple(out)
    start=time.monotonic()
    sols=sorted(visit(0,tuple(factors[q] for q in qs)))
    if len(sols)!=len(set(sols)):raise AssertionError('Duplicate input')
    return sols,{'nodes':nodes,'variables':m,'elapsed_s':time.monotonic()-start,'cache':str(visit.cache_info())}

FACTORS={2:20,3:5,5:1,7:3,11:2,13:2,17:2,19:2,23:1,31:2,43:1,61:2,83:1,97:1,127:2,271:1,307:2,331:1,367:1,733:1,5419:1}
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--scaled',action='store_true')
    ap.add_argument('--E',type=int,default=2)
    args=ap.parse_args()
    fac=FACTORS.copy()
    if args.scaled:
        for p,a in {2:4,3:1,7:1}.items():fac[p]+=a
    sols,stats=inverse(fac,args.E)
    print(json.dumps({'E':args.E,'scaled':args.scaled,'target':str(prod(p**a for p,a in fac.items())),'count':len(sols),'solutions':list(map(str,sols)),'statistics':stats},indent=2))
