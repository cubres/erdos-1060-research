#!/usr/bin/env python3
"""Exact finite regression checks for the two-base rigidity note.

These finite checks are not the proof of the unbounded-exponent theorem.
Run with ordinary Python (not python -O). No third-party packages are used.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt
from pathlib import Path
import json
import time


def primes_to(n: int) -> list[int]:
    s = bytearray(b'\x01') * (n + 1)
    if n >= 0: s[0] = 0
    if n >= 1: s[1] = 0
    for p in range(2, isqrt(n) + 1):
        if s[p]:
            s[p*p:n+1:p] = b'\x00' * ((n-p*p)//p + 1)
    return [p for p in range(2, n + 1) if s[p]]


def prime_by_trial(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, isqrt(n) + 1, 2))


def local_h(p: int, e: int) -> int:
    return p**e * ((p**(e+1)-1)//(p-1))


def local_lists(p: int, cap: int) -> list[int]:
    power, sigma = 1, 1
    out = [1]
    for _ in range(cap):
        power *= p
        sigma += power
        out.append(power*sigma)
    return out


def denominator_tests() -> dict:
    count = 0
    for p in primes_to(101):
        for A in range(1, 41):
            for d in range(1, 41):
                j = Fraction(local_h(p, A-1+d), local_h(p, A-1))
                g = gcd(A, d)
                D = (p**A-1)//(p**g-1)
                assert j.denominator == D
                assert j == p**(2*d) + Fraction(p**d*(p**d-1), p**A-1)
                assert p**(2*d) < j < Fraction(p**(2*d+1), p-1)
                if A >= d:
                    assert j <= p**(2*d) + p**d
                assert Fraction(p**(A-g), 1) <= D < Fraction(p**A, p**g-1)
                count += 1
    assert 4**6 > 5**5
    assert 15 < 16
    for p in primes_to(1000):
        if p < 5: continue
        for d in range(2, p):
            if (p-1) % d == 0:
                phi = sum(gcd(j, d) == 1 for j in range(1, d+1))
                assert 2*phi <= p-1
    return {'increment_and_denominator_cases': count,
            'prime_bound': 101, 'A_and_d_bound': 40}


def pair_test(primes: list[int], cap: int) -> dict:
    values = {p: local_lists(p, cap) for p in primes}
    pairs = 0
    total = 0
    for p, q in combinations(primes, 2):
        seen = {}
        for a, x in enumerate(values[p]):
            for b, y in enumerate(values[q]):
                value = x*y
                assert value not in seen, ('collision', p, q, seen.get(value), (a,b))
                seen[value] = (a,b)
                total += 1
        pairs += 1
    return {'prime_bound': max(primes), 'exponent_cap': cap,
            'fixed_prime_pairs': pairs, 'exponent_vectors_tested': total,
            'collisions': []}


def exceptional_pair_test() -> dict:
    pairs = [(2,1093),(3,1006003),(5,1645333507),(5,188748146801),
             (83,4871),(911,318917),(2903,18787)]
    cap = 60
    records=[]
    for p,q in pairs:
        assert prime_by_trial(p) and prime_by_trial(q)
        assert pow(q,p-1,p*p) == 1
        assert pow(p,q-1,q*q) == 1
        assert pow(q,p-1,p**3) != 1
        assert pow(p,q-1,q**3) != 1
        hp,hq=local_lists(p,cap),local_lists(q,cap)
        seen=set()
        for u in hp:
            for v in hq:
                w=u*v
                assert w not in seen
                seen.add(w)
        records.append({'p':p,'q':q,'both_Fermat_valuations':2,
                        'cap':cap,'distinct_values':len(seen)})
    return {'description':'Seven specified pairs, not a claim about the complete current list',
            'pairs':records}


def collision_distance_test(limit: int = 200000) -> dict:
    sigma=[0]*(limit+1)
    for d in range(1,limit+1):
        for n in range(d,limit+1,d): sigma[n]+=d
    spf=list(range(limit+1))
    for p in range(2,isqrt(limit)+1):
        if spf[p]==p:
            for n in range(p*p,limit+1,p):
                if spf[n]==n: spf[n]=p
    def factor(n: int) -> dict[int,int]:
        f={}
        while n>1:
            p=spf[n]; e=0
            while n%p==0: n//=p; e+=1
            f[p]=e
        return f
    groups={}
    for n in range(1,limit+1): groups.setdefault(n*sigma[n],[]).append(n)
    count=0; minimum=None; first=None
    for target,inputs in groups.items():
        if len(inputs)<2: continue
        factors={n:factor(n) for n in inputs}
        for a,b in combinations(inputs,2):
            fa,fb=factors[a],factors[b]
            changed=sum(fa.get(p,0)!=fb.get(p,0) for p in fa.keys()|fb.keys())
            assert changed>=3, (a,b,target,fa,fb)
            count+=1
            if minimum is None or changed<minimum:
                minimum=changed; first={'a':a,'b':b,'target':target,'changed_bases':changed}
    return {'input_bound':limit,'collision_pairs':count,'minimum_changed_bases':minimum,
            'first_minimum_example':first,
            'scope':'Both inputs are at most the input bound; not complete larger-target fibers.'}


def main() -> None:
    if not __debug__: raise RuntimeError('Run without Python -O; assertions are the checks.')
    start=time.time()
    results={'status':'All finite checks passed; the infinite theorem rests on the written proof.',
             'identities':denominator_tests(),
             'small_pair_census':pair_test(primes_to(1000),24),
             'specified_large_pairs':exceptional_pair_test(),
             'actual_collision_distances':collision_distance_test()}
    results['elapsed_seconds']=round(time.time()-start,3)
    path=Path(__file__).with_name('verification.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
