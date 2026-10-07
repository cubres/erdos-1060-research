"""Independent exact verification by constructing and summing ALL divisors.

Uses only Python's standard library. It does not use the geometric-sum
formula for sigma or an optimization solver. Run without Python's -O flag.
"""
from __future__ import annotations
from math import gcd, isqrt, prod
import json

A_FACTORS = {11:2, 13:2, 17:1, 19:1, 31:1, 61:1, 97:1,
             127:2, 271:1, 307:2, 331:1, 367:1}
B_FACTORS = {13:1, 17:2, 19:2, 23:1, 31:2, 43:1, 61:2,
             83:1, 127:1, 307:1, 733:1, 5419:1}
M = 5276516179938729922490847708056660616574496169354744299520
TARGET_PRIMES = [2,3,5,7,11,13,17,19,23,31,43,61,83,97,127,271,307,331,367,733,5419]
FULL_SCALED_SOLUTIONS = [
    652479105150920502829614362304,
    657147690133657791842570164368,
    727556371219406840968559824836,
    739864699590775927315723428684,
    848815766422641314463319795642,
    863175482855905248535010666798,
]

def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n)+1))

def factor_over(n: int, primes: list[int]) -> dict[int, int]:
    out = {}
    for p in primes:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            out[p] = e
    if n != 1:
        raise ValueError('The supplied prime list does not factor the input.')
    return out

def check(factors: dict[int, int], target: int) -> dict:
    if any(not is_prime(p) or e < 1 for p, e in factors.items()):
        raise ValueError('Invalid factorization.')
    n = prod(p**e for p, e in factors.items())
    divisors = [1]
    for p, e in factors.items():
        divisors = [d * p**j for d in divisors for j in range(e+1)]
    assert len(divisors) == len(set(divisors)) == prod(e+1 for e in factors.values())
    assert all(n % d == 0 for d in divisors)
    divisor_sum = sum(divisors)
    assert n * divisor_sum == target
    return {'input': str(n), 'factors': factors, 'divisor_count': len(divisors),
            'divisor_sum': str(divisor_sum), 'h': str(n*divisor_sum),
            'cubefree': all(e <= 2 for e in factors.values())}

def main() -> None:
    a = prod(p**e for p,e in A_FACTORS.items())
    b = prod(p**e for p,e in B_FACTORS.items())
    assert a != b and gcd(a*b, 42) == 1
    assert min(set(A_FACTORS) | set(B_FACTORS)) == 11
    for p in set(A_FACTORS) | set(B_FACTORS):
        assert not (A_FACTORS.get(p, 0) == B_FACTORS.get(p, 0) > 0)
    rows = [check(A_FACTORS, M), check(B_FACTORS, M)]
    scaled = [check(factor_over(n, TARGET_PRIMES), 336*M)
              for n in FULL_SCALED_SOLUTIONS]
    assert {int(row['input']) for row in scaled if row['cubefree']} == {12*a,14*a,12*b,14*b}
    assert len({12*a,14*a,12*b,14*b}) == 4
    print(json.dumps({'method': 'Complete divisor construction and summation',
                      'base_pair': rows, 'scaled_witnesses': scaled,
                      'all_checks_passed': True,
                      'scope': 'Verifies the listed witnesses. Completeness of the inverse search is a separate argument.'}, indent=2))

if __name__ == '__main__':
    main()
