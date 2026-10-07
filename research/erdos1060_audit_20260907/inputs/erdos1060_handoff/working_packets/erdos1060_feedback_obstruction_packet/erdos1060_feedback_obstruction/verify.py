#!/usr/bin/env python3
"""Exact checks for the conditional universal-feedback obstruction.

Only the Python standard library is used. Primality is decided by a complete
trial division using sieved primes, not by a probable-prime test. The analytic
Bateman-Horn implication is conditional and is NOT verified by this computation.
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from math import isqrt
from pathlib import Path


def sieve(bound: int) -> list[int]:
    if bound < 2:
        return []
    flag = bytearray(b'\1') * (bound + 1)
    flag[:2] = b'\0\0'
    for p in range(2, isqrt(bound) + 1):
        if flag[p]:
            flag[p*p:bound+1:p] = b'\0' * ((bound-p*p)//p + 1)
    return [p for p in range(2, bound + 1) if flag[p]]


def is_prime(n: int, trial: list[int], bound: int) -> bool:
    if n < 2:
        return False
    if isqrt(n) > bound:
        raise ValueError('Insufficient certified trial-division range')
    for p in trial:
        if p*p > n:
            break
        if n % p == 0:
            return False
    return True


def sigma_power(p: int, e: int) -> int:
    if p < 2 or e < 0:
        raise ValueError('Invalid base or exponent')
    return (p**(e+1)-1)//(p-1)


def h_power(p: int, e: int) -> int:
    return p**e * sigma_power(p, e)


def valuation(n: int, p: int) -> int:
    if n < 1 or p < 2:
        raise ValueError('Invalid valuation arguments')
    ans = 0
    while n % p == 0:
        n //= p
        ans += 1
    return ans


def poly_add(a: list[int], b: list[int]) -> list[int]:
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    c = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i+j] += x*y
    while len(c) > 1 and c[-1] == 0: c.pop()
    return c


def all_pair_values_distinct(p: int, q: int, cap: int) -> bool:
    left = [h_power(p, a) for a in range(cap+1)]
    right = [h_power(q, b) for b in range(cap+1)]
    values = {u*v for u in left for v in right}
    return len(values) == (cap+1)**2


def verify(limit: int) -> dict:
    if limit < 6:
        raise ValueError('Use a parameter limit at least 6')
    # Coefficient-level polynomial identities, valid for every parameter.
    P, Q, R, S = [1,0,1], [1,1,1], [1,-1,1], [2,2,1]
    assert poly_add(poly_add(poly_mul(P,P), [-c for c in P]), [1]) == poly_mul(Q,R)
    assert poly_add(poly_mul(Q,Q), [1]) == poly_mul(P,S)

    trial_bound = isqrt(limit*limit+limit+1)
    trial = sieve(trial_bound)
    pairs = []
    used = set()
    for t in range(3, limit+1):
        p, q = t*t+1, t*t+t+1
        if not is_prime(p,trial,trial_bound) or not is_prime(q,trial,trial_bound):
            continue
        assert p not in used and q not in used
        used.update((p,q))
        assert p < q < (t+1)**2+1
        assert p*p-p+1 == q*(t*t-t+1)
        assert q*q+1 == p*(t*t+2*t+2)
        # The two negative signed edges and their precise multiplicities.
        assert [valuation(sigma_power(p,e),q) for e in range(6)] == [0,0,0,0,0,1]
        assert [valuation(sigma_power(q,e),p) for e in range(6)] == [0,0,0,1,0,0]
        assert all_pair_values_distinct(p,q,5)
        internal = defaultdict(list)
        for a in range(6):
            for b in range(6):
                internal[(a+int(b==3),b+int(a==5))].append([a,b])
        duplicates = [(key, opts) for key,opts in internal.items() if len(opts)>1]
        assert duplicates == [((5,3),[[4,3],[5,2]])]
        assert h_power(p,4)*h_power(q,3) > h_power(p,5)*h_power(q,2)
        pairs.append({'t': t, 'p': p, 'q': q})

    # Test an extended exponent range for the first pair: E=4p-2.
    # The written lifting proof now establishes injectivity for all exponents.
    first = pairs[0]
    p, q = first['p'], first['q']
    cap = 4*p-2
    assert all(valuation(sigma_power(p,e),q)<=1 for e in range(cap+1))
    assert all(valuation(sigma_power(q,e),p)<=1 for e in range(cap+1))
    assert all_pair_values_distinct(p,q,cap)

    # Independently test the general cross-valuation rigidity lemma on small
    # prime pairs, not just on the displayed polynomial family.
    small_primes = sieve(101)
    general_cases = 0
    for i,p in enumerate(small_primes):
        for q in small_primes[i+1:]:
            for cap0 in range(1,9):
                condition = (
                    all(valuation(sigma_power(p,e),q)<=1 for e in range(cap0+1))
                    and all(valuation(sigma_power(q,e),p)<=1 for e in range(cap0+1))
                )
                if condition:
                    assert all_pair_values_distinct(p,q,cap0)
                    general_cases += 1

    # Finite regression tests for the unrestricted-exponent theorem for
    # nearby primes. The analytic proof, not this finite sweep, is unrestricted.
    close_cases = []
    for i,p in enumerate(small_primes):
        if p < 5: continue
        for q in small_primes[i+1:]:
            if q >= 2*p: break
            r = next(d for d in range(1,q) if pow(p,d,q)==1)
            s0 = next(d for d in range(1,p) if pow(q,d,p)==1)
            if valuation(p**r-1,q)==valuation(q**s0-1,p)==1:
                assert r>=3 and s0>=2
                assert all_pair_values_distinct(p,q,30)
                for e in range(151):
                    expected_q = 0 if (e+1)%r else 1+valuation((e+1)//r,q)
                    expected_p = 0 if (e+1)%s0 else 1+valuation((e+1)//s0,p)
                    assert valuation(sigma_power(p,e),q)==expected_q
                    assert valuation(sigma_power(q,e),p)==expected_p
                close_cases.append({'p':p,'q':q,'order_mod_q':r,'order_mod_p':s0})

    cutoffs = [10**j for j in range(3,9)]
    counts = {str(x): sum(z['q']<=x for z in pairs) for x in cutoffs
              if x <= limit*limit+limit+1}
    return {
        'status': 'No complete proof of Erdos 1060 is claimed.',
        'parameter_range': [3,limit],
        'primality_method': 'Complete trial division by sieved primes',
        'trial_division_bound': trial_bound,
        'polynomial_identities_checked_at_coefficient_level': True,
        'prime_pair_count': len(pairs),
        'vertex_disjoint_positive_two_cycles': len(pairs),
        'certified_lower_bounds_on_A5_by_prime_cutoff': counts,
        'cap5_injectivity_checks': len(pairs),
        'larger_cap_test': {'p':first['p'], 'q':first['q'],
                           'cap':4*first['p']-2, 'number_of_inputs':(4*first['p']-1)**2},
        'general_two_prime_lemma_test_cases': general_cases,
        'close_prime_unrestricted_theorem_regression': {
            'prime_bound':101, 'pair_count':len(close_cases),
            'value_cap_checked':30, 'valuation_cap_checked':150,
            'pairs':close_cases},
        'conditional_statement': 'Bateman-Horn for t^2+1 and t^2+t+1 would imply A5(x) >= x^(1/2-o(1)); no asymptotic prime-pair count is proved here.',
        'pairs': pairs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=10000)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('verification.json'))
    args=parser.parse_args()
    result=verify(args.limit)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='pairs'},indent=2))

if __name__=='__main__': main()
