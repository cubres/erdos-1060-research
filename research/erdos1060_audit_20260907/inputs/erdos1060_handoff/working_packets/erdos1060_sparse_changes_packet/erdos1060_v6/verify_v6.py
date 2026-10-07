"""Exact checks for Erdős 1060 research continuation v6.
Python standard library only. No solver, internet, or large-prime tests.
Pairwise coprimality of the factor bases certifies their multiplicative
independence, which is all the finite peeling proof needs.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json, math, time
HERE=Path(__file__).resolve().parent

def primes_to(n:int)->list[int]:
    if n<2:return []
    mark=bytearray(b'\1')*(n+1);mark[:2]=b'\0\0'
    for p in range(2,math.isqrt(n)+1):
        if mark[p]:mark[p*p:n+1:p]=b'\0'*((n-p*p)//p+1)
    return [p for p in range(2,n+1) if mark[p]]

def coprime_product(values:list[int])->int:
    """Product-tree proof that every two distinct row bases are coprime."""
    if not values:return 1
    if len(values)==1:
        assert values[0]>=2
        return values[0]
    mid=len(values)//2
    a=coprime_product(values[:mid]);b=coprime_product(values[mid:])
    assert math.gcd(a,b)==1,'Row bases not pairwise coprime'
    return a*b

def finite_certificate(path:Path)->dict:
    data=json.loads(path.read_text());limit=data['upper_input_prime'];cap=data['exponent_cap']
    low=data['lower_input_prime_exclusive'];cut=data['sigma_rough_cutoff']
    small=primes_to(cut);ps=[p for p in primes_to(limit) if p>low]
    used=set();bases=set();columns=[];records=data['local_factorizations']
    for p in ps:
        local={0:{}}
        for e in range(2,cap+1,2):
            sig=sum(p**j for j in range(e+1))
            if any(sig%q==0 for q in small):continue
            key=f'{p}:{e}';used.add(key)
            fact={int(q):int(v) for q,v in records[key].items()}
            assert all(q>=2 and v>0 for q,v in fact.items())
            assert math.prod(q**v for q,v in fact.items())==p**e*sig
            bases.update(fact);local[e]=fact
        for a,b in combinations(sorted(local),2):
            # b>a; retain all nonzero rows, including non-input row bases.
            d={q:local[b].get(q,0)-local[a].get(q,0) for q in local[a].keys()|local[b].keys()}
            columns.append((p,b,a,{q:v for q,v in d.items() if v}))
    assert used==set(records),'Missing/extra local blocks'
    coprime_product(sorted(bases))
    initial=len(columns);rounds=[]
    while columns:
        owners=defaultdict(set)
        for p,a,b,d in columns:
            for q in d:owners[q].add(p)
        forced={q for q,pp in owners.items() if len(pp)==1}
        kept=[col for col in columns if forced.isdisjoint(col[3])]
        if len(kept)==len(columns):break
        rounds.append(len(columns)-len(kept));columns=kept
    assert initial==data['expected_initial_columns']
    assert rounds==data['expected_deletions_by_round']
    assert not columns,'Not a complete noncollision certificate'
    return {'upper_input_prime':limit,'lower_input_prime_exclusive':low,
        'exponent_cap':cap,'sigma_rough_cutoff':cut,'input_primes':len(ps),
        'verified_local_blocks':len(used),'pairwise_coprime_row_bases':len(bases),
        'initial_columns':initial,'deletions_by_round':rounds,'remaining_columns':0,
        'fully_checked':True}

def factor_small(n:int)->dict[int,int]:
    out={};p=2
    while p*p<=n:
        while n%p==0:out[p]=out.get(p,0)+1;n//=p
        p+=1
    if n>1:out[n]=out.get(n,0)+1
    return out

def sigma_from_divisors(n:int)->int:
    # Independent paired-divisor summation, for small regression examples.
    total=0
    for d in range(1,math.isqrt(n)+1):
        if n%d==0:
            total+=d
            if d*d!=n:total+=n//d
    return total

def pair_check(a:int,b:int)->dict:
    assert a*sigma_from_divisors(a)==b*sigma_from_divisors(b)
    fa=factor_small(a);fb=factor_small(b)
    A=B=U=V=1;incompatible=[]
    for p in fa.keys()|fb.keys():
        x,y=fa.get(p,0),fb.get(p,0)
        if x==y:continue
        high,low=max(x,y),min(x,y)
        if (high+1)%(low+1):incompatible.append(p);continue
        Q=sum(p**i for i in range(high+1))//sum(p**i for i in range(low+1))
        assert Q*sum(p**i for i in range(low+1))==sum(p**i for i in range(high+1))
        if x>y:A*=p**(x-y);U*=Q
        else:B*=p**(y-x);V*=Q
    if incompatible:return {'inputs':[a,b],'incompatible_input_primes':sorted(incompatible)}
    assert U%B==0 and V%A==0
    c=U//B;assert c==V//A and c>1
    support=fa.keys()|fb.keys();P=math.prod(Fraction(p,p-1) for p in support)
    assert 1<c*c<P
    return {'inputs':[a,b],'comparable_at_every_prime':True,'integer_multiplier':c,
            'support_euler_product':str(P),'strict_square_inequality_verified':True}

def local_tests()->dict:
    checked=0
    for p in primes_to(2000):
        if p==3:continue
        ok=[e+1 for e in range(4) if sum(p**j for j in range(e+1))%3]
        for x,y in combinations(ok,2):assert x%y==0 or y%x==0
        checked+=1
    # This illustrates why an alleged forced-larger-prime argument is false.
    assert sum(269**i for i in range(3))==13*37*151
    assert all(q<269 and q>7 for q in (13,37,151))
    # The previous local third-index obstruction, rechecked independently.
    assert sum(29**i for i in range(3))==13*67
    assert all(sum(67**j for j in range(e+1))%q for e in (4,6) for q in (2,3,5,7))
    return {'prime_mod_3_chain_checks':checked,'largest_prime_shortcut_counterexample':{'p':269,'sigma_p_squared':13*37*151,'factors':[13,37,151]},
            'third_index_local_obstruction_verified':True,
            'regression_pairs':[pair_check(160,189),pair_check(12,14)]}

def main()->None:
    t=time.monotonic()
    result={'finite_certificates':[finite_certificate(p) for p in sorted(HERE.glob('finite_model_*.json'))],
            'local_tests':local_tests(),
            'scope':'The finite certificates are not an unbounded-prime proof. The analytic theorems are in the accompanying note.',
            'elapsed_seconds':time.monotonic()-t,'all_checks_passed':True}
    (HERE/'verification_v6.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
