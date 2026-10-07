"""Standalone verifier: Python standard library only, exact integer arithmetic.
Run beside factor_cache.json and prime_certificates.json. Independently checks
all factorizations used in the three finite noncollision certificates, proves
primality from recursive Lucas certificates, and repeats exact peeling.
"""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from fractions import Fraction as F
import json, math
HERE=Path(__file__).resolve().parent
FACTORS=json.loads((HERE/'factor_cache.json').read_text())
CERTS=json.loads((HERE/'prime_certificates.json').read_text())

@lru_cache(None)
def prime_certificate(n:int)->bool:
    if n==2:return True
    assert n>2 and n%2==1
    cert=CERTS[str(n)];a=int(cert['a']);fs={int(p):int(e) for p,e in cert['factors'].items()}
    assert math.prod(p**e for p,e in fs.items())==n-1
    assert all(1<p<n and e>0 and prime_certificate(p) for p,e in fs.items())
    assert pow(a,n-1,n)==1
    assert all(pow(a,(n-1)//p,n)!=1 for p in fs)
    return True

def prime_list(B):
    mark=bytearray(b'\1')*(B+1);mark[:2]=b'\0\0'
    for d in range(2,math.isqrt(B)+1):
        if mark[d]:
            for k in range(d*d,B+1,d):mark[k]=0
    return [p for p in range(3,B+1) if mark[p]]

def verify_model(B,exponents):
    columns=[]
    for p in prime_list(B):
        local={}
        for e in exponents:
            fs={int(q):int(v) for q,v in FACTORS[f'{p}:{e}'].items()}
            assert all(v>0 and prime_certificate(q) for q,v in fs.items())
            assert math.prod(q**v for q,v in fs.items())==p**e*sum(p**i for i in range(e+1))
            local[e]=fs
        for a in exponents:
            for b in exponents:
                if a<=b:continue
                row={q:local[a].get(q,0)-local[b].get(q,0) for q in local[a].keys()|local[b].keys()}
                columns.append((p,a,b,{q:v for q,v in row.items() if v}))
    initial=len(columns);rounds=[]
    while columns:
        input_owners={}
        for p,a,b,row in columns:
            for q in row:input_owners.setdefault(q,set()).add(p)
        forced_rows={q for q,owners in input_owners.items() if len(owners)==1}
        kept=[c for c in columns if all(q not in forced_rows for q in c[3])]
        if len(kept)==len(columns):break
        rounds.append(len(columns)-len(kept));columns=kept
    determinant=None
    if columns:
        assert [c[:3] for c in columns]==[(3,4,0),(7,2,0),(11,2,0)]
        m=[[c[3].get(q,0) for c in columns] for q in (3,7,11)]
        determinant=(m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
                     -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                     +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
        assert determinant==18
    return {'prime_bound':B,'allowed_exponents':exponents,'initial_columns':initial,
            'peel_rounds':rounds,'remaining_columns':len(columns),'determinant':determinant,'verified':True}

t,t2,t4=F(397,500),F(63,100),F(397,1000)
assert t**3>F(1,2) and t2**3>F(1,4) and t4**3>F(1,16)
assert (((1+t2)**2)*(F(3,2)+t))**2<F(3,2)**9
assert (1+t2+t4)**2*(F(3,2)+t+t4)<F(3,2)**6
assert (1/(1-t2))**2*2*(1+t)<F(3,2)**9
result={'entropy_inequalities_verified':True,'models':[verify_model(100000,[1,2]),verify_model(10000,[0,2,4]),verify_model(1000,[0,2,4,6])]}
print(json.dumps(result,indent=2))
