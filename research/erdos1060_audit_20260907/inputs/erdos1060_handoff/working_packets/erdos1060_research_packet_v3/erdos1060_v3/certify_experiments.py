"""Produce/check exact finite-search certificates and rational entropy inequalities.
The discovery cache is untrusted until all its factorizations and recursive Lucas
primality certificates have been checked. No numerical optimizer is used here.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import json, math, time
from sympy import factorint

HERE=Path(__file__).resolve().parent
cache=json.loads((HERE/'factor_cache.json').read_text())
primality={}

@lru_cache(None)
def certify_prime(n:int)->bool:
    if n==2:
        primality[str(n)]={'a':1,'factors':{}}
        return True
    if n<2 or n%2==0:raise ValueError(f'Not an odd prime: {n}')
    fs={int(q):int(e) for q,e in factorint(n-1).items()}
    assert math.prod(q**e for q,e in fs.items())==n-1
    for q in fs:certify_prime(q)
    a=2
    while not(pow(a,n-1,n)==1 and all(pow(a,(n-1)//q,n)!=1 for q in fs)):
        a+=1
        if a>10000:raise RuntimeError(f'No small Lucas witness: {n}')
    primality[str(n)]={'a':a,'factors':{str(q):e for q,e in fs.items()}}
    return True

def primes_through(B):
    sieve=bytearray(b'\x01')*(B+1);sieve[0:2]=b'\x00\x00'
    for p in range(2,math.isqrt(B)+1):
        if sieve[p]:sieve[p*p:B+1:p]=b'\x00'*(((B-p*p)//p)+1)
    return [p for p in range(3,B+1) if sieve[p]]

def h(p,e):return p**e * sum(p**j for j in range(e+1))

def exact_model(B,exponents):
    columns=[];blocks=0
    for p in primes_through(B):
        fac={}
        for e in exponents:
            v={int(q):int(a) for q,a in cache[f'{p}:{e}'].items()}
            assert math.prod(q**a for q,a in v.items())==h(p,e)
            for q in v:certify_prime(q)
            fac[e]=v;blocks+=1
        for a in exponents:
            for b in exponents:
                if a<=b:continue
                row={q:fac[a].get(q,0)-fac[b].get(q,0) for q in fac[a].keys()|fac[b].keys()}
                columns.append((p,a,b,{q:v for q,v in row.items() if v}))
    initial=len(columns);rounds=[]
    while columns:
        owners={}
        for p,a,b,row in columns:
            for q in row:owners.setdefault(q,set()).add(p)
        removable={q for q,ps in owners.items() if len(ps)==1}
        survivors=[c for c in columns if not any(q in removable for q in c[3])]
        if len(survivors)==len(columns):break
        rounds.append(len(columns)-len(survivors));columns=survivors
    out={'B':B,'minimum_prime':3,'exponents':exponents,'blocks_verified':blocks,'initial_columns':initial,'peel_rounds':rounds,'remaining_columns':columns}
    if not columns:out['certificate']='All columns removed by exact singleton-prime peeling.'
    else:
        assert exponents in ([0,2,4],[0,2,4,6]) and [c[:3] for c in columns]==[(3,4,0),(7,2,0),(11,2,0)]
        rows=[3,7,11];m=[[c[3].get(q,0) for c in columns] for q in rows]
        det=(m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
             -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
             +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
        assert det==18
        out.update(certificate='Remaining columns have an invertible 3 by 3 minor.',minor_rows=rows,minor=m,determinant=det)
    return out

# t=2^(-1/3). Each of these strict upper bounds follows by cubing.
t=F(397,500); t2=F(63,100); t4=F(397,1000)
assert t**3>F(1,2) and t2**3>F(1,4) and t4**3>F(1,16)
z23=1+t2;z33=F(3,2)+t
z24=1+t2+t4;z34=F(3,2)+t+t4
z2inf=1/(1-t2);z3inf=2*(1+t)
checks={
    'a3_squared':(z23**2*z33)**2 < F(3,2)**9,
    'a4':z24**2*z34 < F(3,2)**6,
    'a5_follows_from_a4':True,
    'a_at_least_6':z2inf**2*z3inf < F(3,2)**9,
}
assert all(checks.values())
start=time.monotonic()
results=[exact_model(100000,[1,2]),exact_model(10000,[0,2,4]),exact_model(1000,[0,2,4,6])]
# Independently verify the saved certificates without calls to factorint.
@lru_cache(None)
def verify_prime(n):
    if n==2:return True
    assert n>2 and n%2 and str(n) in primality
    c=primality[str(n)];fac={int(q):int(e) for q,e in c['factors'].items()};a=c['a']
    assert math.prod(q**e for q,e in fac.items())==n-1
    for q,e in fac.items():assert 1<q<n and e>0 and verify_prime(q)
    assert pow(a,n-1,n)==1
    assert all(pow(a,(n-1)//q,n)!=1 for q in fac)
    return True
for q in primality:verify_prime(int(q))
(HERE/'prime_certificates.json').write_text(json.dumps(primality,sort_keys=True))
out={'entropy_rational_checks':checks,'finite_models':results,'primality_certificates':len(primality),'maximum_certified_prime':max(map(int,primality)),'elapsed_seconds':time.monotonic()-start}
(HERE/'exact_certification.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
