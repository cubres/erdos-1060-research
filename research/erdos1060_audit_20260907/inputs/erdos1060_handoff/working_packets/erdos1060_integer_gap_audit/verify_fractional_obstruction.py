#!/usr/bin/env python3
"""Exact audit of a fractional obstruction for h(k)=k*sigma(k).

Uses only the Python standard library. Proves a single cubefree fiber has one
member, checks the full affine parameterization, and verifies that every
remaining column is positive at a rational feasible point. No asymptotic
claim is made.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import isqrt, prod
import json
from pathlib import Path

TARGET_FACTORS = {2: 7, 3: 3, 5: 1, 7: 2, 13: 1, 19: 2, 127: 1}
TARGET = 504654433920
INPUT = 492765


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def valuation(n: int, p: int) -> int:
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def local_h(p: int, e: int) -> int:
    return p**e * sum(p**j for j in range(e + 1))


def rank(matrix: list[list[int | F]]) -> int:
    a = [list(map(F, row)) for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        scale = a[r][c]
        a[r] = [v / scale for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                factor = a[i][c]
                a[i] = [x - factor*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def affine(u: F, v: F, t: F) -> dict[tuple[int, int], F]:
    return {
        (2, 0): 3-2*v-4*t,
        (2, 1): u+3*v+6*t-4,
        (2, 2): 2-u-v-2*t,
        (3, 0): u+2*v+5*t-3,
        (3, 1): 3-u-v-5*t,
        (3, 2): 1-v,
        (5, 0): t,
        (5, 1): 1-t,
        (7, 0): 1-u-t,
        (7, 1): u,
        (7, 2): t,
        (13, 0): 1-v,
        (13, 1): v,
        (19, 1): t,
        (19, 2): 1-t,
        (127, 0): 1-t,
        (127, 1): t,
    }


def main() -> None:
    ps = list(TARGET_FACTORS)
    require(all(prime(p) for p in ps), 'Unproved target prime')
    require(prod(p**e for p, e in TARGET_FACTORS.items()) == TARGET,
            'Target factorization is incorrect')
    domains = {p: [e for e in range(min(2, TARGET_FACTORS[p]) + 1)
                   if TARGET % local_h(p, e) == 0] for p in ps}
    original = {p: es[:] for p, es in domains.items()}
    require(sum(map(len, domains.values())) == 18, 'Wrong initial option count')

    # Necessary-condition row propagation. Every actual assignment supplies
    # a completion in each individual prime-valuation row.
    removed = []
    while True:
        bad = set()
        for q in ps:
            for p in ps:
                attainable = {0}
                for r in ps:
                    if r == p:
                        continue
                    contributions = {valuation(local_h(r, e), q) for e in domains[r]}
                    attainable = {a+b for a in attainable for b in contributions}
                for e in domains[p]:
                    remaining = TARGET_FACTORS[q] - valuation(local_h(p, e), q)
                    if remaining not in attainable:
                        bad.add((p, e))
        if not bad:
            break
        removed.extend(sorted(bad))
        domains = {p: [e for e in es if (p, e) not in bad]
                   for p, es in domains.items()}
        require(all(domains.values()), 'Propagation emptied a domain')
    require(removed == [(19, 0)], 'Unexpected exact row eliminations')

    options = [(p, e) for p in ps for e in domains[p]]
    a = [[int(r == p) for r, e in options] for p in ps]
    b = [1] * len(ps)
    for q in ps:
        a.append([valuation(local_h(p, e), q) for p, e in options])
        b.append(TARGET_FACTORS[q])
    require(len(options) == 17 and rank(a) == 14, 'Rank or column count mismatch')

    def vector(u: F, v: F, t: F) -> list[F]:
        mapping = affine(u, v, t)
        require(set(mapping) == set(options), 'Parameterization domain mismatch')
        return [F(mapping[option]) for option in options]

    def solves(x: list[F]) -> bool:
        return all(sum(c*xi for c, xi in zip(row, x)) == rhs
                   for row, rhs in zip(a, b))

    # Checking a constant and each of three unit directions proves the
    # affine formula for all rational/real parameter values.
    x0 = vector(F(0), F(0), F(0))
    require(solves(x0), 'Affine constant is not a solution')
    directions = []
    for i in range(3):
        parameters = [F(0)]*3
        parameters[i] = F(1)
        x = vector(*parameters)
        require(solves(x), 'Affine direction does not preserve equations')
        directions.append([xi-zi for xi, zi in zip(x, x0)])
    require(rank(directions) == 3, 'Parameter directions are dependent')
    # rank(A)=14 on 17 columns now proves completeness of the parameterization.

    fractional = vector(F(1, 3), F(2, 3), F(1, 3))
    require(solves(fractional), 'Fractional point is infeasible')
    require(all(0 < x < 1 for x in fractional), 'Point is not strictly positive')

    # Each of u,v,t is itself an indicator, so only eight binary triples
    # can produce a binary solution; this checks all of them exactly.
    binary = []
    for triple in product((0, 1), repeat=3):
        x = vector(*map(F, triple))
        if all(xi in (0, 1) for xi in x):
            require(solves(x), 'Binary endpoint is infeasible')
            k = prod(p**e for (p, e), xi in zip(options, x) if xi)
            binary.append({'parameters': triple, 'input': k})
    require(binary == [{'parameters': (1, 1, 0), 'input': INPUT}],
            'Unexpected binary fiber')

    # Independent arithmetic check, with all divisors formed and summed.
    factorization = {3: 1, 5: 1, 7: 1, 13: 1, 19: 2}
    divisors = [1]
    for p, e in factorization.items():
        divisors = [d*p**j for d in divisors for j in range(e+1)]
    require(prod(p**e for p, e in factorization.items()) == INPUT,
            'Input factorization mismatch')
    require(len(divisors) == 48 and len(set(divisors)) == 48,
            'Incomplete or duplicate divisor construction')
    require(INPUT * sum(divisors) == TARGET, 'Direct divisor-sum check failed')

    # Every unrestricted preimage divides TARGET. Enumerate its 2,304 divisors,
    # with no input-size cutoff, to check the full fiber separately.
    full_fiber = []
    tested_divisors = 0
    for exponents in product(*(range(TARGET_FACTORS[p]+1) for p in ps)):
        tested_divisors += 1
        k = prod(p**e for p, e in zip(ps, exponents))
        hk = prod(local_h(p, e) for p, e in zip(ps, exponents))
        if hk == TARGET:
            full_fiber.append(k)
    require(tested_divisors == 2304, 'Incomplete divisor search')
    require(full_fiber == [INPUT], 'Unexpected unrestricted fiber')

    result = {
        'target': TARGET, 'target_factors': TARGET_FACTORS,
        'input': INPUT, 'sigma_input': sum(divisors), 'divisor_count': len(divisors),
        'initial_domains': original, 'removed_options': removed,
        'surviving_domains': domains, 'columns': len(options),
        'rational_rank': rank(a), 'real_affine_dimension': len(options)-rank(a),
        'positive_fractional_point': {f'{p},{e}': str(x)
                                      for (p, e), x in zip(options, fractional)},
        'binary_solutions': binary,
        'zero_budget_certificate_obstruction':
            'A strictly positive feasible point forces every nonnegative zero-budget column score to be zero.',
        'unrestricted_divisors_tested': tested_divisors,
        'unrestricted_fiber': full_fiber,
        'scope': 'Single target; cubefree affine certificate and complete unrestricted divisor census. No asymptotic claim.',
    }
    output = Path(__file__).with_name('verification.json')
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('target', 'input', 'sigma_input',
          'columns', 'rational_rank', 'real_affine_dimension', 'binary_solutions')}, indent=2))
    print('All exact checks passed; results written to', output)


if __name__ == '__main__':
    main()
