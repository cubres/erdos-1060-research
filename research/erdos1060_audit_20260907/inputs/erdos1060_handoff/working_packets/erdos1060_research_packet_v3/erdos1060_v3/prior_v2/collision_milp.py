"""Exploratory prime-support MILP. Floating-point MILP is a search tool only;
all reported witnesses are recomputed with exact integer arithmetic.
No infeasibility result from this script is used as a mathematical proof.
"""
from __future__ import annotations
import argparse, json, time
import numpy as np
from sympy import primerange, factorint
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

def hblock(p: int, e: int) -> int:
    return p**e * ((p**(e+1)-1)//(p-1))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prime-limit',type=int,default=2000)
    ap.add_argument('--max-exponent',type=int,default=2)
    ap.add_argument('--time-limit',type=float,default=30)
    ap.add_argument('--min-prime',type=int,default=3)
    ap.add_argument('--output',default='milp_search.json')
    args=ap.parse_args()
    if args.max_exponent < 1 or args.min_prime < 2 or args.prime_limit < args.min_prime or args.time_limit <= 0:
        ap.error('Require exponent >= 1, 2 <= min-prime <= prime-limit, and a positive time limit.')
    primes=list(map(int,primerange(args.min_prime,args.prime_limit+1)))
    if not primes:
        ap.error('The specified interval contains no primes.')
    factors={(p,e):{int(q):int(v) for q,v in factorint(hblock(p,e)).items()} for p in primes for e in range(args.max_exponent+1)}
    qs=sorted({q for f in factors.values() for q in f})
    qi={q:i for i,q in enumerate(qs)}
    variables=[(p,a,b) for p in primes for a in range(args.max_exponent+1) for b in range(args.max_exponent+1) if a!=b]
    rr=[]; cc=[]; vv=[]; cost=[]
    pi={p:i for i,p in enumerate(primes)}
    for j,(p,a,b) in enumerate(variables):
        fa=factors[p,a]; fb=factors[p,b]
        for q in set(fa)|set(fb):
            val=fa.get(q,0)-fb.get(q,0)
            if val: rr.append(qi[q]);cc.append(j);vv.append(val)
        rr.append(len(qs)+pi[p]);cc.append(j);vv.append(1)
        rr.append(len(qs)+len(primes));cc.append(j);vv.append(1)
        cost.append((a+b)*np.log(p))
    A=coo_matrix((vv,(rr,cc)),shape=(len(qs)+len(primes)+1,len(variables))).tocsc()
    lower=np.r_[np.zeros(len(qs)),np.zeros(len(primes)),1]
    upper=np.r_[np.zeros(len(qs)),np.ones(len(primes)),np.inf]
    t=time.monotonic()
    res=milp(np.array(cost),integrality=np.ones(len(variables)),bounds=Bounds(0,1),constraints=LinearConstraint(A,lower,upper),options={'time_limit':args.time_limit})
    out={'settings':vars(args),'status':int(res.status),'message':str(res.message),'elapsed_s':time.monotonic()-t,'variables':len(variables),'rows':A.shape[0], 'note':'Floating-point MILP infeasibility and optimality reports are NOT exact proof certificates. Only an independently verified integer witness is certified.'}
    if res.x is not None:
        chosen=[v for v,x in zip(variables,res.x) if x>.5]
        left=right=hl=hr=1
        for p,a,b in chosen:
            left*=p**a;right*=p**b;hl*=hblock(p,a);hr*=hblock(p,b)
        out.update(chosen=chosen,left=str(left),right=str(right),h_left=str(hl),h_right=str(hr),exact_witness_valid=bool(len(chosen)==len({p for p,a,b in chosen}) and left!=right and hl==hr))
    with open(args.output,'w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
