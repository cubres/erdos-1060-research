"""Exact audit of the overlap identity for h(k)=k*sigma(k).

Uses the Python standard library only. Run:
    python verify_gap.py --limit 200000 --output verification.json
The input-bounded sweep is a regression test, not an asymptotic proof.
"""
from __future__ import annotations
import argparse, json, math, time
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def local_sigma(p: int, e: int) -> int:
    return sum(p**j for j in range(e + 1))


def sigma_from_factors(f: dict[int,int]) -> int:
    return math.prod(local_sigma(p,e) for p,e in f.items())


def number(f: dict[int,int]) -> int:
    return math.prod(p**e for p,e in f.items())


def valuation(n: int, q: int) -> int:
    v = 0
    while n % q == 0:
        n //= q
        v += 1
    return v


def divisors(f: dict[int,int]) -> list[int]:
    d = [1]
    for p,e in f.items():
        d = [a*p**j for a in d for j in range(e+1)]
    return d


def audit_pair(f: dict[int,int], g: dict[int,int]) -> dict:
    x,y = number(f), number(g)
    sx,sy = sigma_from_factors(f),sigma_from_factors(g)
    assert x != y and x*sx == y*sy
    ps = sorted(f.keys() | g.keys())
    min_f = {p:min(f.get(p,0),g.get(p,0)) for p in ps}
    H = math.prod(math.gcd(local_sigma(p,f.get(p,0)),local_sigma(p,g.get(p,0))) for p in ps)
    # Independent formula for each local gcd.
    H_alt = math.prod(local_sigma(p,math.gcd(f.get(p,0)+1,g.get(p,0)+1)-1) for p in ps)
    assert H == H_alt
    sg = sigma_from_factors(min_f)
    t = math.gcd(sx,sy)
    assert sg % H == t % H == 0
    R,T = sg//H,t//H
    assert x*sx % T == 0
    C = Fraction(T,R)
    P = math.prod((Fraction(p,p-1) for p in ps if f.get(p,0)!=g.get(p,0)), start=Fraction(1))
    assert 1 < C*C < P
    compatible = all((f.get(p,0)+1) % (g.get(p,0)+1) == 0 or
                     (g.get(p,0)+1) % (f.get(p,0)+1) == 0 for p in ps)
    assert (R == 1) == compatible
    if compatible:
        assert C.denominator == 1
    out = {'x':str(x), 'y':str(y), 'target':str(x*sx),
           'local_gcd_product':str(H), 'sigma_gcd_inputs':str(sg),
           'overlap_T':str(T), 'defect_R':str(R),
           'rational_multiplier':str(C), 'compatible':compatible}
    for cutoff in [2,3,5,7]:
        if any(f.get(p,0)!=g.get(p,0) for p in ps if p<=cutoff):
            continue
        qs = [q for q in range(2,cutoff+1) if is_prime(q)]
        changed = []
        l1 = {}
        for q in qs:
            total = sum(abs(valuation(local_sigma(p,f.get(p,0)),q)-valuation(local_sigma(p,g.get(p,0)),q)) for p in ps if p>cutoff)
            assert total == 2*valuation(T,q)
            l1[str(q)] = total
        for p in ps:
            if p<=cutoff: continue
            la = tuple(valuation(local_sigma(p,f.get(p,0)),q) for q in qs)
            lb = tuple(valuation(local_sigma(p,g.get(p,0)),q) for q in qs)
            if la!=lb: changed.append(p)
        out[f'cutoff_{cutoff}'] = {'changed_labels':changed,'l1_by_prime':l1}
    return out


def sweep(limit: int) -> dict:
    sig = [0]*(limit+1)
    spf = [0]*(limit+1)
    for d in range(1,limit+1):
        for n in range(d,limit+1,d): sig[n]+=d
    for p in range(2,limit+1):
        if spf[p] == 0:
            for n in range(p,limit+1,p):
                if not spf[n]: spf[n]=p
    def fac(n: int) -> dict[int,int]:
        f={}
        while n>1:
            p=spf[n];e=0
            while n%p==0: n//=p;e+=1
            f[p]=e
        return f
    buckets=defaultdict(list)
    for k in range(1,limit+1): buckets[k*sig[k]].append(k)
    pairs=compat=0
    for ks in buckets.values():
        if len(ks)<2: continue
        for x,y in combinations(ks,2):
            result=audit_pair(fac(x),fac(y))
            pairs+=1;compat+=result['compatible']
    return {'input_limit':limit,'collision_pairs_checked':pairs,
            'compatible_pairs':compat,'incompatible_pairs':pairs-compat,
            'scope':'Both inputs at most the stated limit; no unbounded claim.'}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--limit',type=int,default=200000)
    ap.add_argument('--output',type=Path,default=Path('verification.json'))
    args=ap.parse_args()
    if args.limit<1: ap.error('limit must be positive')
    start=time.monotonic()
    A={11:2,13:2,17:1,19:1,31:1,61:1,97:1,127:2,271:1,307:2,331:1,367:1}
    B={13:1,17:2,19:2,23:1,31:2,43:1,61:2,83:1,127:1,307:1,733:1,5419:1}
    assert all(is_prime(p) for p in A.keys()|B.keys())
    witness=audit_pair(A,B)
    dx,dy=divisors(A),divisors(B)
    assert sum(dx)==sigma_from_factors(A)
    assert sum(dy)==sigma_from_factors(B)
    assert number(A)*sum(dx)==number(B)*sum(dy)
    witness['divisor_counts']=[len(dx),len(dy)]
    Nfactor={2:20,3:5,5:1,7:3,11:2,13:2,17:2,19:2,23:1,31:2,43:1,61:2,83:1,97:1,127:2,271:1,307:2,331:1,367:1,733:1,5419:1}
    assert all(is_prime(p) for p in Nfactor)
    assert number(Nfactor)==number(A)*sum(dx)
    P=math.prod((Fraction(p,p-1) for p in Nfactor),start=Fraction(1))
    assert 4<P<8
    assert P<9  # cutoff 3 exceeds sqrt(P)
    assert len(witness['cutoff_3']['changed_labels'])==16
    assert Fraction(witness['rational_multiplier'])==Fraction(378,341)
    witness['P_target_exact']=str(P)
    witness['claimed_radius_without_compatibility']=2
    witness['actual_number_of_changed_labels']=16
    out={'all_checks_passed':True,
         'small_example':audit_pair({2:2,3:1},{2:1,7:1}),
         'large_counterexample_to_dropping_compatibility':witness,
         'sweep':sweep(args.limit),
         'scope':'Audit of exact identities and a failed proof extension. Not a solution or a counterexample to Erdos 1060.',
         'elapsed_seconds':time.monotonic()-start}
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
