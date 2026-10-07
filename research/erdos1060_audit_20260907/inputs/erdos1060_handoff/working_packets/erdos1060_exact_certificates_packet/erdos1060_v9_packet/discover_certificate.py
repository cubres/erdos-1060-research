"""Reproduce the affine-line certificate for the supplied cubefree target.

Discovery uses NumPy/SciPy. Verification uses only verify_v9.py and exact
arithmetic. A numerical solver status is never accepted as a certificate.
This program is tailored to the supplied example, not a general proof of
Erdos Problem 1060.
"""
from __future__ import annotations
import argparse,json
from fractions import Fraction
from math import gcd,lcm,prod
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from verify_v9 import local_model,propagate,rref,solve_unique,divisor_sum,require


def exact_dual(coefficients, columns, rhs, distinguished):
    z=[-Fraction(float(v)).limit_denominator(10**7) for v in coefficients]
    require(sum(a*b for a,b in zip(z,rhs))==0,'Rounded dual has a nonzero budget')
    require(all(sum(a*b for a,b in zip(z,c))>=int(j==distinguished)
                for j,c in enumerate(columns)), 'Rounded dual fails a column inequality')
    return z


def discover(source: Path, output: Path):
    seed=json.loads(source.read_text())
    factors={int(p):int(e) for p,e in seed['target_factorization'].items()}
    cap=int(seed['cap'])
    primes,alpha,N,domains,vectors=local_model(factors,cap)
    ds,_,_=propagate(primes,alpha,domains,vectors)
    desc=[(p,e) for p,d in zip(primes,ds) for e in d]
    cs=[list(vectors[p,e])+[int(p==q) for q in primes] for p,e in desc]
    rhs=alpha+[1]*len(primes)
    A=np.array(cs,dtype=float).T;b=np.array(rhs,dtype=float)
    z=[Fraction(0)]*len(rhs)
    for j in range(len(cs)):
        objective=np.zeros(len(cs));objective[j]=-1
        result=linprog(objective,A_eq=A,b_eq=b,bounds=(0,None),method='highs')
        require(result.success,'Numerical discovery did not finish')
        if abs(result.fun)<1e-8:
            certificate=exact_dual(result.eqlin.marginals,cs,rhs,j)
            z=[a+c for a,c in zip(z,certificate)]
    require(any(z),'No nonzero exact dual certificate was discovered')
    den=lcm(*(v.denominator for v in z));zz=[int(v*den) for v in z]
    g=gcd(*zz);zz=[v//g for v in zz]
    scores=[sum(a*c for a,c in zip(zz,col)) for col in cs]
    require(min(scores)>=0 and sum(a*c for a,c in zip(zz,rhs))==0,'Integer dual failed')
    keep=[j for j,value in enumerate(scores) if value==0]
    rows=[[cs[j][i] for j in keep] for i in range(len(rhs))]
    _,pivots=rref(rows);rank=len(pivots)
    require(rank==len(keep)-1,'The residual model is not an affine line')
    free=next(i for i in range(len(keep)) if i not in pivots)
    free_row=[int(i==free) for i in range(len(keep))]
    solutions=[]
    for value in (0,1):
        x=solve_unique(rows+[free_row],rhs+[value])
        require(all(v in (0,1) for v in x),'An affine endpoint is not binary')
        fs={desc[j][0]:desc[j][1] for j,v in zip(keep,x) if v}
        k=prod(p**e for p,e in fs.items());sig,_=divisor_sum(fs)
        require(k*sig==N,'Endpoint is not a preimage')
        solutions.append({'free_indicator':value,'exponents':fs,'input':str(k)})
    result={'target_factorization':factors,'cap':cap,'primes':primes,
            'dual_prices':zz[:len(primes)],'block_offsets':zz[len(primes):],
            'propagated_options':desc,'scores':scores,
            'remaining_options':[desc[j] for j in keep],'rank':rank,
            'free_option':desc[keep[free]],'solutions':solutions}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(f'Wrote an exact certificate to {output}')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=Path(__file__).with_name('dual_certificate.json'))
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('rediscovered_certificate.json'))
    args=parser.parse_args();discover(args.source,args.output)
